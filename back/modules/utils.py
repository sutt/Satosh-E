import os
import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.environ.get('LNBITS_URL')

# HOST_KEY = os.environ.get('LNBITS_USR_KEY')
# Todo - remove these except for tests
# owner_id    = os.environ.get('OWNER_ID')
# wallet_id   = os.environ.get('WALLET_ID')
# admin_key   = os.environ.get('ADMIN_KEY')
# invoice_key = os.environ.get('INVOICE_KEY')
# basic_lnurlp = os.environ.get('BASIC_LNURLP')

def req_endpoint(endpoint, opt={}, debug=False):
    '''
        
    '''

    method =    opt.get('method',   'GET')
    headers =   opt.get('headers',  {})
    body =      opt.get('body',     {})
    
    try:
        
        response = requests.request(
            method=method, 
            url=BASE_URL + endpoint,
            headers=headers,
            json=body,
            timeout=2,
        )
        
        response.raise_for_status()
        
        data = response.json()

        if debug: print(data)

        return data
    
    except Exception as e:
        
        if debug:
            print(f'err in reqEnpoint: {e}')
            print(f'{response.status_code}\n{response.text}')
        return None