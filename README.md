# pfRICH-Translation-Stage
Python Script for KDC101 Motor Control



1. Ensure that the KDC101 usb is propertly attached and not disconnected:
	'sudo dmesg | grep -i usb'

2. If disconnected, switch usb ports, if error persists:
	'lsmod | grep ftdi_sio'
		
3. If above command returns nothing:
	'sudo modprobe ftdi_sio'
	run 2. again
	run 1. again
	You shold see outputs

4. Open python environment:
   	'source translation/bin/activate'

5. Ready to run python script:
	click top right play button drop down menu, "Run Python File"
	if error, run sudo in front of the code

6. If there are underlined import errors:
   	'pip install pyserial'

7. Make sure that the script has the right python interpreter selected:
   	press "Ctrl+Shift+P"
	select 'Python: Select Interpreter'
	click "Enter interpreter path..."
	to double check your environment path write in terminal 'which python' when the environment is activated
	paste the above path into the python interpreter path on VSCODE 
	
6. After experiment is done, exist VSCODE or deactivate environment:
   	'deactivate'
