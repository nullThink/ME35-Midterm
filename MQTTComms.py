import paho.mqtt.client as mqtt
import time
import os
from compSecrets import *

angles = []

def parseAngles():
    anglesFile = open("gaitAngles.txt", 'r')
    lines = anglesFile.readlines()
    for line in lines:
        line = line.strip()
        line = line.replace("\t", " ")
        angleList = line.split(" ", 2)
        angles.append("("+angleList[0] + ', ' +angleList[1]+')')

parseAngles()


# PC MQTT Overall Setup
toggleAdafruitDashboardSetup = False

compClient = mqtt.Client('nullThink')
topic = 'angles'
#ip=brokerIP
ip = eecsIP

compClient.connect(ip)

def on_message(user, userName, msg):
    if(msg.topic == topic):
        try:
            decodedMessage = msg.payload.decode().strip()

            parsedMessage = decodedMessage.replace("(", "")
            parsedMessage = parsedMessage.replace(")", "")
            angles = parsedMessage.split(",", 2)

            aio.publish(hipAngleFeedKey, angles[0])
            time.sleep(aioRateLimit)
            aio.publish(kneeAngleFeedKey, angles[1])
            time.sleep(aioRateLimit)
        except Exception:
            time.sleep(60)

def sendAngles():
    for angle in angles:
        compClient.publish(topic, angle)

compClient.on_message = on_message
compClient.loop_start()
compClient.subscribe(topic)

# print(angles)

# Adafruit IO Dashboard Interaction
# Note: Rate limit = 30 points per minute
import Adafruit_IO
import sys

aio = Adafruit_IO.MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
aioRateLimit = 60/30

buttonFeedKey = 'me35-midterm'
hipAngleFeedKey = 'me35-midterm-hip'
kneeAngleFeedKey = 'me35-midterm-knee'
sendAnglesKey = 'angles'

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format("all"))
    # Subscribe to changes on a feed.
    client.subscribe(buttonFeedKey)
    client.subscribe(hipAngleFeedKey)
    client.subscribe(kneeAngleFeedKey)
    client.subscribe(sendAnglesKey)

def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(buttonFeedKey, granted_qos[0]))

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

# Keep track of variables. Done so that if button is pressed before assigning
# values, it sends out 0. For if sending values through Adafruit instead of reading
currentHipAngle = [0]
currentKneeAngle = [0]

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

    if(feed_id == hipAngleFeedKey):
        currentHipAngle.append(payload)
    elif(feed_id == kneeAngleFeedKey):
        currentKneeAngle.append(payload)
    elif(feed_id == buttonFeedKey and payload == "1"):
        print("Button has been pressed.")
        send_message("({0}, {1})".format(currentHipAngle[-1], currentKneeAngle[-1]))
    elif(feed_id == sendAnglesKey and payload == "1"):
        print("Sending angles...")
        sendAngles()
    else:
        if(payload == "0"):
            print("Button has been released.")
        else:
            print("Unconfigured Feed")

def send_message(msg):
    compClient.publish(topic, msg) 
# Setup the callback functions defined above.
aio.on_subscribe  = subscribe
aio.on_message = message
aio.on_connect    = connected
aio.on_disconnect = disconnected

# aio.loop_background()

# Connect to the Adafruit IO server.
aio.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
aio.loop_blocking()