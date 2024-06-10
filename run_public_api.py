from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    from server.instances import ServerInstances
    import controllers.public

    ServerInstances.api.start()
