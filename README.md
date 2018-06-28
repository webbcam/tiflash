# TI-Flash

An *unofficial* Python flash programmer for [TI Launchpads](http://www.ti.com/tools-software/launchpads/overview.html).

## Getting Started

TIFlash uses TI's Code Composer Studio scripting interface ([Debug Server Scripting](http://software-dl.ti.com/ccs/esd/documents/users_guide/sdto_dss_handbook.html)) to flash devices. It's essentially a python/command line interface for CCS. This is helpful when just needing to perform simple actions like flashing, erasing or resetting a device without having to spin up an entire CCS GUI session.

Follow the steps below to get TIFlash set up on your computer.


### Prerequisites

You will need to have [Code Composer Studio](http://www.ti.com/tool/CCSTUDIO) installed along with drivers for any devices you plan to use (offered during installation of CCS or available in CCS's Resource Explorer).

You'll also need [Python](https://www.python.org/downloads/) installed on your computer, either 2.7 or 3.6+ (preferred) will work.


### Installing

Install TIFlash via PyPi (*recommended*)

```
pip install tiflash
```

Install via git repo (used for development)

```
git install https://github.com/webbcam/tiflash.git
cd tiflash
pip install -r requirements.txt
pip install -e .
```
### Quickstart
TIFlash can be used via Python directly or using the commandline.

#### Command Line
Installing TIFlash via pip will install the commandline application.

From a command prompt:
```
tiflash -h		# display help menu
tiflash -s L4000CE flash /path/to/image.hex -o ResetOnRestart True
```
For more commandline examples see the [EXAMPLES.md](EXAMPLES.md) file

#### Python
TIFlash can also be used directly in your Python scripts.
```
import tiflash
tiflash.flash(serno='L4000CE', image='/path/to/image.hex', options={'ResetOnRestart':True})
```
For  more python examples see the [EXAMPLES.md](EXAMPLES.md) file

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the process for submitting pull requests to us.

## To Do

Below is a list of features that will be added eventually.

* Add read/write to memory option
* Add read symbols option
* Write wrapper modules for device platform (ie CCFlash, MSPFlash, etc)
* Add Target Detection
* Add Attaching of CCS Session


## Versioning

For the versions available, see the [tags on this repository](https://github.com/webbcam/tiflash/tags).

## Authors

* **Cameron Webb** - *Initial work* - [webbcam](https://github.com/webbcam)

See also the list of [contributors](https://github.com/webbcam/tiflash/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Debug Server Scripting](http://software-dl.ti.com/ccs/esd/documents/users_guide/sdto_dss_handbook.html)

