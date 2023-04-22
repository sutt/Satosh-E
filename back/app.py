import os, sys
import argparse
import requests

from flask import (
    Flask,
    send_file,
    request,
    render_template,
    jsonify,
)
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/ok')
def ok():
    return 'Satosh-E is running'

@app.route('/generate')
def generate():
    dalle_api_key = os.getenv('OPENAI_API_KEY')
    img = requests.get(
        'https://api.openai.com/dall-e/encode', 
        headers={'Authorization': f'Bearer {dalle_api_key}'}
    )    
    return send_file(img, mimetype='image/png')
    
    return 'Satosh-E is running'

if __name__ == '__main__':
    # app.run(host=host, port=port, debug=b_flask_debug) 
    app.run(debug=True)