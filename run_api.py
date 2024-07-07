from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    from server.instances import ServerInstances
    import controllers.public
    import controllers.private
    import middlewares.auth
    from utils.constants import AGENT_ENDPOINT_NAME, USER_ENDPOINT_NAME

    ServerInstances.general_api.mount(
        path=AGENT_ENDPOINT_NAME, app=ServerInstances.agent_api, name="Agent API"
    )

    ServerInstances.general_api.mount(
        path=USER_ENDPOINT_NAME, app=ServerInstances.user_api, name="Agent API"
    )

    ServerInstances.general_api.start()
