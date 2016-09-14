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
