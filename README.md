# Pushbullet Monitor for Raspberry pi
Simply set the parameters in ```config.json``` and run the script by doing:

```bash
pb_monitor.py -c conf.json
```
## Configuration options

|     Value      |              Description                 |
|----------------|------------------------------------------|             
|access_token     | Pushbullet API Access Token             |
|refresh_interval | Interval at which to retrieve pushes    |         
|sender_email     | Email to match to trigger snapshot      |       
|sender_command   | Push body to mach to trigger shapshot   |          
|temp_folder      | Folder where temporary images are saved |            

## Installation Instructions
* Clone the repo, and also clone the [pybullet repo](https://github.com/hebaishi/pybullet)
* Create a symlink from pybullet's pybullet to pb_monitor:

```
cd pb_monitor
ln -s ../pybullet/pybullet.py .
```

* Modify the line starting with ```ExecPath``` in ```pb_monitor.service``` to point to the location of ```pb_monitor.py```

* Install the service by running:

```
systemctl daemon-reload
```

* You can start the service immediately by running:

```
systemctl start pb_monitor.service
```

The service will start automatically at boot.
