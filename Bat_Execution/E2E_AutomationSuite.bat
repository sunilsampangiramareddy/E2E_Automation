@echo off
REM Set the working directory to the project directory
cd /d C:\Automation_Project\E2E_Automation

REM Activate the virtual environment (if using one)
call venv1\Scripts\activate

REM Construct the full test script path
set TEST_SCRIPT_PATH=%TEST_SCRIPT%

REM Run the specific Pytest test script with parameters
pytest %TEST_SCRIPT_PATH% --browser_type=%BROWSER_TYPE% --url=%URL% %HEADED_TYPE% --reruns %RERUNS%

REM Deactivate the virtual environment
call venv1\Scripts\deactivate

REM Pause to keep the command prompt open after execution
pause