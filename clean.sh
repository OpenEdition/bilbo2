#!/bin/bash
pip3 uninstall bilbo2 -y
cd /home/user/bilbo2
rm -rvf build/
rm -rvf bilbo2.egg-info
rm -rvf dist
