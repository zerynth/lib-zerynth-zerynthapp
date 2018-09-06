.. module:: zerynthapp

This module provides access to the Zerynth App functionalities.

The Zerynth App is designed to make interaction with Zerynth programs on your microcontroller device easy. You can think of a Zerynth App as a bidirectional communication channel between a Zerynth script running on the microcontroller and some HTML+Javascript running as a mobile app. In conventional client/server network terms the microcontroller device would be the server, responding to requests from the mobile app client.

A program using the Zerynthapp module must provide the following components:

    * a user interface template, which the microcontroller device delivers to the mobile client
    * a set of notifications that the microcontroller device can send to the mobile app,
      where they are handled as events by scripts embedded in the template
    * a set of event functions that run on the microcontroller device in response to messages receieved from the mobile client

An instance of the Python ZerynthApp class defined in this module, when instantiated and run on your device,
waits for messages coming
from the mobile app via wifi (bluetooth LE is currently under development). Each valid message becomes
an event to be processed by its nominated function.


ZerynthApp Step by Step
=======================

Using the Python zerynthapp module is easy. 

    1. First, define an html template by adding a new html file to the current project. Declare the template as a resource so you can save it to your device's flash memory and open it in the script.
    2. Create a ZerynthaApp instance with a name and a description.
    3. Configure the instance, linking event names to the functions that handle them.
    4. Call the zerynthapp instance's ``run`` method.

HTML templates
**************

An HTML template defines the content that will be delivered to the mobile app, where it is rendered. Embedded Javascript adds event handling logic to the template. The *ZerynthApp* Javascript object can remotely call Python functions by name to be executed on the microcontroller device.

The example below will help you to understand the structure of a template: ::
    
    <html>
        <head>
            <zerynth/>
            <zerynth-jquery/>
            <zerynth-jquery-mobile/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>        
        <body>
            <div data-role="page">
                <div data-role="header"><h1>Zerynth Test App</h1></div>
                <div role="main" class="ui-content" style="text-align:center">
                    <button class="ui-btn ui-btn-inline" onclick="ZerynthApp.call('showmsg','Random number for you:'+Math.random())">Click me!</button>
                    <p id="label"></p>
                </div>
                <div data-role="footer">Powered by Zerynth</div>
            </div>
            <script>
                function update_label(msg){
                    $("#label").text(msg)
                }
                ZerynthApp.listen("btn",update_label)
                ZerynthApp.jquerymobile_scalecontent()
            </script>
        </body>
    </html>

The following special tags in the head section import javascript libraries embedded in the mobile app:

    * **<zerynth/>** imports the basic Zerynth functionalities
    * **<zerynth-jquery/>** imports the JQuery library
    * **<zerynth-jquery-mobile/>** imports the JQuery Mobile library
    * **<zerynth-jqwidgets/>** imports the JQWidgets library

The body section consists of a **<div>** defining the appearance of the interface, and scripting to handle interactions with the device.

In this instance the top-level **<div>** contains three further **<div>** elements for the app header, main window and footer.  The *onclick* attribute of the button specifies generation of an event called *showmsg*, using a call to the ZerynthApp's *call* method. All the parameters are encoded, sent to the board, and used as arguments of the Python function linked to the *show_message* event. The ZerynthApp.call method is the channel from Javascript to Python

In the final script section the ZerynthApp Javascript object is used to register a notification name *"btn"*. Everytime the microcontroller device sends a notification with that name the *update_label* JavaScript function will be executed (in this case it changes the text of the **<p>** html element whose id is "label"). Parameters can be passed to the notify function and will be transmitted to the mobile app. The *notify* method of the ZerynthApp instance is the channel from Python to Javascript.


Zerynth App Instances
*********************

An HTML template must be coupled with a Zerynth script running on a microcontroller. Here is an example script that works with the template above: ::

    import streams
    from wireless import wifi
    from cc3000 import cc3000_tiny as cc3000
    from zerynthapp import zerynthapp


    streams.serial()

    new_resource("template.html")

    try:
        cc3000.auto_init()

        print("Establishing Link...")
        wifi.link("Network Name", wifi.WIFI_WPA2,"WIFI-Password")
        print("Network OK!")        
    except Exception as e:
        print(e)

    def show_message(msg):
        print(msg)

    pressed = 0 
    def btn_pressed():
        global pressed
        pressed+=1
        vp.notify("btn", "Board button pressed ["+str(pressed)+"] times") 

    onPinFall(BTN0, btn_pressed)

    # configure and start the zerynthapp

    vp = zerynthapp.ZerynthApp("Test", "Test Object", "resource://template.html")
    vp.on("showmsg",show_message)
    vp.run()

This simple script connects to the local Wifi network, configures and runs a ZerynthApp instance. First of all, the template must be saved to flash by calling the function *new_resource*. It can then be referenced with the url "resource://name-of-file.extension". 
The script defines two functions and creates a ZerynthApp instance, passing the name of the object, its description and the url of the
resource it created to the template.
The ZerynthApp object's *on* method configures the Javascript-to-Python channel: everytime a "showmsg" event is sent from Javascript, the function *show_message* is called in the Zerynth script.
The *onPinFall* call establishes that each time the board's button is pressed the *btn_pressed*  function is called, and sends the event "btn" to the mobile app using the ZerynthApp's *notify* method. The mobile app is listening for these events, and each time it receives such an event it calls the *update_label* function.  

Object discovery, template transfer and object-to-mobile-app linking is automatically handled by the ZerynthApp instance.

Finally, more than one ZerynthApp instance can be created in the same Zerynth script.

    
The ZerynthApp class
******************

.. class:: ZerynthApp(name, desc, template, logging=False)

        Create a ZerynthApp instance named *name*, with short description *desc* and with UI template *template*
        If *logging* is True, some debug messages are printed.

        *template* must be the url of some resource that can be opened with the open builtin.

    
.. method:: on(event, fn)        

        Associate the event name *event* it executes function *fn* (possibly with arguments).
                
        
.. method:: notify(what, value)        

        Send the message named *what* with value *value* to the mobile app. Notifications are not sent if
        the mobile app is not linked (i.e. has not yet received the UI template).
                
        
.. method:: unlink()        

        Remove the link with the mobile app.
                
        
.. method:: run()        

        Start the ZerynthApp instance on a separate thread and returns immediately.
                
        
