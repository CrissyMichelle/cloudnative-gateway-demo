import time
from locust import HttpUser, task, events
from coolname import generate
import json

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--auth-tok", type=str, env_var="authentication", default="", help="Authentication")

class QuickstartUser(HttpUser):

    timeout = 100

    @task
    def hello_world(self):
        assert len(self.environment.parsed_options.auth_tok) > 0
        self.response_dict = json.loads(self.environment.parsed_options.auth_tok)
        headers = {
            'Authorization': f'BEARER {self.response_dict["access"]}'
        }

        params = {'message': 'hi ' + ' '.join(generate(4))}
        response = self.client.get('/v1/llm', headers=headers, params=params)
        print(response.text)

