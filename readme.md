# Chibi-hr

A cli tool for HR, employee performance in absence and target

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

### Build using pyinstaller

## For the first build:

```
    pyinstaller --onefile --version-file=version.txt --name chibi-HR main.py
```

## for subsequent builds:

```
    pyinstaller chibi-HR.spec
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## TODO List

- [ ] add config for starts row and columns to get.
- [ ] build excel example template
- [ ] add more config
