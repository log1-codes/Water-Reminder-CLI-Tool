# Water Reminder CLI

A modern command-line tool to help you stay hydrated by sending regular water drinking reminders.

## Features

- Customizable reminder intervals with your name 
- System tray notifications
- Configurable reminder messages
- Easy to use CLI interface
- Cross-platform support

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/water-reminder-cli.git

```

2. Install the package:
```bash
pip install -e .
```
3. Navigate to the directory 
```bash
cd water-reminder
```
## Usage
4. How to run this ?
```bash
python cli.py start --interval 1 --name "Anurag"
```
#### 
You can set any time interval you like — for example, 1 for 1 minute or decimals like 0.1 for 6 seconds. You can also personalize it with your name, like I’ve done with “Anurag”


### Customize Reminder Interval

Set a custom reminder interval (in minutes):
```bash
water-reminder --interval 45
```


### Help

View all available commands and options:
```bash
water-reminder --help
```


## Development

To set up the development environment:
```bash
pip install -r requirements.txt
```

## License

MIT License 