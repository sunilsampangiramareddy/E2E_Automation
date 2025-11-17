@echo off
REM Set the working directory to the project directory
cd /d C:\Automation_Project\E2E_Automation

REM Activate the virtual environment (if using one)
call venv1\Scripts\activate

REM Run the specific Pytest test script
pytest tests_SFDC\TC_Login.py tests_SFDC\TC_CreateOpportunity.py --browser_type=chromium --url=https://netapp2--uat.sandbox.lightning.force.com/ --headless --reruns 1

REM Deactivate the virtual environment
call venv1\Scripts\deactivate

REM Pause to keep the command prompt open after execution
pause