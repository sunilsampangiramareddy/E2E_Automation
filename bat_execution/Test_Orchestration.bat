@echo off
REM Set the working directory to the project directory
cd /d %~dp0..

REM Activate the virtual environment (if using one)
call venv\Scripts\activate

REM Run the specific Pytest test script
pytest tests_Orchestration\Test_Orchestration.py --browser_type=chromium --url=https://netapp2--uat.sandbox.lightning.force.com/ --headed --reruns 2

REM Deactivate the virtual environment
call venv\Scripts\deactivate

REM Pause to keep the command prompt open after execution
pause