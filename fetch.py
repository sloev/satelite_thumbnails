import requests
import os
import re
import shutil
import time
import json

from_date = "1990-05-14T18:33:31.475Z"
to_date = "2019-08-14T18:33:31.475Z"
copenhagen = {
    "filter": {
        "type": "AndFilter",
        "config": [
            {
                "type": "GeometryFilter",
                "field_name": "geometry",
                "config": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [12.576213888823986, 55.66543883113067],
                            [12.61807981878519, 55.66543883113067],
                            [12.61807981878519, 55.68490393344112],
                            [12.576213888823986, 55.68490393344112],
                            [12.576213888823986, 55.66543883113067],
                        ]
                    ],
                },
            },
            {
                "type": "OrFilter",
                "config": [
                    {
                        "type": "AndFilter",
                        "config": [
                            {
                                "type": "StringInFilter",
                                "field_name": "item_type",
                                "config": ["PSScene4Band"],
                            }
                        ],
                    },
                    {
                        "type": "AndFilter",
                        "config": [
                            {
                                "type": "StringInFilter",
                                "field_name": "item_type",
                                "config": ["REOrthoTile"],
                            }
                        ],
                    },
                    {
                        "type": "AndFilter",
                        "config": [
                            {
                                "type": "StringInFilter",
                                "field_name": "item_type",
                                "config": ["SkySatCollect"],
                            }
                        ],
                    },
                ],
            },
            {
                "type": "OrFilter",
                "config": [
                    {
                        "type": "DateRangeFilter",
                        "field_name": "acquired",
                        "config": {"gte": from_date, "lte": to_date},
                    }
                ],
            },
        ],
    },
    "item_types": ["PSScene4Band", "REOrthoTile", "SkySatCollect"],
}
api_key = os.environ["API_KEY"]

session = requests.Session()
session.auth = (api_key, "")

sleep_period = 0.1
def post(url, data):
    response = session.post(f"{url}", json=data)
    time.sleep(sleep_period)
    return response


def get(url):
    response = session.get(f"{url}")
    time.sleep(sleep_period)
    return response


def download_file(url, folder):
    local_filename = folder + url.rsplit("/thumb", 1)[0].rsplit("/", 1)[1] + ".png"
    if not os.path.isfile(local_filename):
        print(f"fetching {url}")
        with session.get(f"{url}?api_key={api_key}", stream=True) as r:
            with open(local_filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        time.sleep(sleep_period)
    else:
        print(f"skipping {url} since downloaded")
    return local_filename


next_url = "https://api.planet.com/data/v1/quick-search"
response = post(next_url, copenhagen)

page = 0
today = time.time()
while True:
    print(f"processing page {page}")
    response_text = response.text
    with open(f"./json_files/{today}_{page}.json", "w") as f:
        f.write(json.dumps(response.json(), indent=2))
    print(f"query: {response.status_code}")
    for match in re.finditer(
        "/thumb", response_text
    ):
        url = 'http' + response_text[:match.end() :].rsplit('http', 1)[1]
        download_file(url, "./images/")
    next_url = response.json().get("_links", {}).get("_next", None)
    print(f"next: {next_url}")
    if not next_url:
        break
    response = get(next_url)
    page += 1
