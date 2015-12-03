################################################################################
# ViperApp Basic
#
# Created by VIPER Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

# for this example to work you need to install the cc3000 wifi driver package!

# import everything needed
import streams
from wireless import wifi
from cc3000 import cc3000_tiny as cc3000
# and also import the viperapp module
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

    
#### ViperApp Setup    
    
# :: Javascript to Python ::
# the following function will be called when the template button is pressed
def show_message(msg):
    print(msg)

# :: Python to Javascript ::
# the following function sends messages to the mobile app
# labelling them as "btn" events
pressed =0 
def btn_pressed():
    global pressed
    pressed+=1
    vp.notify("btn","Board button pressed ["+str(pressed)+"] times")
      
# when the board button is pressed, send a notification to the mobile app
onPinFall(BTN0,btn_pressed)


# configure the viper app with a name, a descripton and the template url
vp = viperapp.ViperApp("Test","Test Object","resource://template.html")

# everytime Javascript generates the event "showmsg" the function show_message is called
vp.on("showmsg",show_message)

# run the ViperApp!
vp.run()

# since vp.run starts a new thread, you can do whatever else you want down here!


