import os, sys
import argparse
import tempfile
import requests

from flask import (
    Flask,
    send_from_directory,
    send_file,
    request,
    render_template,
    jsonify,
)
#from flask_cors import CORS
#from dotenv import load_dotenv

#load_dotenv()

app = Flask(__name__)
#CORS(app)

@app.route('/ok')
def ok():
    return 'Satosh-E is running!'

@app.route('/dalle_generate')
def generate():
    text_prompt = request.args.get('prompt', 'Cool satoshi logo')
    #dalle_api_key = os.getenv('OPENAI_API_KEY')
    dalle_api_key = "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"
        # Ensure API key is set
    if not dalle_api_key:
        return 'OPENAI_API_KEY not found. Please set the environment variable.', 500

    # Call the DALL-E API
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
            'size': '256x256',
            'response_format': 'url'
        }
    )

    if response.status_code != 200:
        return f'Error: {response.text}', response.status_code

    img_url = response.json()['data'][0]['url']
    img_response = requests.get(img_url)

    # Save the image to a temporary file
    temp_dir = tempfile.mkdtemp()
    temp_filename = os.path.join(temp_dir, 'generated_image.png')
    with open(temp_filename, 'wb') as f:
        f.write(img_response.content)

    # Return the image using send_from_directory
    return send_from_directory(temp_dir, 'generated_image.png', mimetype='image/png', as_attachment=True)

    # Check if the request was successful
    # if response.status_code != 200:
    #     return f'Error: {response.text}', response.status_code

    # # Get the image URL from the response
    # img_url = response.json()['data'][0]['url']

    # # Fetch the image from the URL
    # img_response = requests.get(img_url)

    # # Return the image
    # #return send_file(img_response.content, mimetype='image/png')
    # return send_file(img_response.content, mimetype='image/png', attachment_filename='generated_image.png', as_attachment=True)
    # #return str(img_response)

    # # img = requests.get(
    # #     'https://api.openai.com/dall-e/encode', 
    # #     headers={'Authorization': f'Bearer {dalle_api_key}'}
    # # )    
    # # return send_file(img, mimetype='image/png')
    
    # # return 'Satosh-E is running!'

if __name__ == '__main__':
    # app.run(host=host, port=port, debug=b_flask_debug) 
    app.run(debug=True)