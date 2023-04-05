from phue import Bridge
from phue import PhueException
import os

class JarvisHue:
    # Variables that only THIS instance can see

    def __init__(self):
        print("")
        print("Preparing Hue Bridge...")
        try:
            self.bridge_ip_address = os.environ.get("bridge_ip_address")
            print("Connecting to Hue Bridge on " + self.bridge_ip_address)
            self.hue_bridge = Bridge(self.bridge_ip_address)
        except PhueException as e:
            # First time we'll receive Code 101 = "The link button has not been pressed in the last 30 seconds."
            if (e.id == 101):
                print(e.message)
                print("Press the LINK button on your Hue and run the app again.")
            else:
                print("Unexpected exception connecting to Hue Bridge - Cannot continue!")
            quit(999)

        print("Finding Hue lights...")
        lights = self.hue_bridge.get_light_objects('name')
        for light in lights:
            print("  * Found light: " + light)

        print("")
        print("Finding Hue light groups...")
        light_groups = self.hue_bridge.get_group()
        for light_group in light_groups:
            print("  * Found light group with ID: " + light_group + " and name: " + light_groups[light_group]['name'])

    def join_hue_bridge(self):
        print("Press the CONNECT button on your Hue Bridge now...")
        self.hue_bridge = Bridge()
        self.hue_bridge.connect()
        print("Hue bridge is now connected.")

    def control_hue(self):
        print("ok")

    def turn_on_group(self, group_name):
        lights_in_group = self.hue_bridge.get_group(group_name, 'lights')
        for light in lights_in_group:
            self.hue_bridge.set_light(int(light), 'on', True)

    def turn_off_group(self, group_name):
        lights_in_group = self.hue_bridge.get_group(group_name, 'lights')
        for light in lights_in_group:
            self.hue_bridge.set_light(int(light), 'on', False)
