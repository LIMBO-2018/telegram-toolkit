# Telegram Toolkit

A professional tool for Telegram group management, member scraping, and messaging.

## Features

- **Member Scraping**: Extract members from any Telegram group you're part of
- **Group Management**: Add members to your groups from CSV files
- **Messaging**: Send personalized messages to Telegram users
- **CSV Utilities**: Merge and manage member lists
- **User-Friendly Interface**: Beautiful CLI with progress indicators and color-coded output
- **Privacy-Aware**: All data stays on your machine, no third-party servers involved

## Installation

### From PyPI (Recommended)

```bash
pip install telegram-toolkit
```

### From Source

```bash
git clone https://LIMBO-2018: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@github.com/LIMBO-2018/telegram-toolkit.git
cd telegram-toolkit
pip install -e .
```

## Quick Start

1. **Setup your API credentials**:

```bash
telegram-toolkit setup --config
```

You'll need to create an application on [my.telegram.org/apps](https://my.telegram.org/apps) to get your API ID and hash.

2. **Scrape members from a group**:

```bash
telegram-toolkit scrape --output members.csv
```

3. **Add members to a group**:

```bash
telegram-toolkit add members.csv --delay 15
```

4. **Send messages to users**:

```bash
telegram-toolkit send members.csv --message message.txt --delay 30
```

## Usage

### Setup and Configuration

```bash
# Configure API credentials
telegram-toolkit setup --config

# Install dependencies
telegram-toolkit setup --install

# Update the tool
telegram-toolkit setup --update
```

### Member Scraping

```bash
# Basic scraping
telegram-toolkit scrape

# Specify output file
telegram-toolkit scrape --output my_members.csv

# Only scrape active users (active in the last week)
telegram-toolkit scrape --active

# Limit the number of members to scrape
telegram-toolkit scrape --limit 100
```

### Adding Members to Groups

```bash
# Basic usage
telegram-toolkit add members.csv

# Specify delay between adding members (in seconds)
telegram-toolkit add members.csv --delay 15

# Limit the number of members to add
telegram-toolkit add members.csv --limit 50
```

### Sending Messages

```bash
# Send a message to all members in the CSV
telegram-toolkit send members.csv

# Use a message from a file
telegram-toolkit send members.csv --message message.txt

# Specify delay between messages (in seconds)
telegram-toolkit send members.csv --delay 45

# Limit the number of messages to send
telegram-toolkit send members.csv --limit 30
```

### CSV Utilities

```bash
# Merge two CSV files
telegram-toolkit merge file1.csv file2.csv --output merged.csv
```

## Message Formatting

When sending messages, you can use the following placeholders:

- `{name}`: Will be replaced with the user's name

Example message:

```
Hello {name},

Thank you for being part of our community!

Best regards,
Your Name
```

## Safety and Ethics

- Always respect Telegram's Terms of Service
- Don't use this tool for spam or harassment
- Be mindful of rate limits to avoid getting your account limited
- Always get proper consent before adding users to groups

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
