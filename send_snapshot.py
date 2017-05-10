#!/usr/bin/python
from optparse import OptionParser
import pybullet
import json

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--config-file", dest="config_filename",
                      help="Path to configuration JSON file", type="string")
    parser.add_option("-f", "--filename", dest="filename",
                      help="File to send", type="string")
    (options, args) = parser.parse_args()

    config_file = open(options.config_filename, "r")
    config = json.loads(config_file.read())

    pybullet.push_file(
        options.filename,
        "Motion.jpg",
        "Motion detected",
        config["access_token"]
    )
