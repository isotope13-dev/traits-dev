import litellm
from litellm.integrations.custom_logger import CustomLogger
class Adapter(CustomLogger):
    def log_post_api_call(self, kwargs, response):
        return kwargs.get("litellm_call_id"), kwargs.get("litellm_params")
