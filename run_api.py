from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    from server.instances import ServerInstances
    import controllers.public
    import controllers.private
    import middlewares.auth

    ServerInstances.general_api.mount(
        path="/agent", app=ServerInstances.agent_api, name="Agent API"
    )

    ServerInstances.general_api.mount(
        path="/user", app=ServerInstances.user_api, name="Agent API"
    )

    ServerInstances.general_api.start()
