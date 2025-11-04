import ctypes
import logging
import os
import platform
import struct

# Set up logger
logger = logging.getLogger(__name__)


TYPES = {
    "Linux": {
        "loader": ctypes.CDLL,
        "functype": ctypes.CFUNCTYPE,
        "prefix": "lib",
        "extension": ".so",
    },
    "Darwin": {
        "loader": ctypes.CDLL,
        "functype": ctypes.CFUNCTYPE,
        "prefix": "lib",
        "extension": ".dylib",
    },
}
if platform.system() == "Windows":
    TYPES["Windows"] = {
        "loader": ctypes.WinDLL,
        "functype": ctypes.WINFUNCTYPE,
        "prefix": "",
        "extension": ".dll",
    }


class LibraryLoadError(OSError):
    pass


def load_library(library, x86_path=".", x64_path=".", arm64_path=None, *args, **kwargs):
    logger.debug("Attempting to load library: %s", library)
    logger.debug(
        "x86_path: %s, x64_path: %s, arm64_path: %s",
        os.path.abspath(x86_path),
        os.path.abspath(x64_path),
        os.path.abspath(arm64_path) if arm64_path is not None else None,
    )

    lib = find_library_path(library, x86_path=x86_path, x64_path=x64_path, arm64_path=arm64_path)
    logger.debug("Resolved library path: %s", lib)

    loaded = _do_load(lib, *args, **kwargs)
    if loaded is not None:
        logger.info("Successfully loaded library: %s", os.path.basename(lib))
        return loaded

    logger.error("Failed to load library: %s", lib)
    raise LibraryLoadError(f"unable to load {library!r}. Provided library path: {lib!r}")


def _do_load(file, *args, **kwargs):
    system = platform.system()
    logger.debug("Using loader for system: %s", system)
    loader = TYPES[system]["loader"]
    try:
        return loader(file, *args, **kwargs)
    except Exception as e:
        logger.error("Error loading %s: %s", file, str(e))
        return None


def find_library_path(libname, x86_path=".", x64_path=".", arm64_path=None):
    system = platform.system()
    prefix = TYPES[system]["prefix"]
    libname_with_prefix = f"{prefix}{libname}"
    logger.debug("Library name with prefix: %s", libname_with_prefix)

    # Detect Python interpreter bitness (not OS architecture)
    pointer_bits = struct.calcsize("P") * 8
    logger.debug("Detected Python interpreter bitness: %d-bit", pointer_bits)

    # Get machine architecture for ARM64 detection
    machine = platform.machine().lower()
    logger.debug("Detected machine architecture: %s", machine)

    # Map architecture to the appropriate path
    if machine in ("arm64", "aarch64"):
        # ARM64 architecture (M1+ Macs, ARM servers, modern Raspberry Pi)
        if arm64_path is None:
            logger.debug("ARM64 detected, arm64_path not specified, falling back to x64_path")
            path = os.path.join(x64_path, libname_with_prefix)
            logger.debug("Using fallback x64 path: %s", x64_path)
        else:
            path = os.path.join(arm64_path, libname_with_prefix)
            logger.debug("Using ARM64 path: %s", arm64_path)
    elif pointer_bits == 64:
        # 64-bit Python interpreter (x86_64)
        path = os.path.join(x64_path, libname_with_prefix)
        logger.debug("Using x64 path (64-bit Python): %s", x64_path)
    else:
        # 32-bit Python interpreter (x86)
        path = os.path.join(x86_path, libname_with_prefix)
        logger.debug("Using x86 path (%d-bit Python): %s", pointer_bits, x86_path)

    ext = get_library_extension()
    logger.debug("Using library extension: %s", ext)

    path = f"{path}{ext}"
    abs_path = os.path.abspath(path)

    logger.debug("Path exists: %s", os.path.exists(abs_path))

    return abs_path


def get_functype():
    return TYPES[platform.system()]["functype"]


def get_library_extension():
    return TYPES[platform.system()]["extension"]
