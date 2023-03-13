import Adafruit_IO
import sys
from compSecrets import *

# REST API TESTING AND LEARNING

# aioAPI = Adafruit_IO.Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# testData = aio.receive(aio.feeds()[0].key)
# print(aioAPI.feeds())
# print(testData)

# MQTT TESTING AND LEARNING

aio = Adafruit_IO.MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

buttonFeedKey = 'me35-midterm'
hipAngleFeedKey = 'me35-midterm-hip'
kneeAngleFeedKey = 'me35-midterm-knee'

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format("all"))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(buttonFeedKey)
    client.subscribe(hipAngleFeedKey)
    client.subscribe(kneeAngleFeedKey)

def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(buttonFeedKey, granted_qos[0]))

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

# Setup the callback functions defined above.
aio.on_connect    = connected
aio.on_disconnect = disconnected
aio.on_message    = message
aio.on_subscribe  = subscribe

# Connect to the Adafruit IO server.
aio.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
aio.loop_blocking()