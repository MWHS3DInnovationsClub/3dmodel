#Forked from Tony DiCola's starter code w/ Adafruit Industries
import sys
import time
import RPi.GPIO as GPIO
import os
import Adafruit_MPR121.MPR121 as MPR121
import threading

# Create MPR121 instance.
cap = MPR121.MPR121()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#SOUND_MAPPING
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

#LIGHT_MAPPING
LIGHT_MAPPING = {
  0: 21,
  1: 17,
  2: 27,
  3: 5,
  4: 22,
  5: 13,
  6: 6,
  7: 26,
  8: 18,
  9: 23,
  10: 24,
  11: 25,
}

globalPin = -1

def light(pin):
    gp = LIGHT_MAPPING[pin]
    globalPin = pin
    GPIO.setup(gp,GPIO.OUT)
    print("LED on")
    GPIO.output(gp,GPIO.HIGH)

def sound(pin,x=''):
    gp = LIGHT_MAPPING[pin]
    GPIO.setup(gp, GPIO.OUT)
    os.system('omxplayer --threshold 0 -o both /home/pi/Music/'+x+ + SOUND_MAPPING[pin])
    print("LED off")
    GPIO.output(gp,GPIO.LOW)

def sound2(pin):
    sound(pin, 'low')

def sound3(pin):
   sound(pin, 'ss')

last_touched = cap.touched()
			
k = -1
j = -1
# Main loop to print a message every time a pin is touched.
print('Press Ctrl-C to quit.')
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
		if  i != j  and k == -1:
	        	if __name__ == '__main__':
                                t1 = threading.Thread(target = light, args = (i,))
                                t2 = threading.Thread(target = sound3, args = (i,))
                                t2.start()
				t1.start()
                                j = i
                                t1.join()
                                t2.join()
                                os.system('omxplayer --threshold 0 -o both /home/pi/Music/more.mp3')		
		elif i == k:
                	if __name__ == '__main__':
                    		t1 = threading.Thread(target = light, args = (i,))
                                t2 = threading.Thread(target = sound2, args = (i,))
                                t2.start()
				t1.start()
                	    	k = -1
				t1.join()
                                t2.join()
		else:
                	if __name__ == '__main__':
                    		t1 = threading.Thread(target = light, args = (i,))
                                t2 = threading.Thread(target = sound, args = (i,))
                                t2.start()
				t1.start()
				t1.join()
                                t2.join()
				j = - 1
                	if i in [0,1,2,4]:
                		k = i
				os.system('omxplayer --threshold 0 -o both /home/pi/Music/more.mp3')			
                	else:
                		k = -1
	if not current_touched & pin_bit and last_touched & pin_bit:
		print('{0} released!'.format(i))

    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.1)
