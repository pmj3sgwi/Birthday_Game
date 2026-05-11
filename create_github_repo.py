import urllib.request
import json

url = 'https://api.github.com/user/repos'
data = json.dumps({'name': 'Game-BTTF', 'private': True}).encode('utf-8')

req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Accept', 'application/vnd.github+json')
req.add_header('Content-Type', 'application/json')

try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    print('SUCCESS')
    print('Clone URL:', result.get('clone_url'))
    print('SSH URL:', result.get('ssh_url'))
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'ERROR {e.code}: {body}')
    # If 422 → repo might already exist
    if 'already_exists' in body:
        print('REPO_ALREADY_EXISTS')
except Exception as e:
    print(f'ERROR: {str(e)}')