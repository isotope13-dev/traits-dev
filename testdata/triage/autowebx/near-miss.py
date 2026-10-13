"""Install dependencies with `pip install requests`."""
class Parser:
    def extract(self, headers):
        return headers
    def parse(self):
        self.extract({'Content-Type': 'text/plain'})
url = '/delete'
clientKey = 'value'
websiteURL = 'https://example.com'
taskId = 1
result_endpoint = 'https://solver.example/getTaskResult'
task_type = 'RecaptchaV2TaskProxyless'
