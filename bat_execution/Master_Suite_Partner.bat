@echo off
REM Set the working directory to the project directory
cd /d %~dp0..

REM Activate the virtual environment (if using one)
call venv\Scripts\activate

REM Run the specific Pytest test script
pytest utils\master_suite.py tests_Partner_Base\TC_PartnerLogin.py tests_Partner_Base\TC_Partner_Copy_Quote.py tests_Partner_Base\TC_Partner_Open_Quote.py --browser_type=chromium --url=https://netapp2--uat.sandbox.lightning.force.com/ --headed --reruns 2 --junitxml=failed_report.xml

REM Check the exit code of the previous pytest run
if %ERRORLEVEL% NEQ 0 (
    REM Run only the failed tests from the current batch file
    pytest --lf utils\master_suite.py tests_Partner_Base\TC_PartnerLogin.py tests_Partner_Base\TC_Partner_Copy_Quote.py tests_Partner_Base\TC_Partner_Open_Quote.py --browser_type=chromium --url=https://netapp2--uat.sandbox.lightning.force.com/ --headed --reruns 2 --junitxml=failed_report.xml
)

REM Deactivate the virtual environment
call venv\Scripts\deactivate

REM Pause to keep the command prompt open after execution
pause
