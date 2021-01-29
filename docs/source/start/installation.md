# Installation #

Make sure you full filled the [requirements](./requirements.html) before going any further.

You can now running the installation of python module with setup.py. It will :
* Install [LIBSVM](https://github.com/ocampor/libsvm). A python binding to libsvm.
* Install [python-crfsuite](https://python-crfsuite.readthedocs.io/en/latest/#). A smart python binding to crfsuite. 
* Install [lxml](https://lxml.de/), python libraries to process xml document. 

## Stable version ##
To install the last stable version on a Unix system, open a console and enter:


```console
git clone https://github.com/openedition/bilbo2.git
cd bilbo2
git checkout `git describe --tags --abbrev=0`
python3 setup.py install --user
```

## Development version ##
If you wish to install the development version, open a console and enter:
```console
git clone https://github.com/openedition/bilbo2.git
cd bilbo2
python3 setup.py install --user
```


## Uninstall bilbo2 ##

For uninstall bilbo2:
```bash
pip3 uninstall bilbo2
```

For remove and clean your local bilbo2 repositories: 

```bash
cd bilbo2
rm -rvf build/
rm -rvf bilbo2.egg-info/
rm -rvf dist/
```

Or you can use directly bash script clean.sh.

```bash
./clean.sh
```

Note that you have to replace the **right path** to your repository in the clean.sh script. 

## Optional libraries ##

If you have [jenkins](https://jenkins.io/) installed and you wish to make a continuous integration testing, you need to install a optional libraries to generate xml report. It will fit python unittest report to jenkins format specification  :
```
pip3 install unittest-xml-reporting
```

