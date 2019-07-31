import os
import logging
from datetime import datetime


logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler = logging.FileHandler(os.getcwd() + 
f'/server/log/{datetime.today().strftime("%Y%m%d")}_server_main.log')

handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)
