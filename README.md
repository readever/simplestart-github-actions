# SimpleStart

A Python web framework for building web applications with Element UI.

## Installation

```bash
pip install simplestart
```

## Usage

```python
import simplestart as ss

# Your code here
```

## Building from Source

This package uses Cython to compile Python code to C for better performance.

### Prerequisites

- Python 3.10+
- Cython
- C compiler

### Build

```bash
pip install build
python -m build --wheel
```

## GitHub Actions

This project uses GitHub Actions to automatically build wheels for multiple platforms:
- Linux (Ubuntu)
- macOS
- Windows

Supported Python versions: 3.10, 3.11, 3.12, 3.13

## License

MIT