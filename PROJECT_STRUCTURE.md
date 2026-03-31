# Project Structure Overview

## Complete Directory Tree

```
MarketRisk/
│
├── src/
│   └── marketrisk/                          # Main Python package
│       ├── __init__.py                      # Package initialization
│       ├── calculator.py                    # Core option pricing calculator
│       ├── cli.py                           # Command-line interface
│       └── utils.py                         # Utility functions
│
├── tests/
│   ├── __init__.py                          # Tests package
│   ├── test_calculator.py                   # Unit tests (15 tests)
│   └── fixtures/                            # Test data (optional)
│
├── docs/
│   ├── INSTALL.md                           # Installation instructions
│   ├── USAGE.md                             # Usage guide with examples
│   └── API.md                               # API documentation (optional)
│
├── .gitignore                               # Git ignore rules
├── setup.py                                 # Package setup (setuptools)
├── pyproject.toml                           # Modern Python project config
├── requirements.txt                         # Production dependencies
├── requirements-dev.txt                     # Development dependencies
├── README.md                                # Project documentation
├── CHANGELOG.md                             # Version history
│
└── __pycache__/                             # Python cache directory

```

## Directory Purposes

### `src/marketrisk/` - Source Code
Contains the main Python package code.

**Files:**
- `__init__.py` - Makes directory a package, exports public API
- `calculator.py` - Main `OptionsGreeksCalculator` class with all methods
- `cli.py` - Command-line interface for interactive use
- `utils.py` - Validation and utility functions

**Access:**
```python
from marketrisk.calculator import OptionsGreeksCalculator
from marketrisk.cli import main
from marketrisk.utils import parse_date
```

### `tests/` - Unit Tests
Contains all test files following pytest/unittest conventions.

**Files:**
- `__init__.py` - Makes directory a package
- `test_calculator.py` - 15 comprehensive unit tests
- `fixtures/` - Test data and fixtures (optional)

**Run:**
```bash
python -m unittest discover -s tests -p "test_*.py" -v
pytest tests/ -v
```

### `docs/` - Documentation
Contains project documentation.

**Files:**
- `INSTALL.md` - Installation and setup instructions
- `USAGE.md` - Usage guide with code examples
- `API.md` - Detailed API reference (optional)

### Root Level - Configuration
Standard Python project configuration files.

**Essential:**
- `setup.py` - Setuptools configuration for package distribution
- `pyproject.toml` - Modern Python project configuration (PEP 517/518)
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development tools and test dependencies
- `.gitignore` - Git ignore patterns
- `README.md` - Main project documentation
- `CHANGELOG.md` - Version and change history

## File Purposes Explained

### `src/` vs Root Level
The `src/` layout is recommended because:
1. **Isolation**: Source code is separate from configuration
2. **Safety**: Prevents accidentally importing uninstalled code
3. **Scalability**: Easy to add multiple packages
4. **Standards**: Follows PEP 420 and PEP 517

### `tests/` Directory
- Separated from source code (cleaner structure)
- Follows unittest/pytest discovery conventions
- Can be excluded from package installation
- Easy to run: `python -m unittest discover`

### Configuration Hierarchy
```
pyproject.toml          ← Modern: Replaces old setup.cfg
    ↓ (uses)
setup.py               ← Setuptools configuration
    ↓ (reads)
requirements*.txt      ← Dependency versions
```

## Package Installation

### After Structure
The package can now be:

1. **Installed in editable mode** (development):
   ```bash
   pip install -e .
   ```
   Creates: `src/marketrisk.egg-info/`

2. **Installed normally** (production):
   ```bash
   pip install .
   ```

3. **Installed from PyPI** (future):
   ```bash
   pip install marketrisk
   ```

## Import Statements

```python
from marketrisk.calculator import OptionsGreeksCalculator
```

## Common Operations

### Install Package
```bash
pip install -e .                    # Editable mode
pip install -r requirements-dev.txt # Dev dependencies
```

### Run Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
pytest tests/ -v
```

### Run CLI
```bash
python -m marketrisk.cli
marketrisk                          # If installed as package
```

### Code Quality
```bash
black src/ tests/              # Format code
flake8 src/ tests/             # Lint
mypy src/                      # Type check
pytest tests/ --cov            # Coverage
```

### Generate Documentation
```bash
sphinx-build -b html docs/ docs/_build/
```

## Legacy Files (Optional Cleanup)

These old files are still in the root but superseded:

```
OLD                              →  NEW
─────────────────────────────────────────────────────────
OptionsGreeksCalculator.py       →  src/marketrisk/calculator.py
OptionsGreeksCalculatorTest.py   →  tests/test_calculator.py
run_tests.py                     →  unittest discovery
INSTALL.md                       →  docs/INSTALL.md
```

You can delete them when comfortable with the new structure.

## Package Metadata

### Module Hierarchy
```
marketrisk/                     (Package)
├── calculator                  (Module) → OptionsGreeksCalculator class
├── cli                         (Module) → main() function
└── utils                       (Module) → Utility functions
```

### Public API
```python
# Main imports
from marketrisk import OptionsGreeksCalculator
from marketrisk.calculator import OptionsGreeksCalculator
from marketrisk.cli import main
```

### Entry Points
```
Console Command: marketrisk
  Points to: marketrisk.cli:main()
```

## Development Workflow

```
Clone/Download
    ↓
Create venv: python -m venv venv
    ↓
Activate: venv\Scripts\activate
    ↓
Install: pip install -e . -r requirements-dev.txt
    ↓
Code/Test: Make changes, run tests
    ↓
Format: black src/ tests/
    ↓
Lint: flake8 src/ tests/
    ↓
Commit: git add . && git commit
```

## Best Practices Applied

✅ **Package Structure**
- Source code in `src/`
- Tests in `tests/`
- Docs in `docs/`
- Configuration at root

✅ **Configuration**
- `pyproject.toml` for tool settings
- `setup.py` for package metadata
- Separate requirements files

✅ **Testing**
- Unittest/pytest compatible
- Automatic discovery
- Proper imports

✅ **Documentation**
- README for overview
- INSTALL guide
- USAGE guide with examples
- Docstrings in code

✅ **Version Control**
- Comprehensive `.gitignore`
- No unnecessary files tracked

## Verification Checklist

✅ Package installs: `pip install -e .`
✅ Tests pass: `python -m unittest discover`
✅ CLI works: `python -m marketrisk.cli`
✅ Imports work: `from marketrisk import ...`
✅ Documentation: README, INSTALL, USAGE
✅ Type hints: Present in all functions
✅ Docstrings: Comprehensive documentation

## Next Level Improvements (Optional)

These can be added later:

- [ ] GitHub Actions for CI/CD
- [ ] Coverage reporting
- [ ] Type stub files (.pyi)
- [ ] Sphinx documentation
- [ ] Pre-commit hooks
- [ ] PyPI publishing
- [ ] Docker support
- [ ] API documentation generation

---

**Status**: ✅ Complete restructuring following Python industry best practices!

