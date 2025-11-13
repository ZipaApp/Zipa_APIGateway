import os
import requests

# Map service names to URLs using environment variables,
# defined inside docker-compose.yml
SERVICE_URLS = {
    'auth': os.environ.get('AUTH_SERVICE_URL'),
    'inventory': os.environ.get('INVENTORY_SERVICE_URL'),
    'services': os.environ.get('SERVICES_SERVICE_URL'),
    # 'buyorder': os.environ.get('BUYORDER_SERVICE_URL'),
}

def forward_request(service_name, endpoint, original_request):
    base_url = SERVICE_URLS.get(service_name)
    if not base_url:
        return {'error': f'Service URL for {service_name} not configured', 'status_code': 502}
    url = f"{base_url}/{endpoint}"
    try:
        resp = requests.request(
            method=original_request.method,
            url=url,
            headers={key: value for key, value in original_request.headers if key != 'Host'},
            data=original_request.get_data(),
            params=original_request.args
        )
        return {
            'data': resp.json() if resp.headers.get('Content-Type') == 'application/json' else resp.text,
            'status_code': resp.status_code
        }
    except Exception as e:
        return {'error': str(e), 'status_code': 500}
