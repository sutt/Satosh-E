import os, sys
import requests
from dotenv import load_dotenv
from flask import jsonify
from .utils import req_endpoint
load_dotenv()

dalle_api_key   = os.environ.get('OPENAI_API_KEY')
invoice_key     = os.environ.get('INVOICE_KEY')

def call_midjourney_api(text_prompt):
    pass

def call_dalle_api(
        text_prompt,
        s_img_size='256x256',   # TODO - add larger size
    ):
        
    if not dalle_api_key:
        print('OPENAI_API_KEY not found. Please set the environment variable.')
        return None
    
    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {dalle_api_key}'
        },
        json={
            'model': 'image-alpha-001',
            'prompt': text_prompt,
            'num_images': 1,
            'size': s_img_size,
            'response_format': 'url'
        }
    )

    if response.status_code != 200:
        print(f'Error: {response.text}', response.status_code)
        return None
    
    img_url = response.json()['data'][0]['url']

    return img_url


def get_wallet_balance():
    pass

def get_payments(wlt_invoice_key):
    
    endpoint = 'api/v1/payments'

    opt = {
        'headers': {
            'X-Api-Key': wlt_invoice_key
        }
    }

    data = req_endpoint(endpoint, opt)

    # lots you can do with this data, right now
    # we just use this to unclear a cached account balance
    try:
        return len(data)
    except:
        return None

def get_tip_balance():

    amt = get_balance_and_key()
    
    data = {'balance': amt}
    
    return jsonify(data)

def get_balance(wlt_invoice_key):
    
    endpoint = 'api/v1/wallet'

    opt = {
        'headers': {
            'X-Api-Key': wlt_invoice_key
        }
    }

    data = req_endpoint(endpoint, opt)
    
    if data is None: return None
    
    amount_millisats = data.get('balance') 
    amount_sats = int(amount_millisats / 1000)

    return amount_sats


if __name__ == '__main__':
    
    import argparse    
    import time

    # > python modules/services.py --prompt "woman holding a bitcoin"
    # usually takes 4-5 seconds
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--prompt', 
        required=False,
        help='Enter your prompt for dalle and/or midjourney')
    args = parser.parse_args()

    prompt = (
        'racoon holding a bitcoin' 
        if args.prompt is None 
        else args.prompt
    )
    msg  = f'''calling dall-e api \n'''
    msg += f'''prompt: {args.prompt}\n'''
    msg += f'''openai key: {dalle_api_key}\n''' 
    msg += f'''calling now... \n'''
    print(msg)
    
    t0 = time.time()
    result = call_dalle_api(prompt)
    t1 = time.time()

    msg = '''\n'''
    msg  = f'''result: {result}\n'''
    msg += f'''time: {t1-t0}\n'''
    print(msg)


