import logging
import sys
from logging import Formatter, StreamHandler

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

ugc_logger = logging.getLogger("ugc_service")
ugc_logger.addHandler(handler)
