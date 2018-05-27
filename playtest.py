import sys
import time
import pygame
import RPi.GPIO as GPIO

import Adafruit_MPR121.MPR121 as MPR121

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

# Define mapping of capacitive touch pin presses to sound files
# tons more sounds are available but because they have changed to .flac in /opt/sonic-pi/etc/samples/ some will not work
# more .wav files are found in /usr/share/scratch/Media/Sounds/ that work fine this example uses Aniamal sounds.

SOUND_MAPPING = {
  0: '/opt/sonic-pi/etc/samples/dwing.flac',
  1: '/opt/sonic-pi/etc/samples/cwing.flac',
  2: '/opt/sonic-pi/etc/samples/dwing.flac',
  3: '/opt/sonic-pi/etc/samples/bass_dnb_f.flac',
  4: '/opt/sonic-pi/etc/samples/bass_hit_c.flac',
  5: '/opt/sonic-pi/etc/samples/elec_plip.flac',
  6: '/opt/sonic-pi/etc/samples/bass_trance_c.flac',
  7: '/opt/sonic-pi/etc/samples/vinyl_backspin.flac',
  8: '/opt/sonic-pi/etc/samples/elec_soft_kick.flac',
  9: '/opt/sonic-pi/etc/samples/elec_tick.flac',
  10: '/opt/sonic-pi/etc/samples/vinyl_rewind.flac',
  11: '/opt/sonic-pi/etc/samples/elec_twang.flac',
}

sounds = [0,0,0,0,0,0,0,0,0,0,0,0]

for key,soundfile in SOUND_MAPPING.iteritems():
        sounds[key] =  pygame.mixer.Sound(soundfile)
        sounds[key].set_volume(1);
        
LIGHT_MAPPING = {
  0: 4,
  1: 17,
  2: 27,
  3: 22,
  4: 5,
  5: 6,
  6: 13,
  7: 19,
  8: 26,
  9: 18,
  10: 23,
  11: 24,
}

lights = [0,0,0,0,0,0,0,0,0,0,0,0]

for key,gpiopin in LIGHT_MAPPING.iteritems():
        lights[key] = gpiopin

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
            if (sounds[i]):
                sounds[i].play()
            if (lights[i]):
                GPIO.setup(gpiopin,GPIO.OUT)
                print "LED on"
                GPIO.output(gpiopin,GPIO.HIGH)
                time.sleep(5)
                print "LED off"
                GPIO.output(gpiopin,GPIO.LOW)
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))

    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.1)

    # Alternatively, if you only care about checking one or a few pins you can
    # call the is_touched method with a pin number to directly check that pin.
    # This will be a little slower than the above code for checking a lot of pins.
    #if cap.is_touched(0):
    #    print('Pin 0 is being touched!')
