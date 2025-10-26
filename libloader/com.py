import logging

from pywintypes import com_error
from win32com.client import gencache

# Set up logger
logger = logging.getLogger(__name__)


def prepare_gencache():
    logger.debug("Preparing gencache for COM object loading")
    gencache.is_readonly = False  # type: ignore[attr-defined]
    gencache.GetGeneratePath()  # type: ignore[attr-defined]


def load_com(*names):
    logger.debug("Attempting to load COM objects: %s", names)
    if gencache.is_readonly:  # type: ignore[attr-defined]
        prepare_gencache()
    result = None
    failed_names = []
    for name in names:
        try:
            logger.debug("Trying to load COM object: %s", name)
            result = gencache.EnsureDispatch(name)
            logger.info("Successfully loaded COM object: %s", name)
            break
        except com_error as e:
            logger.debug("Failed to load COM object %s: %s", name, str(e))
            failed_names.append(name)
            continue
    if result is None:
        logger.debug("Failed to load any COM objects. Tried: %s", failed_names)
        raise com_error(f"Unable to load any of the provided com objects: {failed_names}")
    return result
