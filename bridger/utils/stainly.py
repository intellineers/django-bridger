import requests
from django.conf import settings
import pandas as pd

def fetch_df(endpoint):
    url = f"{settings.STAINLY_API_BASE_ENDPOINT_URL}{endpoint}"
    headers = {
        'user-agent': 'workbench',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if settings.STAINLY_TOKEN:
        headers["Authorization"] = f'Token {settings.STAINLY_TOKEN}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == requests.codes.ok:
            r_json = response.json()
            if r_json.get("results", None):
                data = pd.json_normalize(r_json['results'])
                return data
    except requests.exceptions.ConnectionError as e:
        pass
    return pd.DataFrame()