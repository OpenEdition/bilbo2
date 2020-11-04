#!/bin/bash
python3 -m pip uninstall bilbo2 -y
cd /data/bilbo2
rm -rvf build/
rm -rvf bilbo2.egg-info
rm -rvf dist
