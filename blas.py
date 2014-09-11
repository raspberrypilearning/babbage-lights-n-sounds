#!/usr/bin/env python

from RPi import GPIO
from pdtone import PDTone
import signal, time

GPIO.setmode(GPIO.BCM)

# Start and connect to PD
tone = PDTone()

tunes = {
  'Tune 1': [('a',1),('a#',0.5),('d',1)]
}

pins = [22, 23, 24, 25]

current_tune = None
current_tune_idx = None

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
  global steps, current_tune
  button = pins.index(pin)
  print("Pressed button: " + str(button))
  print("Notes: " + str(get_notes(pin)))
  steps.append(pin)
  if check_progress():
    note = tunes[current_tune][len(steps)-1]
    tone.note(notes[note[0]][0],note[1])
  else:
    tone.note(300,0.5)

def get_notes(pin):
  result = []
  for key,note in notes.iteritems():
    if pin == note[1]:
      result.append(key)
  return result

def setup_output():
  for pin in pins:
    try:
      GPIO.remove_event_detect(pin)
    except RuntimeError:
      pass
    try:
      GPIO.setup(pin, GPIO.OUT, initial=False)
    except RuntimeWarning:
      pass

def setup_input():
  for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=handle_button, bouncetime=300)

def play_note((note,duration)):
  f = notes[note][0]
  l = notes[note][1]
  GPIO.output(l, True)
  tone.note(f,duration)
  GPIO.output(l, False)

def check_progress():
  global steps
  for idx, step in enumerate(steps):
    if not tunes[ current_tune ][ idx ][ 0 ] in get_notes(step):
      return False
  return True
 

steps = []

current_tune_idx = 0

while 1:
  current_tune = tunes.keys()[current_tune_idx]
 
  print("Playing " + current_tune + "...")

  setup_output()

  for note in tunes[ current_tune ]:
    play_note(note)

  setup_input()
  
  steps = []
  failed = False
  while check_progress() and len(steps) < len( tunes[ current_tune ] ): 
    pass
    
  if check_progress():
    print("Clever girl...")
  else:
    print("What have you done!?")

  time.sleep(1)
  print("Get ready...")
  time.sleep(1)

  current_tune_idx += 1
  if current_tune_idx >= len(tunes):
    current_tune_idx = 0
