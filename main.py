import os
from stability_sdk import client
from flask import Flask, request, send_file, make_response, jsonify
from views import generateImage, compareImages
import uuid
from flask_cors import CORS
import csv
import time
import json

app = Flask(__name__)

# Allow all origins CORS
CORS(app, resources={r"/*": {"origins": "*"}})

os.environ['STABILITY_HOST'] = os.getenv('STABILITY_HOST')
os.environ['STABILITY_KEY'] = os.getenv('STABILITY_KEY')


# Set up our connection to the API.
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],  # API Key reference.
    verbose=True,  # Print debug messages.
    # Set the engine to use for generation.
    engine="stable-diffusion-xl-beta-v2-2-2",
    # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0
    # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-diffusion-xl-beta-v2-2-2 stable-inpainting-v1-0 stable-inpainting-512-v2-0
)


@app.route('/generate', methods=['POST'])
def generateImages():
    prompt = request.form.get('prompt')
    seed = request.form.get('seed')
    # generate a random image name
    random_image_name = str(uuid.uuid4())
    # Set up our initial generation parameters.
    # generateImage(stability_api, prompt, random_image_name)
    # write log file
    with open('log.csv', 'a') as log:
        log_writer = csv.writer(
            log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow(
            [request.remote_addr, prompt, seed, random_image_name])
    # return send_file(f'./images/{random_image_name}.png', mimetype='image/png')
    # time.sleep(3)
    response = send_file(
        f'./images/0ba34621-12b0-4586-a02e-e74a87d4fdd8.png', mimetype='image/png', as_attachment=True, download_name=f'0ba34621-12b0-4586-a02e-e74a87d4fdd8.png')

    response.set_cookie('generated', 'true')
    response.headers.add('Access-Control-Expose-Headers',
                         'Content-Disposition , Set-Cookie')
    return response


@app.route('/compare', methods=['POST'])
def matchImage():
    # get the image name from the request
    image_name = request.form.get('image_name')
    print(image_name)
    with open('data.json', 'r') as json_data_file:
        data = json.load(json_data_file)
        for file in data:
            result = compareImages(f'./persons/{file["image"]}',
                                   f'./images/{image_name}')
            if result.get('verified'):
                response = send_file(
                    f'./persons/{file["image"]}', mimetype='image/png', as_attachment=True, download_name=file['image']
                )
                response.headers.add('Access-Control-Expose-Headers',
                                     'Content-Disposition , Set-Cookie')

                return response

    return 'No match found', 404


@app.route('/get-image-person', methods=['GET'])
def getImagePerson():
    # get the image name from the request
    image_name = request.args.get('image_name')
    print(image_name)
    with open('data.json', 'r') as json_data_file:
        data = json.load(json_data_file)
        for file in data:
            if file['image'] == image_name:
                result = compareImages(
                    f'./persons/{file["image"]}', f'./images/{image_name}')
                return jsonify(file), 200

    return 'No match found', 404


if __name__ == '__main__':
    app.run(debug=True)
