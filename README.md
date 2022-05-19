# vk_modules
this script is designed to solve the problem that arises when you need to connect several simple (or more complex) scripts to one vk_api token

for this, scripts are presented in the form of modules for the vk_modules program

* makefile is used to control vk_modules

* systemd service is used for initialization

# Setup
run following commands to put the systemd service
to the right place, make systemctl stuff and get things ready to run:<br>

`cd <PATH_TO_PROJECT_DIR>`<br>
`make setup`
> (make sure that the <PATH_TO_PROJET_DIR> is somewhere in user home folder)

to run the script:<br>
`make start`

to stop script:<br>
`make stop`

# Setting configuration
to insert telegram bot key:

* make file <br>
`<PATH_TO_PROJET_DIR>/token.txt`<br>
and put your bot token into this file

# Modules description
each module is in its own folder inside the modules directory and has a main.py file.

inside main.py, each module contains two functions: 
* module_start (at the time of initialization) 
* module_execute (at the time of execution).

functions arguments:
* `SCRIPT_PATH` - (one can add '/modules/{module_name}/' to interact with files in the module directory)
* `vk_session` (only module_execute) - to call methods from vk-api
* `event` (only module_execute) - vk event (according to the black list of events from the file <br>
  <PATH_TO_PROJET_DIR>/misc/config.json
  
to enable or disable modules one can edit `loaded_modules` in `<PATH_TO_PROJET_DIR>/misc/config.json`
  
## message_logger module
this module is engaged in logging incoming and outgoing messages for subsequent analytics using the logging library

logs are contained in `<PATH_TO_PROJET_DIR>/modules/message_logger/misc.json`

## status_sheduler module
this module is designed to monitor the status of the vk_modules script

this module responds with the given message to the entered command (stored in it`s main.py file)
(you need to use "Избранное" dialog for this)



