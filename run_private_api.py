from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    from server.instances import ServerInstances
    import controllers.private
    import middlewares.auth

    ServerInstances.api.start()
