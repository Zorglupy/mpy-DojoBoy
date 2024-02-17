#
#
#  DojoBoy - Create WiFi Acces Point
#
#

from dojoboy_v2 import djbDisplay
from dojoboy_v2 import djbNetwork
from dojoboy_v2 import djbControl

display = djbDisplay.Display(False)
wifi = djbNetwork.Network()

wifi.mode = wifi.ACCESS_POINT

wifi.ssid = 'DJB-NET'
wifi.password = 'password1234'

wifi.init_network()

display.center_text_XY("Mode:Station" if wifi.mode==wifi.STATION else "Mode:Access Point",y=56)
display.center_text_XY(wifi.get_ip(),y=65)
display.show()