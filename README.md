# Persian Date Indicator for Ubuntu

This project provides a simple Ubuntu desktop application that displays the current Persian date in the top panel. It utilizes a Python script and a `.desktop` file for easy access and integration with the Ubuntu desktop environment.

![image](https://github.com/shalior/persian-date-indicator/assets/42506404/c56d6a6a-2aa4-43cd-876b-355a47190dfd)


## Features

- Displays the current Persian date in the top panel.
- Automatically updates the date daily.

## Requirements

- Ubuntu or any other GNOME-based Linux distribution.
- Python 3
- `gi` repository modules

## Installation

To install the Persian Date Indicator on your Ubuntu system, follow these steps:

1. **Clone the repository or download the source code**

   First, clone the repository to your local machine or download the source code. If you have `git` installed, you can clone the repository with the following command:

   ```bash
   git clone https://github.com/shalior/persian-date-indicator.git
   ```

   Alternatively, download the source code directly from the project's GitHub page.

   Dependencies:
    
   ```bash
   sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
   ```

### Manual Installation

1. **Copy the script to a suitable location**

   We recommend `/opt/persian-date` for system-wide use:

   ```bash
   sudo mkdir -p /opt/persian-date
   sudo cp *.py /opt/persian-date/
   ```

2. **Install dependencies**

   Ensure Python 3 and the necessary modules are installed:

   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-gi
   ```

3. **Create a `.desktop` file**

   Create a `.desktop` file to integrate the application with the Ubuntu desktop:

   ```plaintext
   [Desktop Entry]
   Name=Persian date
   Comment=Shows Persian date
   Exec=/usr/bin/python3 /opt/persian-date/script.py
   Terminal=false
   Type=Application
   Categories=Utility;
   ```

   Save this file as `persian-date.desktop` in `~/.local/share/applications/` for the current user or `/usr/share/applications/` for all users.

4. **Set the application to run at startup**

   Copy the `.desktop` file to the autostart directory:

   ```bash
   cp ~/.local/share/applications/persian-date.desktop ~/.config/autostart/
   ```

## Usage

After installation, the Persian Date Indicator will start automatically with your desktop session. You can see the current Persian date displayed in the top panel.

## Uninstallation

To uninstall the Persian Date Indicator, remove the script, `.desktop` file, and any startup entries you created during installation.

## Contributing

Contributions to the Persian Date Indicator are welcome! Please feel free to submit pull requests or open issues on the project's GitHub page.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
