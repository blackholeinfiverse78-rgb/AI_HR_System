@echo off
echo Running HR-AI System Tests...
echo.

echo [1/3] Unit Tests
python test_runner.py
if %errorlevel% neq 0 goto :error

echo.
echo [2/3] Integration Tests  
python run_tests.py
if %errorlevel% neq 0 goto :error

echo.
echo [3/3] Quick Validation
python quick_test.py
if %errorlevel% neq 0 goto :error

echo.
echo ✅ ALL TESTS PASSED
goto :end

:error
echo ❌ TESTS FAILED
exit /b 1

:end