################################################################################
# Viper App Oscilloscope
#
# Created by VIPER Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

# warning!! this example is too big for the Particle Core :(


# import needed modules
import streams
from wireless import wifi
from cc3000 import cc3000_tiny as cc3000
import adc
# and import the viperapp module
from viperapp import viperapp



streams.serial()

# save the template.html in the board flash with new_resource
new_resource("template.html")

# connect to a wifi network
try:
    cc3000.auto_init()

    print("Establishing Link...")
    wifi.link("Network-Name",wifi.WIFI_WPA2,"Wifi-Password")

    print("Ok!")
        
except Exception as e:
    print(e)


# Configure and run the ViperApp instance
vp = viperapp.ViperApp("Oscilloscope","Yeah, a javascript oscilloscope","resource://template.html")
vp.run()


while True:
    sleep(500)
    # read from adc
    x = adc.read(A4)
    # send the value to the mobile app via a notification event called "adc"
    # the notification is sent only after the mobile app to viper script link is established ;)
    vp.notify("adc",x)