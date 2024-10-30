# helios-activity

This README provides instructions on how to set up and run the application on both Windows and macOS.

## Installation

1. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Running Helios on Windows

To build Helios desktop app on Windows, use the following command:

```bash
pyinstaller --add-data 'model;model' --onefile -w helios.py
```

This command packages the application into a single executable file and suppresses the console window.

## Running Helios on macOS

To build Helios desktop app on macOS, use the following command:

```bash
pyinstaller --add-data 'model:model' --onefile -noconsole helios.py
```

This command packages the application into a single executable file without a console window.

After running the respective command, you will find the compiled executable in the `dist` directory. You can distribute this executable and run it on the respective operating system.

