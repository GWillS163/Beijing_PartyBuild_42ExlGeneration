import requests
import json
from pprint import pprint

get_all_url = 'http://127.0.0.1:8000/getalllist'

res = requests.get(get_all_url)
raw_data = json.loads(res.text)

pprint(raw_data)
