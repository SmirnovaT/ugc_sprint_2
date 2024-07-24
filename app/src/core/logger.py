import logging
import sys
from logging import Formatter, StreamHandler

ugc_handler = StreamHandler(stream=sys.stdout)
ugc_handler.setFormatter(
    Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

ugc_logger = logging.getLogger("ugc_service")
ugc_logger.addHandler(ugc_handler)
