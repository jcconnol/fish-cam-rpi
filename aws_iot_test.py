import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def fish_data_recieving(self, params, packet):
	print("recieved message from aws iotcore")
	print("packet topic: "+packet.topic)
	print("Payload: ", (packet.payload))
	return packet.payload

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
myMQTTClient.subscribe("fish_cam", 1, fish_data_recieving)
while True:
	time.sleep(1)
	
	
	
