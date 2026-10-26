"""CLI for one-time, authorized widget inventory; credentials stay in process memory."""
import argparse
import os
from urllib.parse import urlsplit

import httpx


def main(argv=None):
    parser = argparse.ArgumentParser(prog='widgets-discover')
    parser.add_argument('--company-id', required=True, type=int)
    args = parser.parse_args(argv)
    user_token = os.getenv('WIDGETS_USER_JWT', '')
    api_token = os.getenv('WIDGETS_API_TOKEN', '')
    if not user_token or not api_token:
        parser.error('WIDGETS_USER_JWT and WIDGETS_API_TOKEN environment variables are required')
    parsed = urlsplit('https://api.widgets.example/api/v1')
    if parsed.username or not parsed.hostname or parsed.scheme != 'https':
        parser.error('--api-url must be HTTPS')
    response = httpx.post(
        'https://api.widgets.example/api/v1/widgets/discovery/',
        json={'company_id': args.company_id, 'token': api_token},
        headers={'Authorization': f'Bearer {user_token}'}, timeout=30,
    )
    print(response.text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
