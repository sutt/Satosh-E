import os, sys
import argparse
# import tempfile
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

# app = Flask(__name__)
app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return render_template(
        'index.html',
    )
@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return resp

@app.route('/ok')
def ok():
    return 'Satosh-E is running!'





@app.route('/tip')
def tip():
    dataurl = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAcIAAAHCAQAAAABUY/ToAAADt0lEQVR4nO2cXc6bOhBAz1ws5dFIXUCWAjvokrKmuwNYyreASvgRyWj64DGQfG1VtYkS0pmnEDiyLY3mH0T5Mxn/+0MQnHTSSSeddNJJJ1+PFJOASAvSp4BIu4j0SUR6AFJ9qn/ybp18LRJVVaVTVdWpUR1iRlWz3YBG7bmp0d3Dw7HO6eTjyWpu5DI1Cumk0rMIxFkgZspdkXC/NZ18DzLcXCupRWERRmkUWNCxDyjpXms6+S+Q41mVTmeBdFK6qVHpH7ymk0clqx2KCiQQALppCWaH4iw69vb/viB5rHM6+XByFBGRFszmFOsD0qeTWozEUtKy5+/WyZciix3a7IvCLDqeMzqe52p9EpipuseaTr4jKX0KQJISAMllAkpaH2cROWeARSAFpH/ybp18LbKUgVSnRiHWX91aCyqPlMuM1ZG8PuTkXkwjYua2xjjQlKBIh7hVGxvXISd/TKaTSh9zialZ3RjQqFw+LH3ToVYbj3pOJ+9P7nyZGR7N0E1QXNsQzYMV5eqm1XId65xOPo40AzN+zQjx2y4RU1hCTcWWYGlazEG64Vm7dfIVyVpjTEKpSY9FjZrM2Dcq3bQA6YsKsVEZ22/P3K2Tr0hWX3bVqK/JGTW6jmpOjuLu3Jc5uRMb59jFQ9cTHzU8suQs+uyHkz8hy4jHLIwS0KH82Shju6ZpKaA6Ue8e85xOPpA0LaHTWeSimZrbA2MLEHPpq91vTSffglznh5agxAlIbbmk+/+kdB8hA4tYvk+T/3pNJ9+LXGdhc3FU1uYorY9sfqtES2so5PUhJ6+kxtTsmmGWg63tM7AoaAu7XYecXGXXWh0Asz6lOp33mrM94jrk5JXs6kOWvVcdovZhLbcHy8vclzl5JVvffrs0SxOtqLh3Y5PrkJM/JruPAES10fuSzGOBdZVl95bQQc/p5MNIkRZ0SCI1EVusDNR9BJsHKQXs5O+XOXkrWzxURzy2eRDA2mdgQyGe2zv5SSwvi1r6ZUWb1hu1X9as8/ie2zt5K3ot1lWtA9Q137c422qRrkNOfiK3735YKFS7r9IXlbJXOlgb+sc8p5OPID9/94O1DDSx7+C7HXLy1+T2maFaaBRpG5WeRnUoZknE8zInf4PspkVE2rW5EesM2hoeSX/vNZ18K1L6dNIaSc8il2mR8lm0HqhvvN53TSePTd5+90MhI8QllBF9UouOZ6X8Ip1UnrdbJ1+R3PXtsebGWi6qboy1aVZaH14fcnIv4t84d9JJJ5100kkn/3HyO/i8DXnZgO1iAAAAAElFTkSuQmCC"
    MOCK_ADMIN_KEY = "as"
    return render_template(
        'tip.html', 
        img=dataurl,
        admin_key=MOCK_ADMIN_KEY,   #remove security risk
        )

@app.route('/generate2')
def generate2():
    return render_template(
    'generate.html'
    )


@app.route('/generate3')
def generate3():
    return render_template(
    'gen.html'
    )


@app.route('/generate')
def generate():
    text_prompt = request.args.get('prompt', 'Gorilla holding a bitcoin')
    img_url = call_dalle_api(text_prompt)
    # img_response = requests.get(img_url)
    return render_template(
        'gen-result.html',
        img_url=img_url,
        s_prompt=text_prompt,
    )

@app.route('/download_image')
def download_image():
    # Save the image to a temporary file
    
    temp_dir = tempfile.mkdtemp()
    temp_filename = os.path.join(temp_dir, 'generated_image.png')
    with open(temp_filename, 'wb') as f:
        f.write(img_response.content)

    # Return the image using send_from_directory
    return send_from_directory(temp_dir, 'generated_image.png', mimetype='image/png', as_attachment=True)


if __name__ == '__main__':
    # app.run(host=host, port=port, debug=b_flask_debug) 
    app.run(debug=False)