import requests
import json
from urllib.parse import parse_qs
import base64


url = "https://academia.srmuniv.ac.in/accounts/signin.ac"

headers = {'Origin': 'https://academia.srmuniv.ac.in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36' }




def getToken(username, password):
    payload = {'username': username,
               'password': password,
               'client_portal': 'true',
               'portal': '10002227248',
               'servicename': 'ZohoCreator',
               'serviceurl': 'https://academia.srmuniv.ac.in/',
               'is_ajax': 'true',
               'grant_type': 'password',
               'service_language': 'en'}

    r = requests.post(url, data=payload, headers=headers)
    json_data = json.loads(r.text)

    if "error" in json_data:
        error_m = json_data['error']['msg']
        json_o = {"status":"error", "msg":error_m}
        return json.dumps(json_o)
    else:
        params = parse_qs(json_data['data']['token_params'])
        params['state'] = 'https://academia.srmuniv.ac.in/'
        r = requests.get(json_data['data']['oauthorize_uri'], data=params, headers=headers)
        token = json.dumps(r.history[0].cookies.get_dict())
        token = str(base64.encodestring(str.encode(token)),'utf-8')


        json_o = {"status":"success", "token": token}
        return json.dumps(json_o)

