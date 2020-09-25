#!/bin/bash
pip3 uninstall bilboV2 -y
cd /home/user/bilbo_v2
rm -rvf build/
rm -rvf bilboV2.egg-info
rm -rvf dist
