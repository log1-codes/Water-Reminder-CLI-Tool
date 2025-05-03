# Water Reminder CLI

A modern command-line tool to help you stay hydrated by sending regular water drinking reminders.

## Features

- Customizable reminder intervals
- System tray notifications
- Configurable reminder messages
- Easy to use CLI interface
- Cross-platform support

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/water-reminder-cli.git
cd water-reminder-cli
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Basic Usage

Start the water reminder with default settings (30-minute intervals):
```bash
water-reminder
```

### Customize Reminder Interval

Set a custom reminder interval (in minutes):
```bash
water-reminder --interval 45
```

### Stop the Reminder

To stop the reminder service:
```bash
water-reminder --stop
```

### Help

View all available commands and options:
```bash
water-reminder --help
```

## Configuration

The tool uses a configuration file located at `~/.water-reminder/config.json`. You can customize:
- Reminder interval
- Custom reminder messages
- Notification settings

## Development

To set up the development environment:
```bash
pip install -r requirements.txt
```

## License

MIT License 