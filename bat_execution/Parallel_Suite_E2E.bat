@echo off
REM Set the working directory to the project directory
cd /d %~dp0..

REM Activate the virtual environment (if using one)
call venv\Scripts\activate

REM Run the specific Pytest test script
pytest -n 5 tests_SFDC_Base\TC_Login.py tests_SFDC_Base\TC_CreateOpportunity.py tests_CPQ_Base\TC_API_Validation.py tests_CPQ_Base\TC_Copy_Quote.py tests_CPQ_Base\TC_Open_Quote.py tests_CPQ_Base\TC_FAS_AFF_Cluster_Config.py tests_ERP_FTR\E2E_UAT_003_Part_1.py tests_ERP_FTR\E2E_UAT_003_Part_2.py tests_ERP_FTR\E2E_UAT_017.py tests_ERP_FTR\E2E_UAT_018.py tests_ERP_FTR\E2E_UAT_022_Part_1.py tests_ERP_FTR\E2E_UAT_022_Part_2.py tests_ERP_FTR\E2E_UAT_024.py tests_ERP_FTR\E2E_UAT_025_Part_1.py tests_ERP_FTR\E2E_UAT_025_Part_2.py tests_ERP_FTR\E2E_UAT_026_Part_1.py tests_ERP_FTR\E2E_UAT_026_Part_2.py tests_ERP_FTR\E2E_UAT_038.py tests_ERP_FTR\E2E_UAT_051.py tests_ERP_FTR\TC_FAS_AFF_ASA_AFX_Multiple_Cluster_Config_001.py --browser_type=chromium --url=https://netapp2--uat.sandbox.lightning.force.com/ --headed --reruns 2 --junitxml=failed_report.xml

REM Check the exit code of the previous pytest run
if %ERRORLEVEL% NEQ 0 (
    REM Run only the failed tests from the current batch file
    pytest -n 5 --lf tests_SFDC_Base\TC_Login.py tests_SFDC_Base\TC_CreateOpportunity.py tests_CPQ_Base\TC_API_Validation.py tests_CPQ_Base\TC_Copy_Quote.py tests_CPQ_Base\TC_Open_Quote.py tests_CPQ_Base\TC_FAS_AFF_Cluster_Config.py tests_ERP_FTR\E2E_UAT_003_Part_1.py tests_ERP_FTR\E2E_UAT_003_Part_2.py tests_ERP_FTR\E2E_UAT_017.py tests_ERP_FTR\E2E_UAT_018.py tests_ERP_FTR\E2E_UAT_022_Part_1.py tests_ERP_FTR\E2E_UAT_022_Part_2.py tests_ERP_FTR\E2E_UAT_024.py tests_ERP_FTR\E2E_UAT_025_Part_1.py tests_ERP_FTR\E2E_UAT_025_Part_2.py tests_ERP_FTR\E2E_UAT_026_Part_1.py tests_ERP_FTR\E2E_UAT_026_Part_2.py tests_ERP_FTR\E2E_UAT_038.py tests_ERP_FTR\E2E_UAT_051.py tests_ERP_FTR\TC_FAS_AFF_ASA_AFX_Multiple_Cluster_Config_001.py --browser_type=chromium --url=https://netapp2--uat.sandbox.lightning.force.com/ --headed --reruns 2 --junitxml=failed_report.xml
)

REM Deactivate the virtual environment 
call venv\Scripts\deactivate 

REM Pause to keep the command prompt open after execution
pause