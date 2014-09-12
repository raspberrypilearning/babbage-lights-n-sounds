#!/usr/bin/env python

from RPi import GPIO
from pdtone import PDTone
import signal, time

GPIO.setmode(GPIO.BCM)

# Start and connect to PD
tone = PDTone()

# Keep an index of our notes, so we can loop through
# them in order for success/failure tunes
notes_keys = ['a','a#','b','c','c#','d','d#','e','f','f#','g','g#']

# Pins for the lights/buttons
pins = [22, 23, 24, 25]

notes = {
	'a':	(440,	pins[0]), 
	'a#':	(466.16,pins[1]), 
	'b':	(493.88,pins[2]), 
	'c': 	(523.25,pins[3]), 
	'c#':	(554.37,pins[0]), 
	'd':	(587.33,pins[1]), 
	'd#':	(622.25,pins[2]), 
	'e':	(659.25,pins[3]), 
	'f':	(698.46,pins[0]), 
	'f#':	(739.99,pins[1]), 
	'g':	(783.99,pins[2]), 
	'g#':	(830.61,pins[3])
	}

def handle_button(pin):
  button = pins.index(pin)

  note = notes[notes_keys[button]]

  print(button, note[0])

  tone.tone(note[0])
  tone.power_on()
  # Hold the tone while the button is held down
  while(GPIO.input(pin) == False):
    pass
  tone.power_off()

def get_notes(pin):
  """
  Get all notes corresponding to a particular
  button, represented by its GPIO pin number
  """
  result = []
  for key,note in notes.iteritems():
    if pin == note[1]:
      result.append(key)
  return result

def setup_input():
  """
  Switch all pins to INPUT mode and add event handlers
  to catch our button presses
  """
  for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=handle_button, bouncetime=100)

setup_input()

while 1:
  pass
