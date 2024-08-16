import time
import json
from flask import Flask, request
from gcp import GCSClient

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.data
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    with open ("service_key.json", "r") as f:
        service_key = json.load(f)
    
    client = GCSClient(service_key)
    client.upload_image(
        bucket_name='smartfarm_leafs',
        image=image,
        timestamp=timestamp
    )

    return "Image received!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
