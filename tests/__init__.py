from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

import controllers.public
import controllers.private
import middlewares.auth
