# WarforkNotify
Lightweight application that sits in your system tray and notifies you when Warfork servers meet specified criteria such as player count and region. 

# Features
- Region-based server filtering (NA, SA, EU, AS)
- Windows toast notifications for newly active servers
- Runs in the system tray
- Simple CustomTkinter GUI

Install required libraries with 
```bash
pip install customtkinter pystray pillow requests beautifulsoup4 winotify
```

# Usage
1. Start the application by running gui.py
2. Select your desired settings
3. Press Start Notifier
4. Right-click the tray icon to quit or re-open the settings menu
