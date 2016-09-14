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

from optparse import OptionParser

class PushBulletMonitor(object):
    def __init__(self, access_token, refresh_interval, sender_email, sender_command, temp_folder):
        """
        Initialisation function
        """
        self.access_token = access_token
        self.refresh_interval = refresh_interval
        self.sender_email = sender_email
        self.sender_command = sender_command
        self.temp_folder = temp_folder
        self.camera = picamera.PiCamera()

    def _new_image(self):
        """
        Internal function to capture a new image
        """
        time = datetime.now()
        filename = self.temp_folder
        filename += "motion-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
        self.camera.resolution = (1920, 1080)
        self.camera.capture(filename)
        print "Captured %s" % filename
        return filename

    def run(self):
        current_time = time.time()
        while True:
            time.sleep(self.refresh_interval)
            pushes_list = pybullet.get_pushes(current_time, True, self.access_token)
            if pushes_list:
                pushes_data = json.loads(pushes_list)["pushes"]

                for idx in range(len(pushes_data)-1, -1, -1):
                    print idx
                    if pushes_data[idx]["sender_email"] == self.sender_email and pushes_data[idx]["type"] == "note" and pushes_data[idx]["body"] == self.sender_command:
                        temp_filename = self._new_image()
                        pybullet.push_file(temp_filename, "Snapshot.jpg", "Snapshot", self.access_token)
                        os.remove(temp_filename)
                        current_time = time.time()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--config-file", dest="config_filename",
                      help="Path to configuration JSON file", type="string")
    (options, args) = parser.parse_args()


    config_file = open(options.config_filename, "r")
    config = json.loads(config_file.read())
    monitor = PushBulletMonitor(
        config["access_token"],
        config["refresh_interval"],
        config["sender_email"],
        config["sender_command"],
        config["temp_folder"]
    )
    monitor.run()
