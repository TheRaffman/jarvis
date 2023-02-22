from phue import Bridge
import os

class JarvisHue:
    # Variables that only THIS instance can see
    bridge_ip_address = os.environ.get("bridge_ip_address")
    hue_bridge = Bridge(bridge_ip_address)

    def __init__(self):
        print("")
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
