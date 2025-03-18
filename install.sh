#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Telegram Toolkit Installer${NC}"
echo "=============================="
echo

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}Python 3 is not installed. Please install Python 3.6 or higher.${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create virtual environment. Please install venv package.${NC}"
    exit 1
fi
echo -e "${GREEN}Virtual environment created.${NC}"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}Virtual environment activated.${NC}"

# Install the package
echo -e "${YELLOW}Installing Telegram Toolkit...${NC}"
pip install -e .
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install Telegram Toolkit.${NC}"
    exit 1
fi
echo -e "${GREEN}Telegram Toolkit installed successfully.${NC}"

# Setup configuration
echo -e "${YELLOW}Would you like to configure Telegram API credentials now? (y/n)${NC}"
read -r setup_now

if [[ $setup_now == "y" || $setup_now == "Y" ]]; then
    telegram-toolkit setup --config
fi

echo
echo -e "${GREEN}Installation completed!${NC}"
echo
echo -e "To use Telegram Toolkit, activate the virtual environment:"
echo -e "${YELLOW}source venv/bin/activate${NC}"
echo
echo -e "Then run commands like:"
echo -e "${YELLOW}telegram-toolkit --help${NC}"
echo
echo -e "Enjoy using Telegram Toolkit!"
