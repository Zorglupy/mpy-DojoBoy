#
#
#  DojoBoy - WiFi connection to Acces Point
#
#

from dojoboy_v2 import djbDisplay
from dojoboy_v2 import djbNetwork
from dojoboy_v2 import djbControl

display = djbDisplay.Display(False)
wifi = djbNetwork.Network()

wifi.mode = wifi.STATION

wifi.ssid = 'My Wifi'
wifi.password = 'Wifi_Password'

wifi.init_network()

display.center_text_XY("Mode:Station" if wifi.mode==wifi.STATION else "Mode:Access Point",y=56)
display.center_text_XY(wifi.get_ip(),y=65)
display.show()