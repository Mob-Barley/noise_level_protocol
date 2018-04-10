#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import subprocess
import os

from datetime import datetime, timedelta

tomorrow = datetime.now() + timedelta(days=1)
tomorrow_formatted = tomorrow.strftime('%Y%m%d')

os.makedirs("/home/pi/noise/mp3/" + tomorrow_formatted);
print("Path is created")