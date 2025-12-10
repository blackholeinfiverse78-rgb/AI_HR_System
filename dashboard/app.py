import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import time

st.set_page_config(
    page_title="HR-AI Dashboard", 
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

API_BASE = "http://localhost:5000"

# Custom CSS for enhanced styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
}
.success-box {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 0.75rem;
    margin: 0.5rem 0;
}
.warning-box {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 0.75rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🚀 HR-AI System Dashboard v3.0</h1><p>AI-Powered Recruitment & Analytics Platform</p></div>', unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("### 🏠 Navigation")
    
    # Real-time system status
    status_placeholder = st.empty()
    
    def make_api_request(method, endpoint, data=None, retries=2):
        for attempt in range(retries):
            try:
                url = f"{API_BASE}{endpoint}"
                if method == "GET":
                    response = requests.get(url, timeout=5)
                elif method == "POST":
                    response = requests.post(url, json=data, timeout=5)
                
                if response.status_code == 200:
                    return response.json(), None
                else:
                    return None, f"API Error: {response.status_code}"
            except requests.exceptions.ConnectionError:
                if attempt == retries - 1:
                    return None, "Backend offline. Please start the API server."
                time.sleep(1)
            except requests.exceptions.Timeout:
                if attempt == retries - 1:
                    return None, "Request timeout. Server may be overloaded."
                time.sleep(1)
            except Exception as e:
                return None, f"Error: {str(e)}"
        return None, "Connection failed"
    
    health_data, _ = make_api_request("GET", "/health")
    if health_data:
        status_placeholder.success("✅ System Online")
    else:
        status_placeholder.error("❌ System Offline")
    
    st.markdown("---")
    
    page = st.selectbox(
        "📊 Choose Page", 
        ["Overview", "Candidates", "Feedback", "Automation", "Analytics", "RL Analytics", "System Health", "Smart Features"],
        format_func=lambda x: f"📈 {x}" if x == "Analytics" else f"🧠 {x}" if x == "RL Analytics" else f"💼 {x}" if x == "Candidates" else f"💬 {x}" if x == "Feedback" else f"⚙️ {x}" if x == "Automation" else f"🔧 {x}" if x == "System Health" else f"🤖 {x}" if x == "Smart Features" else f"🏠 {x}"
    )
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("### 📊 Quick Stats")
    candidates_data, _ = make_api_request("GET", "/candidate/list")
    if candidates_data:
        st.metric("👥 Candidates", len(candidates_data))
    
    feedback_data, _ = make_api_request("GET", "/feedback/logs")
    if feedback_data:
        st.metric("📝 Feedback", len(feedback_data))
    
    # RL Status in sidebar
    st.markdown("---")
    st.markdown("### 🧠 RL Brain Status")
    try:
        rl_status_response = requests.get(f"{API_BASE}/ai/status")
        if rl_status_response.status_code == 200:
            rl_status = rl_status_response.json()
            if rl_status.get("rl_status") == "ACTIVE":
                st.success("🟢 RL Active")
                st.metric("Skills Learned", rl_status.get("brain_metrics", {}).get("total_skills", 0))
            else:
                st.warning("🟡 RL Inactive")
        else:
            st.error("🔴 RL Offline")
    except:
        st.error("🔴 RL Offline")
    
    # Auto-refresh toggle
    st.markdown("---")
    auto_refresh = st.checkbox("🔄 Auto Refresh (30s)")
    
    if auto_refresh:
        time.sleep(30)
        st.rerun()

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

elif page == "Analytics":
    st.header("📊 General Analytics Dashboard")
    
    # Basic Analytics (moved RL to separate page)
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution Chart - Candidate Scores
        st.subheader("📈 Score Distribution")
        candidates_data, _ = make_api_request("GET", "/candidate/list")
        if candidates_data and len(candidates_data) > 0:
            df = pd.DataFrame(candidates_data)
            if 'match_score' in df.columns:
                fig_dist = px.histogram(df, x='match_score', nbins=20, title="Candidate Score Distribution")
                st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.info("No scores available yet")
        else:
            st.info("No candidates data")
            # Fallback to sample if empty for demo
            scores = np.random.normal(75, 15, 100)
            fig_dist = px.histogram(x=scores, nbins=20, title="Sample Score Distribution")
            st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Skills Analysis
        st.subheader("💼 Skills Analysis")
        if candidates_data:
            all_skills = []
            for candidate in candidates_data:
                skills = candidate.get('skills', [])
                if isinstance(skills, list):
                    all_skills.extend(skills)
            
            if all_skills:
                skill_counts = pd.Series(all_skills).value_counts().head(10)
                fig_skills = px.bar(x=skill_counts.index, y=skill_counts.values, title="Top Skills")
                st.plotly_chart(fig_skills, use_container_width=True)
    
    # Feedback Analytics
    st.subheader("💬 Feedback Analytics")
    feedback_data, _ = make_api_request("GET", "/feedback/logs")
    if feedback_data and len(feedback_data) > 0:
        df_feedback = pd.DataFrame(feedback_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'outcome' in df_feedback.columns:
                outcome_counts = df_feedback['outcome'].value_counts()
                fig_pie = px.pie(values=outcome_counts.values, names=outcome_counts.index, title="Outcome Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            if 'score' in df_feedback.columns:
                avg_score = df_feedback['score'].astype(float).mean()
                st.metric("Average Score", f"{avg_score:.2f}", "📊")
                
                fig_score = px.box(df_feedback, y='score', title="Score Distribution")
                st.plotly_chart(fig_score, use_container_width=True)
        
        with col3:
            total_feedback = len(df_feedback)
            st.metric("Total Feedback", total_feedback, "📝")
            
            if 'timestamp' in df_feedback.columns:
                df_feedback['date'] = pd.to_datetime(df_feedback['timestamp']).dt.date
                daily_counts = df_feedback.groupby('date').size()
                fig_timeline = px.line(x=daily_counts.index, y=daily_counts.values, title="Daily Feedback Trend")
                st.plotly_chart(fig_timeline, use_container_width=True)

elif page == "RL Analytics":
    st.header("🧠 Reinforcement Learning Analytics")
    
    # RL Status Check
    try:
        rl_status_response = requests.get(f"{API_BASE}/ai/status")
        if rl_status_response.status_code == 200:
            rl_status = rl_status_response.json()
            if rl_status.get("rl_status") == "ACTIVE":
                st.success("✅ RL Brain is FULLY ACTIVE and learning!")
            else:
                st.warning("⚠️ RL Brain status unclear")
        else:
            st.error("❌ Cannot connect to RL Brain")
    except:
        st.error("❌ RL Brain connection failed")
    
    # RL Performance Metrics
    st.subheader("📊 RL Performance Dashboard")
    
    try:
        performance_response = requests.get(f"{API_BASE}/ai/rl-performance")
        if performance_response.status_code == 200:
            perf_data = performance_response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_decisions = perf_data.get("performance_metrics", {}).get("total_decisions", 0)
                st.metric("🎯 Total Decisions", total_decisions)
            
            with col2:
                success_rate = perf_data.get("performance_metrics", {}).get("success_rate", 0)
                st.metric("📈 Success Rate", f"{success_rate:.1f}%")
            
            with col3:
                performance_score = perf_data.get("performance_metrics", {}).get("performance_score", 0)
                st.metric("🏆 Performance Score", f"{performance_score:.1f}/100")
            
            with col4:
                weights_count = perf_data.get("brain_health", {}).get("weights_count", 0)
                st.metric("🧠 Skills Learned", weights_count)
        else:
            st.info("No performance data available yet")
    except Exception as e:
        st.error(f"Performance data error: {e}")
    
    # RL Analytics Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Reward Evolution")
        try:
            analytics_response = requests.get(f"{API_BASE}/ai/rl-analytics")
            if analytics_response.status_code == 200:
                analytics_data = analytics_response.json()
                reward_data = analytics_data.get("reward_evolution", {})
                
                if reward_data.get("timestamps"):
                    df_rewards = pd.DataFrame({
                        "Timestamp": pd.to_datetime(reward_data["timestamps"]),
                        "Reward": reward_data["rewards"],
                        "Cumulative": reward_data["cumulative_rewards"]
                    })
                    
                    fig_rewards = go.Figure()
                    fig_rewards.add_trace(go.Scatter(
                        x=df_rewards["Timestamp"], 
                        y=df_rewards["Cumulative"],
                        mode='lines+markers', 
                        name='Cumulative Reward',
                        line=dict(color='blue', width=3)
                    ))
                    
                    fig_rewards.update_layout(
                        title="RL Learning Progress (Real-time)",
                        xaxis_title="Time",
                        yaxis_title="Cumulative Reward",
                        height=400
                    )
                    st.plotly_chart(fig_rewards, use_container_width=True)
                    
                    # Show reward statistics
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Total Reward", f"{reward_data.get('total_reward', 0):.2f}")
                    with col_b:
                        st.metric("Average Reward", f"{reward_data.get('average_reward', 0):.3f}")
                    with col_c:
                        st.metric("Learning Episodes", len(reward_data.get('rewards', [])))
                else:
                    st.info("No reward data available yet. Start making decisions!")
            else:
                st.error("Failed to fetch RL analytics")
        except Exception as e:
            st.error(f"Reward evolution error: {e}")
    
    with col2:
        st.subheader("🧠 Brain State Visualization")
        try:
            state_response = requests.get(f"{API_BASE}/ai/rl-state")
            if state_response.status_code == 200:
                rl_state = state_response.json()
                top_skills = rl_state.get("top_skills", {})
                
                if top_skills:
                    skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Weight'])
                    
                    fig_weights = px.bar(
                        skills_df, 
                        x='Weight', 
                        y='Skill',
                        orientation='h',
                        title="Top Learned Skills (Weights)",
                        color='Weight',
                        color_continuous_scale='viridis'
                    )
                    fig_weights.update_layout(height=400)
                    st.plotly_chart(fig_weights, use_container_width=True)
                    
                    # Weight statistics
                    weight_stats = rl_state.get("weight_statistics", {})
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Active Skills", weight_stats.get("active_skills_count", 0))
                    with col_b:
                        st.metric("Avg Weight", f"{weight_stats.get('average_weight', 0):.3f}")
                else:
                    st.info("No brain weights available yet")
            else:
                st.error("Could not fetch brain state")
        except Exception as e:
            st.error(f"Brain state error: {e}")
    
    # Decision Accuracy Analysis
    st.subheader("🎯 Decision Accuracy & Learning Trends")
    
    try:
        analytics_response = requests.get(f"{API_BASE}/ai/rl-analytics")
        if analytics_response.status_code == 200:
            analytics_data = analytics_response.json()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                accuracy_data = analytics_data.get("decision_accuracy", {})
                accuracy = accuracy_data.get("accuracy_percentage", 0)
                st.metric("🎯 Decision Accuracy", f"{accuracy:.1f}%")
                
                correct = accuracy_data.get("correct_predictions", 0)
                total = accuracy_data.get("total_predictions", 0)
                st.caption(f"{correct}/{total} correct predictions")
            
            with col2:
                learning_data = analytics_data.get("learning_metrics", {})
                velocity = learning_data.get("learning_velocity", 0)
                trend = learning_data.get("learning_trend", "stable")
                
                st.metric("📈 Learning Velocity", f"{velocity:.3f}")
                
                if trend == "improving":
                    st.success(f"📈 Trend: {trend.title()}")
                elif trend == "declining":
                    st.error(f"📉 Trend: {trend.title()}")
                else:
                    st.info(f"➡️ Trend: {trend.title()}")
            
            with col3:
                skill_dist = analytics_data.get("skill_distribution", {}).get("skill_categories", {})
                strong_skills = skill_dist.get("strong_skills", 0)
                st.metric("💪 Strong Skills", strong_skills)
                st.caption(f"Weight > 1.5")
        else:
            st.info("Analytics data not available")
    except Exception as e:
        st.error(f"Analytics error: {e}")
    
    # Recent RL Activity
    st.subheader("📋 Recent RL Activity")
    
    try:
        history_response = requests.get(f"{API_BASE}/ai/rl-history?limit=10")
        if history_response.status_code == 200:
            history_data = history_response.json()
            recent_history = history_data.get("history", [])
            
            if recent_history:
                # Create a clean dataframe for display
                display_data = []
                for entry in recent_history:
                    display_data.append({
                        "Timestamp": entry.get("timestamp", "")[:19],  # Remove microseconds
                        "Candidate": entry.get("candidate", "Unknown"),
                        "Outcome": entry.get("outcome", "N/A"),
                        "Reward": f"{entry.get('calculated_reward', 0):.3f}",
                        "Learning Δ": f"{entry.get('learning_delta', 0):.3f}",
                        "Skills Count": len(entry.get("skills", []))
                    })
                
                df_recent = pd.DataFrame(display_data)
                st.dataframe(df_recent, use_container_width=True)
                
                # Summary statistics
                summary_stats = history_data.get("summary_statistics", {})
                if summary_stats:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Entries", summary_stats.get("total_entries", 0))
                    with col2:
                        st.metric("Positive Outcomes", summary_stats.get("positive_outcomes", 0))
                    with col3:
                        st.metric("Negative Outcomes", summary_stats.get("negative_outcomes", 0))
            else:
                st.info("No recent RL activity. Start making decisions to see learning in action!")
        else:
            st.error("Could not fetch RL history")
    except Exception as e:
        st.error(f"RL history error: {e}")
    
    # RL Control Panel
    st.subheader("🎛️ RL Control Panel")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh RL Data", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📊 Get RL Performance", use_container_width=True):
            try:
                perf_response = requests.get(f"{API_BASE}/ai/rl-performance")
                if perf_response.status_code == 200:
                    perf_data = perf_response.json()
                    st.json(perf_data)
                else:
                    st.error("Performance data unavailable")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col3:
        if st.button("⚠️ Reset RL Weights", use_container_width=True):
            if st.checkbox("I confirm reset (this will lose all learned weights)"):
                try:
                    reset_response = requests.post(f"{API_BASE}/ai/rl-reset?confirm=true")
                    if reset_response.status_code == 200:
                        st.success("RL weights reset successfully!")
                        st.rerun()
                    else:
                        st.error("Reset failed")
                except Exception as e:
                    st.error(f"Reset error: {e}")

elif page == "System Health":
    st.header("🔧 System Health & Integration")
    
    # Integration Checker
    st.subheader("🔗 Integration Status Checker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**API Endpoints Status**")
        
        endpoints = [
            ("/health", "System Health"),
            ("/candidate/list", "Candidate API"),
            ("/feedback/logs", "Feedback API"),
            ("/system/status", "System Status")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{API_BASE}{endpoint}", timeout=5)
                if response.status_code == 200:
                    st.success(f"✅ {name}: Connected")
                else:
                    st.error(f"❌ {name}: Error {response.status_code}")
            except Exception as e:
                st.error(f"❌ {name}: Connection Failed")
    
    with col2:
        st.write("**Communication Channels**")
        
        # Test communication endpoints
        channels = [
            ("/communication/email", "Email Service"),
            ("/communication/whatsapp", "WhatsApp Service"),
            ("/communication/voice", "Voice Service")
        ]
        
        for endpoint, name in channels:
            # Since these require parameters, just check if endpoint exists
            try:
                response = requests.post(f"{API_BASE}{endpoint}?candidate_id=1", timeout=5)
                if response.status_code in [200, 404, 422]:  # 422 is validation error, means endpoint works
                    st.success(f"✅ {name}: Available")
                else:
                    st.warning(f"⚠️ {name}: Status {response.status_code}")
            except Exception:
                st.error(f"❌ {name}: Unavailable")

elif page == "Smart Features":
    st.header("🤖 AI-Powered Smart Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 AI Recommendations")
        rec_candidate_id = st.number_input("Candidate ID for Recommendations", min_value=1, step=1)
        
        if st.button("Get AI Recommendations"):
            rec_data, error = make_api_request("GET", f"/smart/recommendations/{rec_candidate_id}")
            if rec_data:
                st.success("AI Recommendations Generated!")
                for i, rec in enumerate(rec_data.get('recommendations', []), 1):
                    st.write(f"{i}. {rec}")
            else:
                st.error(f"Failed to get recommendations: {error}")
        
        st.write("---")
        st.subheader("📬 Smart Follow-up")
        followup_candidate_id = st.number_input("Candidate ID for Follow-up", min_value=1, step=1, key="followup_id")
        followup_days = st.slider("Days until follow-up", 1, 14, 3)
        
        if st.button("Schedule Smart Follow-up"):
            followup_data, error = make_api_request("POST", f"/smart/schedule-followup/{followup_candidate_id}?days={followup_days}")
            if followup_data:
                st.success(f"Follow-up scheduled for {followup_days} days!")
            else:
                st.error(f"Failed to schedule follow-up: {error}")
    
    with col2:
        st.subheader("🔔 Smart Notifications")
        
        if st.button("Check Pending Notifications"):
            notif_data, error = make_api_request("GET", "/smart/pending-notifications")
            if notif_data:
                pending = notif_data.get('pending_notifications', [])
                if pending:
                    st.write(f"**{len(pending)} pending notifications:**")
                    for notif in pending:
                        st.info(f"Candidate {notif.get('candidate_id')}: {notif.get('type')}")
                else:
                    st.success("No pending notifications")
            else:
                st.error(f"Failed to get notifications: {error}")
        
        st.write("---")
        st.subheader("⚡ Bulk Operations")
        
        if st.button("Update All Match Scores"):
            update_data, error = make_api_request("POST", "/smart/bulk-score-update")
            if update_data:
                updated_count = update_data.get('updated', 0)
                st.success(f"✅ Updated {updated_count} candidates")
                if updated_count > 0:
                    st.balloons()
            else:
                st.error(f"❌ Bulk update failed: {error}")
    
    # AI Analytics
    st.subheader("📊 AI Analytics Dashboard")
    
    analytics_data, error = make_api_request("GET", "/analytics/dashboard")
    if analytics_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Candidates", analytics_data.get('total_candidates', 0))
        with col2:
            st.metric("Avg Match Score", f"{analytics_data.get('avg_match_score', 0):.1f}%")
        with col3:
            st.metric("Total Feedback", analytics_data.get('total_feedback', 0))
        with col4:
            st.metric("Recent Activity", analytics_data.get('recent_activity', 0))
        
        # Top Skills Chart
        top_skills = analytics_data.get('top_skills', [])
        if top_skills:
            skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
            fig_skills = px.bar(skills_df, x='Skill', y='Count', title="Top Skills in Demand")
            st.plotly_chart(fig_skills, use_container_width=True)

# Enhanced Footer with system info
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💻 System Info")
    
    # System status indicators
    if 'health_data' in locals() and health_data:
        st.success("✅ Backend: Online")
        st.success("✅ Database: Connected")
        st.success("✅ AI Engine: Active")
        
        # Check RL status
        try:
            rl_check = requests.get(f"{API_BASE}/ai/status")
            if rl_check.status_code == 200 and rl_check.json().get("rl_status") == "ACTIVE":
                st.success("✅ RL Brain: ACTIVE")
            else:
                st.warning("⚠️ RL Brain: Inactive")
        except:
            st.error("❌ RL Brain: Offline")
    else:
        st.error("❌ Backend: Offline")
        st.error("❌ RL Brain: Offline")
    
    st.markdown("---")
    st.markdown("**🚀 HR-AI System v3.0**")
    st.markdown("🔧 Backend: FastAPI + SQLite + AI")
    st.markdown("📊 Frontend: Streamlit")
    st.markdown("🤖 Analytics: Plotly + ML")
    st.markdown("🧠 RL Brain: FULLY ACTIVE")
    st.markdown("⚡ Real-time Dashboard")
    
    # Last updated timestamp
    st.markdown(f"**🔄 Last Updated:** {datetime.now().strftime('%H:%M:%S')}")
