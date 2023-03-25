from picamera import PiCamera
from time import sleep
import base64
import boto3
import os
from PIL import Image

IMAGE_PATH = 'fish_pic.jpg'

def compressMe(file, verbose = False):
    
      # Get the path of the file
    filepath = os.path.join(os.getcwd(), 
                            file)
      
    # open the image
    picture = Image.open(filepath)
      
    # Save the picture with desired quality
    # To change the quality of image,
    # set the quality variable at
    # your desired level, The more 
    # the value of quality variable 
    # and lesser the compression
    picture.save(file, 
                 "JPEG", 
                 optimize = True, 
                 quality = 10)

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

try:
    # do something with the camera
    #os.remove(IMAGE_PATH)
    camera = PiCamera()
    camera.start_preview()
    camera.capture(IMAGE_PATH)

    sleep(0.5)

    camera.stop_preview()
    compressMe(IMAGE_PATH)
    pass
finally:
    camera.close()
    





#client = boto3.client('s3', 
#    aws_access_key_id=os.environ["AWS_SERVER_PUBLIC_KEY"], 
#    aws_secret_access_key=os.environ["AWS_SERVER_SECRET_KEY"], 
#    region_name='us-east-2')

#client.upload_file(IMAGE_PATH, 'fish-cam', IMAGE_PATH)




