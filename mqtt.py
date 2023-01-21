from umqtt.simple import MQTTClient

def connect_mqtt():
    print("inside connect_mqtt")
    prefix="pinyanmed/"
#     client=MQTTClient(client_id=b"FreezerData",
#                         server=b"9658e4debf9744dcb4bc7b651293b9fd.s2.eu.hivemq.cloud",
#                         port=0,
#                         user=b"buddyp1",
#                         password=b"Cl@rkie01",
#                         keepalive=7200,
#                         ssl=True,
#                         ssl_params={'server_hostname':'9658e4debf9744dcb4bc7b651293b9fd.s2.eu.hivemq.cloud'}
#                         )
    client = MQTTClient(prefix+"freezer/#", "test.mosquitto.org",port=1883,user=None, password=None, keepalive=300, ssl=False, ssl_params={})
    client.set_callback(callback)

#     client.subscribe(prefix+"freezer/#")
    client.connect()
   
#     client.set_callback(callback)
#     client.subscribe(prefix+"GPIO/#") //don't need this unless sending command back to pico
#     
    
    print("mqtt client connected:")
    print(client.server)
    return client

def callback(topic, msg):
    global json_msg
    json_msg = json.loads(msg.decode('utf-8'))
    print("Message received")
#     draw_now()
        
def publish(mqttclient,topic,value):
    print(topic)
    print(str(value))
    mqttclient.publish(topic,value)
    print("publish done.")
    
