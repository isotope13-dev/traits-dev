import locale
import signal
class FileShares:
    def unshare(self, name):
        return {"last_result": name}
shares = FileShares()
result = shares.unshare("public-document")
locale_name = locale.getlocale()
russian_locale = "ru_RU"
status = {"network_source": "ip/ifconfig + iw/nmcli", "body_b64": ""}
signals = {name: getattr(signal, "SIG" + name) for name in ("TERM", "KILL", "QUIT")}
application_names = ("openvpn",)
