@echo off
echo Telegram Toolkit Installer
echo ==============================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.6 or higher.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment. Please install venv package.
    exit /b 1
)
echo Virtual environment created.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo Virtual environment activated.

REM Install the package
echo Installing Telegram Toolkit...
pip install -e .
if %ERRORLEVEL% neq 0 (
    echo Failed to install Telegram Toolkit.
    exit /b 1
)
echo Telegram Toolkit installed successfully.

REM Setup configuration
echo Would you like to configure Telegram API credentials now? (y/n)
set /p setup_now=

if /i "%setup_now%"=="y" (
    telegram-toolkit setup --config
)

echo.
echo Installation completed!
echo.
echo To use Telegram Toolkit, activate the virtual environment:
echo call venv\Scripts\activate
echo.
echo Then run commands like:
echo telegram-toolkit --help
echo.
echo Enjoy using Telegram Toolkit!
