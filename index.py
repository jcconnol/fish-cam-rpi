from RPLCD import CharLCD
import RPi.GPIO as GPIO
import os
import glob
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


############## TEMPERATURE FUNCTIONS ###############


# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_rom():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return '%3.3f'% temp_f
 


############## PICTURE ###############

IMAGE_PATH = 'fish_pic.jpg'
BUCKET_NAME = 'fish-cam'

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def take_picture():
	camera = PiCamera()
	camera.start_preview()
	camera.capture(IMAGE_PATH)

	sleep(1)

	camera.stop_preview()
	return get_base64_encoded_image(IMAGE_PATH)


def s3_image_upload():
	client = boto3.client('s3', 
		aws_access_key_id=os.environ["AWS_SERVER_PUBLIC_KEY"], 
		aws_secret_access_key=os.environ["AWS_SERVER_SECRET_KEY"], 
		region_name='us-east-2')

	client.upload_file(IMAGE_PATH, 'fish-cam', IMAGE_PATH)



def upload_s3_json(json_data):
	client = boto3.client('s3', 
		aws_access_key_id=os.environ["AWS_SERVER_PUBLIC_KEY"], 
		aws_secret_access_key=os.environ["AWS_SERVER_SECRET_KEY"], 
		region_name='us-east-2')
		
	
		
	s3_object = s3.Object(BUCKET_NAME, 'fish_cam.json')
	s3_object.put(
		Body=(bytes(json.dumps(json_data).encode('UTF-8')))
	)


############## AWS MQTT COMMS ###############


def fish_data_recieving(self, params, packet):
	print("recieved message from aws iotcore")
	print("packet topic: "+packet.topic)
	print("Payload: ", (packet.payload))
	temp = read_temp()
	
	fish_json_data = {
		"temp_f": temp
	}
	
	upload_s3_json(fish_json_data)
	
	take_picture()
	s3_image_upload()


print("run")

myMQTTClient = AWSIoTMQTTClient("FishCamClient")
myMQTTClient.configureEndpoint("a2uum0c49otnb0-ats.iot.us-east-2.amazonaws.com", 8883)

myMQTTClient.configureCredentials("/home/pi/AWSIoT/root-ca.pem", "/home/pi/AWSIoT/private.pem.key", "/home/pi/AWSIoT/certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

print("initiating topic...")

myMQTTClient.connect()
myMQTTClient.subscribe("home/fish_data", 1, fish_data_recieving)



degree_symbol = (
	0b00111,
	0b00101,
	0b00111,
	0b00000,
	0b00000,
	0b00000,
	0b00000,
	0b00000,
)



iter = 0
lcd_width = 16
lcd_height = 1

lcd_string = " Temp: "

GPIO.setwarnings(False)
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23])
lcd.create_char(0, degree_symbol)

while(True):
	lcd_string = " Temp: " + read_temp() + chr(0) + "F"
	lcd.cursor_pos = (0, 0) 
	lcd.write_string(lcd_string)
	time.sleep(5)
	lcd.clear()
	time.sleep(1)
	

	
	
	
	

