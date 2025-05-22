# Google Autocomplete CLI Tool

A command-line interface tool that fetches and displays Google search autocomplete suggestions for user-provided keywords. Supports multiple languages including RTL (Right-to-Left) languages like Hebrew.

## Features

- Interactive command-line interface
- Multi-language support (English, Hebrew)
- Proper RTL text handling
- Real-time Google autocomplete suggestions
- Easy language switching
- Configurable language settings

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/autosuggest.git
cd autosuggest
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python autosuggest.py
```

### Commands
- Type your search keyword to get suggestions
- Type 'lang' to change language
- Type 'quit', 'exit', or 'q' to exit
- Press Ctrl+C to exit anytime

### Language Support
- English (en)
- Hebrew (he) - with proper RTL support

## Configuration

Language settings are stored in `language_config.json`. You can modify this file to add more languages or change existing settings.

## Requirements

- Python 3.6 or higher
- Required packages (see requirements.txt):
  - requests
  - arabic-reshaper
  - python-bidi

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Suggest API
- arabic-reshaper and python-bidi libraries for RTL text support 