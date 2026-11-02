# Unit fixture for a WLAN profile XML parser; no WLAN API calls.
import xml.etree.ElementTree as ET

SAMPLE = "<WLANProfile><MSM><security><sharedKey><keyMaterial>REDACTED</keyMaterial></sharedKey></security></MSM></WLANProfile>"

def profile_name(xml_text):
    return ET.fromstring(xml_text).tag
