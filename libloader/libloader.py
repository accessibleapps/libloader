import ctypes
import logging
import os
import platform

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


def load_library(library, x86_path=".", x64_path=".", *args, **kwargs):
    logger.debug("Attempting to load library: %s", library)
    logger.debug("x86_path: %s, x64_path: %s", os.path.abspath(x86_path), os.path.abspath(x64_path))

    lib = find_library_path(library, x86_path=x86_path, x64_path=x64_path)
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


def find_library_path(libname, x86_path=".", x64_path="."):
    system = platform.system()
    prefix = TYPES[system]["prefix"]
    libname_with_prefix = f"{prefix}{libname}"
    logger.debug("Library name with prefix: %s", libname_with_prefix)

    arch = platform.architecture()[0]
    logger.debug("Detected architecture: %s", arch)

    if arch == "64bit":
        path = os.path.join(x64_path, libname_with_prefix)
        logger.debug("Using 64-bit path: %s", x64_path)
    else:
        path = os.path.join(x86_path, libname_with_prefix)
        logger.debug("Using 32-bit path: %s", x86_path)

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
