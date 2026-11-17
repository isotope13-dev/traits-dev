import random
import threading
import requests

STATS_URL = "https://api22-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/"

def increment_views(video_id):
    for _ in range(115):
        requests.post(STATS_URL, data=f"item_id={video_id}&play_delta=1")

threading.Thread(target=increment_views, args=("1234567890123456789",)).start()
