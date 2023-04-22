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
from flask_cors import CORS
from dotenv import load_dotenv

from modules.services import (
    call_dalle_api,
    call_midjourney_api,
)

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/ok')
def ok():
    return 'Satosh-E is running!'

@app.route('/generate')
def generate():
    
    text_prompt = request.args.get('prompt', 'Gorilla holding a bitcoin')
    img_url = call_dalle_api(text_prompt)
    img_response = requests.get(img_url)

    # Save the image to a temporary file
    temp_dir = tempfile.mkdtemp()
    temp_filename = os.path.join(temp_dir, 'generated_image.png')
    with open(temp_filename, 'wb') as f:
        f.write(img_response.content)

    # Return the image using send_from_directory
    return send_from_directory(temp_dir, 'generated_image.png', mimetype='image/png', as_attachment=True)


if __name__ == '__main__':
    # app.run(host=host, port=port, debug=b_flask_debug) 
    app.run(debug=True)