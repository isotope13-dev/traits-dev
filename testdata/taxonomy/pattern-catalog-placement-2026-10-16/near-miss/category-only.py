categories: [api, secret]
rules:
  - name: slack-token
    pattern: |
      xoxp-[0-9-]+-[a-f0-9]{20,}
