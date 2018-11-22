import os
import sys
import stat
import shutil
import time
from subprocess import call
import fileinput
from config import *

def processDevices(devices):
	for deviceUUID, device in devices.items():
		if not 'nickname' in device:
			device['nickname'] = deviceUUID[:8]


def editFile(file_path, target, new_value):
	print('Editing file: ' + file_path)

	# Read in the file
	with open(file_path, 'r') as file :
	  filedata = file.read()

	# Replace the target string
	filedata = filedata.replace(target, new_value)

	# Write the file out again
	with open(file_path, 'w') as file:
		file.write(filedata)


def getDirName(nickname):
	return relPath + "{}-RDM".format(nickname)


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def make():
	# Clone the base repo
	print('Cloning repo...')
	dir = relPath + "RealDeviceMap-UIControl"
	os.system("git clone " + repoUrl + " ./" + dir)
	os.chdir(dir)
	print('Running pod install...')
	os.system('pod install')
	os.chdir('..')


def buildAll(devices):
	numDevices = len(devices)
	numDone = 1

	for deviceUUID, device in devices.items():
		deviceName = device['nickname']
		print('Building instance {} out of {}'.format(numDone, numDevices))

		dir = getDirName(deviceName)
		build(dir)
		editFile(dir + '/RealDeviceMap-UIControl/Config.swift', 'DEVICE_UUID', deviceName)
		editFile(dir + '/RealDeviceMap-UIControl/Config.swift', 'http://RDM_UO:9001', backendURLBaseString)
		editFile(dir + '/run.py','DEVICE_UUID', deviceUUID)
		
		if isinstance(device,dict) and 'account_manager' in device and device['account_manager'] == True:
			editFile(dir + '/RealDeviceMap-UIControl/Config.swift', 'class Config: ConfigProto {', 'class Config: ConfigProto {\n\tvar enableAccountManager = true\n')
			
		if isinstance(device,dict) and 'ilocation' in device:
			editFile(dir + '/spoof.py','DEVICE_UUID', deviceUUID)
			editFile(dir + '/spoof.py','http://DEVICE_IP:8080/loc', 'http://{}:8080/loc'.format(device['ilocation']))

		os.chdir(dir)
		print('Running pod install...')
		os.system('pod install')

		print('Deleting old project files...')
		shutil.rmtree('RealDeviceMap-UIControl.xcodeproj', onerror=remove_readonly)
		shutil.rmtree('RealDeviceMap-UIControl.xcworkspace', onerror=remove_readonly)
		os.chdir(os.path.dirname(os.path.realpath(__file__)))

		print('Copying project files...')
		shutil.copytree(relPath + 'RealDeviceMap-UIControl/RealDeviceMap-UIControl.xcodeproj', dir + '/RealDeviceMap-UIControl.xcodeproj')
		shutil.copytree(relPath + 'RealDeviceMap-UIControl/RealDeviceMap-UIControl.xcworkspace', dir + '/RealDeviceMap-UIControl.xcworkspace')
		numDone += 1
		

def build(dir):
	if os.path.exists(dir):
		print("Deleting directory {}...".format(dir))
		shutil.rmtree(dir, onerror=remove_readonly)

	print("Cloning repo in {}...".format(dir))
	os.system("git clone " + repoUrl + " ./" + dir)


def launch(bashScript, script, dir, sessionName):
	scriptData = """
	#!/bin/bash
	cd {0}
	cd {1}
	echo "Launching {2}..."
	screen -S {3} python {2}
	""".format(os.path.dirname(os.path.realpath(__file__)), dir, script, sessionName)

	with open(bashScript, 'w') as file:
		file.write(scriptData)

	os.system('chmod +x ' + bashScript)

	os.system('open -a Terminal.app ' + bashScript)

def startAll(devices):
	numDevices = len(devices)
	numDone = 1

	for deviceUUID, device in devices.items():
		deviceName = device['nickname']
		print('Initializing {}...'.format(deviceName))
		print('Instance {} out of {}'.format(numDone, numDevices))
		dir = getDirName(deviceName)

		launchScript = deviceName + ".launch.command"

		print('Launching run.py...')
		#os.chdir(dir)
		#os.system('screen -dmS {} python run.py'.format(deviceName))
		#os.chdir(os.path.dirname(os.path.realpath(__file__)))
		launch(launchScript, 'run.py', dir, deviceName)

		if isinstance(device,dict) and 'ilocation' in device:
			print('Launching spoof.py...')
			time.sleep(5)
			launch(launchScript, 'spoof.py', dir)

		if numDone < numDevices:
			print("Waiting for {} seconds to start the next instance".format(startDelay))
			time.sleep(startDelay)
		
		numDone += 1


def stopAll(devices):
	numDevices = len(devices)
	numDone = 1

	for deviceUUID, device in devices.items():
		deviceName = device['nickname']
		print('Stopping {}...'.format(deviceName))
		print('Instance {} out of {}'.format(numDone, numDevices))

		os.system('screen -X -S {} quit'.format(deviceName))
		print('{} is stopped.'.format(deviceName))


def getDeviceId(device_id):
	if device_id in devices:
		# UUID found
		return device_id
	else:
		# Look for nickname instead
		for deviceUUID, device in devices.items():
			if device['nickname'] == device_id:
				# UUID found
				return deviceUUID
	return None


processDevices(devices)