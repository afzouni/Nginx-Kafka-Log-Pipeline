import logging
import os

logging.basicConfig(
    level=os.getenv("LOGGING_LEVEL", "ERROR"), 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)