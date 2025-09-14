# Public-IP-Discord-Bot
A discord bot for displaying the public IP of the server it is running on

## Dependencies
### Python3
Install from
- [Python3](https://www.python.org/downloads/)
### discord.py, python-dotenv
Install using
```bash
pip install -r requirements.txt
```
## Installation / Running
Note: It is highly recommended to run this in a virtual environment such as venv, however it should still work without it
1. Install the dependencies above
2. Rename `.env.template` to `.env`
3. Enter your API key into the `.env` file
4. Run it using the specified command for your os
    - Windows: `python ip_bot.py`
    - Linux: `python3 ip_bot.py`
## Troubleshooting
### 'python' is not recognized as an internal or external command
- Ensure python is added to your PATH
    - [Using Python on Windows](https://docs.python.org/3/using/windows.html)
- Have you restarted your computer / server after installation or restarted your terminal
### discord.errors.LoginFailure: Improper token has been passed.
- Have you added your token to the `.env` file
- Have you added it to the `.env` instead of the `.env.template` file
- Is it the right token?
    - On the Discord developer portal, you can reset your token under the settings>Bot tab
### TypeError: expected token to be a str, recieved NoneType instead
- Does the `.env` file exist in the same folder you are running the script from
### ModuleNotFoundError: No module named 'discord'
- Have you installed the dependencies mentioned in `requirements.txt`
- Have you activated your virtual environment if you installed the dependencies there
### discord.errors.PrivilegedIntentsRequired
- Under the settings>Bot tab, have you enabled `MESSAGE CONTENT INTENT`