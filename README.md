# Libloader

Libloader is a cross-platform Python library that simplifies loading shared libraries on macOS, Windows, and Linux. It handles platform-specific differences automatically, making your code more portable.

It also provides a COM module (`libloader.com`), making it easier to load COM DLLs on Windows.

## Installation

```bash
pip install libloader
```

## Usage

### Loading Shared Libraries

```python
from libloader import load_library

# Load a library with default paths
my_lib = load_library("mylibrary")

# Load a library with custom paths for 32-bit and 64-bit versions
my_lib = load_library("mylibrary", x86_path="./lib/x86", x64_path="./lib/x64")

# Load a library with ARM64 support (M1+ Macs, ARM servers)
my_lib = load_library("mylibrary", x64_path="./lib/x64", arm64_path="./lib/arm64")

# Call a function from the library
result = my_lib.some_function(arg1, arg2)
```

### Working with COM Objects (Windows)

```python
from libloader.com import load_com

# Load a COM object
excel = load_com("Excel.Application")

# Try multiple COM objects until one succeeds
speech = load_com("SAPI.SpVoice", "SpeechLib.SpVoice")
```

## API Reference

### libloader

* `load_library(library, x86_path=".", x64_path=".", arm64_path=None, *args, **kwargs)`: Load a library with the given name. If `arm64_path` is not specified on ARM64 systems, falls back to `x64_path`.
* `find_library_path(libname, x86_path=".", x64_path=".", arm64_path=None)`: Finds the path of the given library.
* `get_functype()`: Returns the ctypes functype for the current platform.
* `get_library_extension()`: Get the extension of the library for your current platform.
* `_do_load(file, *args, **kwargs)`: Attempts to actually load the library. Used internally by load_library.

### libloader.com

* `load_com(*names)`: Load a COM object. If you pass multiple names, it will try each one until one works.
* `prepare_gencache()`: Prepare the gencache for COM. Called automatically by load_com().

## Platform Support

Libloader automatically handles the differences between platforms:

* Windows: `.dll` files
* macOS: `.dylib` files
* Linux: `.so` files

### Architecture Support

Libloader automatically detects the system architecture and loads the appropriate library:

* **x86** (32-bit): Uses `x86_path`
* **x86_64/AMD64** (64-bit Intel/AMD): Uses `x64_path`
* **ARM64/aarch64** (M1+ Macs, ARM servers): Uses `arm64_path` if specified, otherwise falls back to `x64_path`

This means existing code works on Apple Silicon Macs without modification, while allowing you to provide architecture-specific binaries when needed.

## License

See the LICENSE file for details.
