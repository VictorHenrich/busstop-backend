from server.instances import ServerInstances
from utils.responses import ResponseSuccess


@ServerInstances.api.get("/")
def index() -> ResponseSuccess:
    return ResponseSuccess("APPLICATION RUNNING!")
