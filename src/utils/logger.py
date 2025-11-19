import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def log(level: str, message: str, data: dict = None):
    """Custom logger"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
    }
    if data:
        log_data["data"] = data
    
    if level == "ERROR":
        logger.error(log_data)
    elif level == "WARN":
        logger.warning(log_data)
    elif level == "DEBUG":
        logger.debug(log_data)
    else:
        logger.info(log_data)

