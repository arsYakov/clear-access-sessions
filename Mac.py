import pandas as pd
from netmiko import Netmiko
from netmiko import ConnectHandler
from pandas import DataFrame
import concurrent.futures
import easygui

# CLI PARAMETERS:
USERNAME = ''
PASS = ''
ENABLE = ''

def clear_access_session(switchip):
	try:
		login = {
   		"host": switchip,
   		"username": USERNAME,
   		"password": PASS,
   		"device_type": "cisco_ios",
   		"secret": ENABLE}
		net_connect = Netmiko(**login)
		net_connect.enable()
		for mac in maclist[switchip]:
			print(f'Clearing Access for {mac} on {switchip}')
			command = f"clear access-session mac {mac}"
			net_connect.send_command(command)
		net_connect.disconnect()
	except:
		print(f'{switchip} had a problem')

def main():
	macDF = pd.read_excel(easygui.fileopenbox())

	for ip,mac in zip(macDF['NAS-IP-Address'],macDF['MACAddress']):
		if ip not in maclist:
			maclist[ip] = [mac]
		else:
			maclist[ip].append(mac)

	with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
		executor.map(clear_access_session,maclist.keys())

if __name__ == '__main__':
	# Creating empty dict to hold data to process
	maclist = {}
	main()
