from flask import Flask, request
from pymongo import MongoClient
import gridfs
import time
import os

app = Flask(__name__)

# MongoDB 연결 설정
client = MongoClient('mongodb://mongo:27017/')
db = client['smartfarm']
fs = gridfs.GridFS(db)

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.data
    device_id = request.headers.get('device-id')
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    try:
        image_id = f"{device_id}_{timestamp}.jpg"
        fs.put(image, filename=image_id, id=image_id)

        collection = db[device_id]
        data = {
            'device_id': device_id,
            'timestamp': timestamp,
            'image_id': image_id
        }
        collection.insert_one(data)

        return "Image received and stored in GridFS!", 200
    
    except Exception as e:
        return f"Failed to upload image: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    print("Server started successfully.")
