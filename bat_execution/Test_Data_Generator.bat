@echo off
REM Set the working directory to the project directory
cd /d %~dp0..

REM Activate the virtual environment (if using one)
call venv\Scripts\activate

REM Run the specific test script
python utils\test_data_generator.py 

REM Deactivate the virtual environment
call venv\Scripts\deactivate

REM Pause to keep the command prompt open after execution
pause