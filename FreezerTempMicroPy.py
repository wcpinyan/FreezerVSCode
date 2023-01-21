
from machine import Pin
from time import sleep
import dht
import network
import socket
import json
from mqtt import *

# import secrets

def connect():
    print("inside connect")
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Linksys01','dianne01')
    while wlan.isconnected()==False:
        print('waiting for connection...')
        sleep(1)
    ip=wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    print("inside open_socket")
    address=(ip,80)
    print(f"address: {address}")
    connection=socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

font_family = "monospace"
unit="F"
unit_hum="%"
temp_f=0
hum=0

def webpage(temp_f,hum):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta http-equiv="refresh" content="10">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    html{{font-family: {font_family}; background-color: snowwhite;
    display:inline-block; margin: 0px auto; text-align: center;}}
      h1{{color: darkgray; width: 200; word-wrap: break-word; padding: 2vh; font-size: 35px;}}
      p{{font-size: 1.5rem; width: 200; word-wrap: break-word;}}
      .button{{font-family: {font_family};display: inline-block;
      background-color: black; border: none;
      border-radius: 4px; color: white; padding: 16px 40px;
      text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
      p.dotted {{margin: auto;
      width: 75%; font-size: 25px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>Freezer Temp</title>
    <h1>Basement Freezer Temp</h1>
    <br>
    
    <br>
    <div >
    <span style="color: white;font-size:4.0rem;border-radius: 75px;
  background: #73AD21;
  padding: 50px;
  width: 300px;
  height: 300px;">{temp_f}°{unit}</span></div><br>
  <div style="margin-top:140px;">
  <span style="color: white;font-size:3.5rem;border-radius: 75px;
  background: rgba(0, 0, 255, 0.7);;
  padding: 50px;
  
  width: 300px;
  height: 300px;">{hum}{unit_hum} Hum</span></div>
    </body></html>
    """
    return html


sensor = dht.DHT22(Pin(15))

def serve():
    while True:
      try:
        print("inside serve")
        sleep(10)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9/5) + 32.0
#         client=connection.accept()[0]
#         request=client.recv(1024)
#         request=str(request)
#         html=webpage(temp_f,hum)
#         client.send(html)
#         client.send(temp_f)
#         client.close()
        data={"temp":f"{temp_f}","humidity":f"{hum}"}
        data=json.dumps(data)
        mqttclient.publish("pinyanmed/freezer/data",data)
    #     print('Temperature: %3.1f C' %temp)
        print('Temperature: %3.1f F' %temp_f)
        print('Humidity: %3.1f %%' %hum)
      except OSError as e:
        print('Failed to read sensor.')
        
try:
    ip=connect()
#     connection=open_socket(ip)
#     print("socket conn made.................")
    mqttclient=connect_mqtt()
    print(mqttclient)
#     serve(connection)
    serve()
except KeyboardInterrupt:
    machine.reset()