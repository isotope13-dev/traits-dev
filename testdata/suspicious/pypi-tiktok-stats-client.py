import requests

STATS_URL = "https://api22-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/"
response = requests.get(STATS_URL, params={"item_id": video_id})
print(response.json())
