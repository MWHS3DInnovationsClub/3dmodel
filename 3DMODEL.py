# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import time
import RPi.GPIO as GPIO
import os
import Adafruit_MPR121.MPR121 as MPR121
from multiprocessing import Process

# Thanks to Scott Garner & BeetBox!
# https://github.com/scottgarner/BeetBox/

print 'Adafruit MPR121 Capacitive Touch Audio Player Test'

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

# Alternatively, specify a custom I2C address such as 0x5B (ADDR tied to 3.3V),
# 0x5C (ADDR tied to SDA), or 0x5D (ADDR tied to SCL).
#cap.begin(address=0x5B)

# Also you can specify an optional I2C bus with the bus keyword parameter.
#cap.begin(busnum=1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SOUND_MAPPING = {
  0: 'awing.m4a',
  1: 'bwing.m4a',
  2: 'cwing.m4a',
  3: 'dwing.m4a',
  4: 'ewing.m4a',
  5: 'awinggym.m4a',
  6: 'bwinggym.m4a',
  7: 'cwinggym.m4a',
  8: 'specgym.m4a',
  9: 'hwing.m4a',
  10: 'swimmingpool.m4a',
  11: 'rotunda.m4a',
}

LIGHT_MAPPING = {
  0: 21,
  1: 17,
  2: 27,
  3: 5,
  4: 22,
  5: 6,
  6: 13,
  7: 26,
  8: 18,
  9: 23,
  10: 24,
  11: 25,
}

def light(pin):
    gp = LIGHT_MAPPING[pin]
    GPIO.setup(gp,GPIO.OUT)
    print "LED on"
    GPIO.output(gp,GPIO.HIGH)

def sound(pin):
    os.system('omxplayer --threshold 0 -o hdmi /home/pi/Music/' + SOUND_MAPPING[pin])
    print"LED off"
    GPIO.output(gp,GPIO.LOW)

def sound2(pin):
    os.system('omxplayer --threshold 0 -o hdmi /home/pi/Music/low' + SOUND_MAPPING[pin])
    print"LED off"
    GPIO.output(gp,GPIO.LOW)

# Main loop to print a message every time a pin is touched.
print('Press Ctrl-C to quit.')
last_touched = cap.touched()
while True:
    current_touched = cap.touched()
    # Check each pin's last and current state to see if it was pressed or released.
    for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        # First check if transitioned from not touched to touched.
        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} touched!'.format(i))
            if i == k:
                if __name__ == '__main__':
                p1 = Process(target = light, args = (i,))
                p1.start()
                p2 = Process(target = sound2, args = (i,))
                p2.start()
                k = -1
            else
                if __name__ == '__main__':
                    p1 = Process(target = light, args = (i,))
                    p1.start()
                    p2 = Process(target = sound, args = (i,))
                    p2.start()
                if i in [0,1,2,4]
                    k = i
                else
                    k = -1
                os.system('omxplayer --threshold 0 -o hdmi /home/pi/Music/more.mp3')
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))

    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.1)
