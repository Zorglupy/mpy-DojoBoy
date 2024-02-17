#
#
#  DojoBoy - Connection to WiFi and get informations on Internet
#
#

from dojoboy_v2 import djbDisplay
from dojoboy_v2 import djbNetwork
from dojoboy_v2 import djbControl

from time import sleep, ticks_ms, ticks_diff
import requests

display = djbDisplay.Display(False)
wifi = djbNetwork.Network()

wifi.mode = wifi.STATION

wifi.ssid = 'My Wifi'
wifi.password = 'Wifi_Password'

wifi.init_network()

display.center_text_XY("Mode:Station" if wifi.mode==wifi.STATION else "Mode:Access Point",y=56)
display.center_text_XY(wifi.get_ip(),y=65)
display.show()

start = ticks_ms() # start a millisecond counter

astronauts = requests.get("http://api.open-notify.org/astros.json").json()

delta = ticks_diff(ticks_ms(), start)

number = astronauts['number']
print('There are', number, 'astronauts in space.')
str_astronauts = "Il y a "+ str(number) +" astronautes"
display.fill(0)
display.text(str_astronauts,0,0)
display.text("dans l'espace",0,8)
for i in range(number):
    name_astronauts = str(i+1)+" "+str(astronauts['people'][i]['name'])
    display.text(name_astronauts, 0, 24 + (i * 8))
    print(i+1, astronauts['people'][i]['name'])

print("HTTP GET Time in milliseconds:", delta)

display.show()
