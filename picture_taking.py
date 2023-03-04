from picamera import PiCamera
from time import sleep
import base64
import boto3
import os

IMAGE_PATH = 'fish_pic.jpg'

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

camera = PiCamera()
camera.start_preview()
camera.capture(IMAGE_PATH)

sleep(1)

camera.stop_preview()

print(len(get_base64_encoded_image(IMAGE_PATH)))



client = boto3.client('s3', 
    aws_access_key_id=os.environ["AWS_SERVER_PUBLIC_KEY"], 
    aws_secret_access_key=os.environ["AWS_SERVER_SECRET_KEY"], 
    region_name='us-east-2')

client.upload_file(IMAGE_PATH, 'fish-cam', IMAGE_PATH)




