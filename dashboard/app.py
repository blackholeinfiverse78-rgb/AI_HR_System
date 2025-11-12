import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HR-AI Dashboard", layout="wide")

API_BASE = "http://localhost:5000"

st.title("🚀 HR-AI System Dashboard")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose Page", ["Overview", "Candidates", "Feedback", "Automation"])

def make_api_request(method, endpoint, data=None):
    try:
        url = f"{API_BASE}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

if page == "Overview":
    st.header("System Overview")
    
    col1, col2, col3 = st.columns(3)
    
    # Check system health
    health_data, error = make_api_request("GET", "/health")
    if health_data:
        with col1:
            st.metric("System Status", "Healthy", "🟢")
        with col2:
            st.metric("Database", "Connected", "✅")
        with col3:
            st.metric("API", "Active", "⚡")
    else:
        st.error(f"System Health Check Failed: {error}")
    
    # Show recent feedback
    feedback_data, error = make_api_request("GET", "/feedback/logs")
    if feedback_data and len(feedback_data) > 0:
        st.subheader("Recent Feedback")
        df = pd.DataFrame(feedback_data)
        st.dataframe(df.head(10))

elif page == "Candidates":
    st.header("Candidate Management")
    
    # Add new candidate
    with st.expander("Add New Candidate"):
        with st.form("add_candidate"):
            name = st.text_input("Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone* (Format: +91-XXXXXXXXXX)")
            skills_input = st.text_area("Skills* (comma-separated)")
            
            submitted = st.form_submit_button("Add Candidate")
            
            if submitted:
                if name and email and phone and skills_input:
                    skills = [skill.strip() for skill in skills_input.split(",")]
                    candidate_data = {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "skills": skills
                    }
                    
                    result, error = make_api_request("POST", "/candidate/add", candidate_data)
                    if result:
                        st.success(f"Candidate added successfully! ID: {result['candidate_id']}")
                        st.rerun()
                    else:
                        st.error(f"Failed to add candidate: {error}")
                else:
                    st.error("Please fill all required fields")
    
    # List candidates
    st.subheader("Current Candidates")
    candidates_data, error = make_api_request("GET", "/candidate/list")
    if candidates_data:
        if len(candidates_data) > 0:
            df = pd.DataFrame(candidates_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No candidates found. Add some candidates to get started.")
    else:
        st.error(f"Failed to load candidates: {error}")

elif page == "Feedback":
    st.header("HR Feedback System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Submit Feedback")
        with st.form("feedback_form"):
            candidate_id = st.number_input("Candidate ID", min_value=1, step=1)
            feedback_score = st.slider("Feedback Score", 1, 5, 3)
            comment = st.text_area("Comment")
            actual_outcome = st.selectbox("Actual Outcome", ["accept", "reject", "reconsider"])
            
            submitted = st.form_submit_button("Submit Feedback")
            
            if submitted:
                feedback_data = {
                    "candidate_id": candidate_id,
                    "feedback_score": feedback_score,
                    "comment": comment,
                    "actual_outcome": actual_outcome
                }
                
                result, error = make_api_request("POST", "/feedback/hr_feedback", feedback_data)
                if result:
                    st.success("Feedback submitted successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to submit feedback: {error}")
    
    with col2:
        st.subheader("Feedback History")
        feedback_data, error = make_api_request("GET", "/feedback/logs")
        if feedback_data:
            if len(feedback_data) > 0:
                df = pd.DataFrame(feedback_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No feedback logs found.")
        else:
            st.error(f"Failed to load feedback: {error}")

elif page == "Automation":
    st.header("Automation Control")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trigger Event")
        with st.form("automation_form"):
            candidate_id = st.number_input("Candidate ID", min_value=1, step=1)
            event_type = st.selectbox("Event Type", [
                "shortlisted", "rejected", "interview_scheduled", "onboarding_completed"
            ])
            
            # Optional overrides
            st.write("Optional Overrides:")
            override_email = st.text_input("Override Email (optional)")
            override_phone = st.text_input("Override Phone (optional)")
            
            submitted = st.form_submit_button("Trigger Automation")
            
            if submitted:
                metadata = {}
                if override_email:
                    metadata["override_email"] = override_email
                if override_phone:
                    metadata["override_phone"] = override_phone
                
                event_data = {
                    "candidate_id": candidate_id,
                    "event_type": event_type,
                    "metadata": metadata
                }
                
                result, error = make_api_request("POST", "/trigger/", event_data)
                if result:
                    st.success("Automation triggered successfully!")
                    st.json(result)
                else:
                    st.error(f"Failed to trigger automation: {error}")
    
    with col2:
        st.subheader("Automation History")
        candidate_id_history = st.number_input("Candidate ID for History", min_value=1, step=1, key="history_id")
        
        if st.button("Load History"):
            history_data, error = make_api_request("GET", f"/trigger/history/{candidate_id_history}")
            if history_data:
                if len(history_data.get("automation_history", [])) > 0:
                    df = pd.DataFrame(history_data["automation_history"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No automation history found for this candidate.")
            else:
                st.error(f"Failed to load history: {error}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**HR-AI System v1.0**")
st.sidebar.markdown("Backend: FastAPI + SQLite")
st.sidebar.markdown("Frontend: Streamlit")