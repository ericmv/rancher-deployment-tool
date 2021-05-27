import requests
import json

ACCESS_KEY = "E2B56B27974CD81EB4A9"
SECRET_KEY = "qovPL8p5ArWi2DFCyASVih2MjJY5o1ewKyebeu1Z"

API_URL = "https://rancher.eplansoftreview.com/v2-beta"
ENVIRONMENT_API_URL = "https://rancher.eplansoftreview.com/v2-beta/projects/1a7"
services_endpoint = ENVIRONMENT_API_URL + "/services/"

def upgrade_service(service_id, version):
    upgrade_endpoint = services_endpoint + service_id
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    r = requests.get(upgrade_endpoint, headers=headers, auth=(ACCESS_KEY, SECRET_KEY))

    inServiceStrategy = json.loads(r.text)['upgrade']["inServiceStrategy"]
    launchConfig = inServiceStrategy["launchConfig"]
    launchConfig["imageUuid"] = "docker:" + version
    payload = {
        'inServiceStrategy': {
            'batchSize': inServiceStrategy["batchSize"],
            'intervalMillis': inServiceStrategy["intervalMillis"],
            'startFirst': inServiceStrategy["startFirst"],
            'launchConfig': launchConfig
        }
    }

    params = {
        'action': 'upgrade'
    }
    upgrade_response = requests.post(upgrade_endpoint, headers=headers, auth=(ACCESS_KEY, SECRET_KEY), params=params, data=json.dumps(payload))
    print(upgrade_response.text)

def get_services(environment) -> list:
    services_endpoint = API_URL + "/projects/" + environment + "/services"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    r = requests.get(services_endpoint, headers=headers, auth=(ACCESS_KEY, SECRET_KEY))
    return json.loads(r.text)["data"]


def get_stacks(environment) -> list:
    stacks_endpoint = API_URL + "/projects/" + environment + "/stacks"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    r = requests.get(stacks_endpoint, headers=headers, auth=(ACCESS_KEY, SECRET_KEY))
    return json.loads(r.text)["data"]

upgrade_service("1s1071", "473702960913.dkr.ecr.us-west-2.amazonaws.com/epr:v2.6.1.369")
