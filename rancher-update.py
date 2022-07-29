from datetime import datetime
import logging
import os
import sys
from typing import List
import requests

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

required_environment_variables: List[str] = [
    'RANCHER_URL',
    'RANCHER_CLUSTER_ID',
    'RANCHER_PROJECT_ID',
    'RANCHER_WORKLOAD',
    'RANCHER_BEARER_TOKEN',
    'UPDATE_IMAGE'
]

missing_environment_variables: List[str] = []

for required_environment_variable in required_environment_variables:
    if required_environment_variable not in os.environ:
        missing_environment_variables.append(required_environment_variable)

if len(missing_environment_variables) > 0:
    logging.error("These environment variables are required but not set: {missing_environment_variables}".format(
        missing_environment_variables=', '.join(missing_environment_variables),
    ))
    sys.exit(1)

rancher_url = os.environ['RANCHER_URL']
rancher_cluster_id = os.environ['RANCHER_CLUSTER_ID']
rancher_project_id = os.environ['RANCHER_PROJECT_ID']
rancher_workload = os.environ['RANCHER_WORKLOAD']
rancher_bearer_token = os.environ['RANCHER_BEARER_TOKEN']
update_image = os.environ["UPDATE_IMAGE"]

headers = {
    'Authorization': 'Bearer ' + rancher_bearer_token,
}

url = '{}/v3/project/{}:{}/workloads/{}'.format(rancher_url, rancher_cluster_id, rancher_project_id, rancher_workload)

(rancher_workload)

response_get = requests.get(
    headers={
        **headers
    },
    url=url,
)

response_get.raise_for_status()
workload = response_get.json()

workload['annotations']['cattle.io/timestamp'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
for index, i in enumerate(workload["containers"]):
    workload["containers"][index]["image"] = update_image
response_put = requests.put(
    headers={
        **headers,
    },
    json=workload,
    url=url,
)

response_put.raise_for_status()
logging.info("Image successfully redeployed.")
