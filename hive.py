import sys
from common import *

if "-make" in sys.argv:
	make()

elif "-build" in sys.argv:
	buildAll(devices)

elif "-build_one" in sys.argv:
	deviceId = getDeviceId(sys.argv.pop())

	if deviceId is None:
		print("Device not found")
	else:
		device = {deviceId : devices[deviceId]}
		buildAll(device)

elif "-start" in sys.argv:
	startAll(devices)

elif "-start_one" in sys.argv:
	deviceId = getDeviceId(sys.argv.pop())

	if deviceId is None:
		print("Device not found")
	else:
		device = {deviceId : devices[deviceId]}
		startAll(device)

else:
	print("\nHive for RealDeviceMap")
	print("\nUsage: python hive.py -make -build -start")
	print("\t-make\t\tMakes a new RealDeviceMap-UIControl folder to add your provisioning credentials to.")
	print("\t-build\t\tBuilds folders for all devices and edits the files")
	print("\t-start\t\tLaunches each device in its own window and executes python run.py")
	print("\t-start_one\tLaunches a single device in its own window and executes python run.py (Device uuid must be last argument)")

print("\nDone.")