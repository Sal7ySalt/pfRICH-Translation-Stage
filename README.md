# pfRICH-Translation-Stage
Python Script for KDC101 Motor Control <br>

Link to Thorlabs Motion Control Manual: https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf <br>
<br>
<br>

Setting up python script on VSCODE: <br>

1. Ensure that the KDC101 usb is propertly attached and not disconnected: <br>
	'sudo dmesg | grep -i usb'

2. If disconnected, switch usb ports, if error persists: <br>
	'lsmod | grep ftdi_sio'
		
3. If above command returns nothing: <br>
	'sudo modprobe ftdi_sio' <br>
	run 2. again <br>
	run 1. again <br>
	You shold see outputs

4. Open python environment: <br>
   	go to directory /home/rhig <br>
   	'source translation/bin/activate'

5. Ready to run python script: <br>
	click top right play button drop down menu, "Run Python File" <br>
	if error, run sudo in front of the code 

6. If there are underlined import errors: <br>
   	'pip install pyserial'

7. Make sure that the script has the right python interpreter selected: <br>
   	press "Ctrl+Shift+P" <br>
	select 'Python: Select Interpreter' <br>
	click "Enter interpreter path..." <br>
	to double check your environment path write in terminal 'which python' when the environment is activated<br>
	paste the above path into the python interpreter path on VSCODE  
	
6. After experiment is done, exist VSCODE or deactivate environment: <br>
   	'deactivate'
