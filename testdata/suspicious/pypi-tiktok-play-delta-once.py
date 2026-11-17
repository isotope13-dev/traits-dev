import requests

STATS_URL = "https://api22-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/"
requests.post(STATS_URL, data=f"item_id={video_id}&play_delta=1")
