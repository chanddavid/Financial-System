import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s, %(pathname)s:%(lineno)d , message: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)