from dotenv import load_dotenv
import logging


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    from server.instances import ServerInstances
    import controllers.http.public
    import controllers.http.private
    import controllers.websocket
    import middlewares.auth
    from utils.config import AGENT_ENDPOINT_NAME, USER_ENDPOINT_NAME

    ServerInstances.general_api.mount(
        path=AGENT_ENDPOINT_NAME, app=ServerInstances.agent_api, name="Agent API"
    )

    ServerInstances.general_api.mount(
        path=USER_ENDPOINT_NAME, app=ServerInstances.user_api, name="Agent API"
    )

    ServerInstances.general_api.start()
