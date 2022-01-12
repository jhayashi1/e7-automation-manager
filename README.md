# e7-automation-manager

This project was originally based on https://github.com/EmaOlay/E7-Auto-Shop-Refresh

## Dependencies

Python packages can be installed using ```pip install -r requirements.txt```

adb can be downloaded from https://developer.android.com/studio/releases/platform-tools
## Installation

Android debug bridge must be enabled for bluestacks by clicking the gear icon in the
bottom right of the screen > Advanced > Connect to Android at 127.0.0.1:####

Add adb.exe to your path using the guide below

https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0

Open the command prompt and connect to bluestacks using ```adb connect localhost:####```

Run the program with the command ```python main.py```