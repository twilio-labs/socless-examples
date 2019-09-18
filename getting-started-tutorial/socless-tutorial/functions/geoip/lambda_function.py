import requests
from socless import socless_bootstrap

def handle_state(ip):
    r = requests.get("https://tools.keycdn.com/geo.json", params={"host": ip})
    geoip_info = r.json()['data']['geo']
    desired_results = {
        "country": geoip_info['country_name'],
        "latitude": str(geoip_info['latitude']),
        "longitude": str(geoip_info['longitude'])
        }
    return desired_results


def lambda_handler(event, context):
    return socless_bootstrap(event, context, handle_state)
