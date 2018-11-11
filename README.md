# RealDeviceMap-Hive
Multi-instance manager assistant for RealDeviceMap

# Installation
1. Open a terminal and run `git clone https://github.com/AnnexMap/RealDeviceMap-Hive.git`.
2. Rename `config.example.py` to `config.py` and edit. Add your devices and set the address to your RealDeviceMap backend.
3. In a terminal, navigate to the `RealDeviceMap-Hive` directory that you cloned in step 1.
4. Run `python hive.py -make`.
5. In Xcode, opne the `RealDeviceMap-UIControl` project that was just created in the same parent directory as RealDeviceMap-Hive.
6. In Xcode, set the Signing Team for the Provisioning Profile on the targets RealDeviceMap-UIControl and RealDeviceMap-UIControlTests
7. Save the Xcode project

# Usage
1. In a terminal, in the `RealDeviceMap-Hive` directory, run `python hive.py -build`
2. Run `python hive.py -start` to launch the instances
