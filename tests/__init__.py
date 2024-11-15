from dotenv import load_dotenv
import logging
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()

os.environ["DATABASE_CURRENT_NAME"] = "tests"

import controllers.http.private
import controllers.http.private
import controllers.websocket
import middlewares.auth
