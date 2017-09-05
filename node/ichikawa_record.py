#!/usr/bin/env python

import commands
import rospy
import sys
import time

def record():
    check = commands.getoutput("arecord -d 4 SSL/check/test-1-1.wav")
