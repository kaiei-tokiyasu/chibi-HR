# Chibi-hr

Chibi-HR is an interactive menu-driven CLI application designed to process HR Excel files such as monthly absence reports and employee productivity targets. It summarizes the data into structured outputs to support reporting and decision-making.

---

## Setup

### Prerequisites

- Python 3.7 or higher installed on your system.

---

### Clone the repo using github desktop or using CLI:

```console
    git clone https://github.com/kaiei-tokiyasu/chibi-HR.git
    cd chibi-HR
```

### Create and activate a virtual environment

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
.\venv\Scripts\activate.bat

# On macOS/Linux:
source venv/bin/activate
```

### run and test

```
    python main.py
```

### On first run

- A default config.json file will be generated.
- Input/output folders will be created (input/, output/).
- If config.json is deleted or corrupted, it will be regenerated automatically.

### Build using pyinstaller

## For the first build:

```
    pyinstaller --onefile --name chibi-HR main.py
```

## for subsequent builds:

```
    pyinstaller chibi-HR.spec
```

---

## Developer Customization

For details on customizing processing parameters, see [CONTRIBUTING.md](CONTRIBUTING.md#configuration-and-customization).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## TODO List

- [ ] add config for starts row and columns to get.
- [ ] build excel example template
- [ ] add more config
