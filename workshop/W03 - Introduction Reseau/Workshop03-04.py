#
#
#  DojoBoy - Connection to WiFi and create Web Server.
#
#

from dojoboy_v2 import djbDisplay
from dojoboy_v2 import djbNetwork
from dojoboy_v2 import djbControl

display = djbDisplay.Display(False)
wifi = djbNetwork.Network()

wifi.mode = wifi.STATION

wifi.ssid = '24'
wifi.password = 'zorghome'

wifi.data_link_buf = 1024

stateis = "LED is OFF"

html = """<!DOCTYPE html>
<html>
   <head>
     <title>Web Server On Pico W</title>
   </head>
  <body>
      <h1>Pico Wireless Web Server</h1>
      <p>%s</p>
      <a href="/light/on">Turn On</a>
      <a href="/light/off">Turn Off</a>
  </body>
</html>
"""

wifi.init_network()

display.center_text_XY("Mode:Station" if wifi.mode==wifi.STATION else "Mode:Access Point",y=56)
display.center_text_XY(wifi.get_ip(),y=64)
display.center_text_XY("Wait connection...",y=72)
display.show()

wifi.listen_data_link()

while True:
    addr = wifi.wait_conn_data_link()
    print('client connected from', addr)
    display.fill(0)
    request = wifi.recv_data_link()
    print(request)
    request = str(request)
    led_on = request.find('/light/on')
    led_off = request.find('/light/off')
    print( 'led on = ' + str(led_on))
    print( 'led off = ' + str(led_off))

    if led_on == 6:
      print("led on")
      #led.value(1)
      display.circle(80,64,10,display.RED_H, True)
      stateis = "LED is ON"

    if led_off == 6:
      print("led off")
      #led.value(0)
      display.circle(80,64,10,display.RED_L, True)
      stateis = "LED is OFF"
    display.show()
    # generate the web page with the stateis as a parameter
    response = html % stateis
    wifi.send_data_link('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    wifi.send_data_link(response)
    wifi.close_data_link()