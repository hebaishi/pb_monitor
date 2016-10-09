#!/usr/bin/python
import os
import io
import picamera
import time
import json
from datetime import datetime
import time
from PIL import Image
import pybullet
import urllib2

from optparse import OptionParser

class PushBulletMonitor(object):
    def __init__(self, config):
        """
        Initialisation function
        """
        self.access_token = config["access_token"]
        self.refresh_interval = config["refresh_interval"]
        self.sender_email = config["sender_email"]
        self.temp_folder = config["temp_folder"]
        self.commands = config["commands"]
        self.camera = picamera.PiCamera()

    def _new_image(self, width, height):
        """
        Internal function to capture a new image
        """
        time = datetime.now()
        filename = self.temp_folder
        filename += "pb_monitor-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
        self.camera.resolution = (width, height)
        self.camera.capture(filename)
        print "Captured %s" % filename
        return filename

    def run(self):
        """
        Main function to run monitor
        """
        current_time = time.time()
        while True:
            try:
                time.sleep(self.refresh_interval)
                pushes_list = pybullet.get_pushes(current_time, True, self.access_token)
                if pushes_list:
                    print "Getting pushes"
                    pushes = json.loads(pushes_list)["pushes"]

                    for push in pushes:
                        if push["sender_email"] == self.sender_email and push["type"] == "note":
                            for command in self.commands:
                                if push["body"] == command["command_name"]:
                                    current_time = time.time()
                                    temp_filename = self._new_image(command["width"], command["height"])
                                    pybullet.push_file(temp_filename, "Snapshot.jpg", datetime.now().strftime("Snapshot taken on %d-%b-%Y at %H:%M %p"), self.access_token)
                                    os.remove(temp_filename)
            except KeyboardInterrupt:
                exit()
            except:
                pass

def wait_for_internet_connection():
    while True:
        try:
            response = urllib2.urlopen('http://www.google.com',timeout=5)
            return
        except urllib2.URLError:
            pass

if __name__ == "__main__":
    wait_for_internet_connection()
    parser = OptionParser()
    parser.add_option("-c", "--config-file", dest="config_filename",
                      help="Path to configuration JSON file", type="string")
    (options, args) = parser.parse_args()

    config_file = open(options.config_filename, "r")
    config = json.loads(config_file.read())
    monitor = PushBulletMonitor(config)
    monitor.run()
