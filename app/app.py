from flask import Flask, request, jsonify, current_app
from pymongo import MongoClient
from celery import Celery
import gridfs
import time
import logging

app = Flask(__name__)

# MongoDB 연결 설정
client = MongoClient('mongodb://mongo:27017/')
db = client['smartfarm']
fs = gridfs.GridFS(db)

# celery instance 생성
celery_app = Celery(app.name, broker='pyamqp://guest@localhost//')
celery_app.conf.update(app.config)
celery_app.conf.result_backend = 'rpc://'

# 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_logging(app):
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

setup_logging(app)

@celery_app.task
def store_image(image, device_id, timestamp):
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

        logger.info(f"{image_id} stored in MongoDB!")
        return f"{image_id} stored in MongoDB!", 200
    
    except Exception as e:
        logger.error(f"Failed to store image: {str(e)}")
        return f"Failed to store image: {str(e)}", 500

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.data
    device_id = request.headers.get('device-id')
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    current_app.logger.info(f"Received upload request from device_id: {device_id}")

    task = store_image.delay(image, device_id, timestamp)
    
    return jsonify({'task_id': task.id}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
