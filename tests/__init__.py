from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

import controllers.http.private
import controllers.http.private
import controllers.websocket
import middlewares.auth
