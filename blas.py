#!/usr/bin/env python

from RPi import GPIO
from pdtone import PDTone
import signal, time

GPIO.setmode(GPIO.BCM)

# Start and connect to PD
tone = PDTone()

# Store all the tunes here, as lists with format (note, duration)
tunes = {
  'Tune 0': [('a',0.5),('a',0.5),('b',0.5),('c',0.5)],
  'Tune 1': [('a',1),('a#',0.5),('d',1)],
  'Tune 2': [('c',0.5),('d',0.5),('e',0.5)],
  'Tune 3': [('a',0.5),('a#',0.5),('b',0.5),('c',0.5)]
}

# How many attempts does a player get at each tune
player_lives = 2
lives = player_lives
steps = []
running = None
current_tune = None
current_tune_idx = 0 # Start at tune 0

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
  """
  Handle a button press, add it to the list of
  steps and play the corresponding tone
  """
  global steps, current_tune, running
  if not running:
    return False
  button = pins.index(pin)
  print("Pressed button: " + str(button))
  print("Notes: " + str(get_notes(pin)))
  steps.append(pin)
  if check_progress():
    note = tunes[current_tune][len(steps)-1]
    tone.tone(notes[note[0]][0])
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

def setup_output():
  """
  Switch all our pins to OUTPUT mode and
  remove any event detection
  """
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
  """
  Switch all pins to INPUT mode and add event handlers
  to catch our button presses
  """
  for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=handle_button, bouncetime=500)

def play_note((note,duration)):
  """ 
  Play a single note through our PD instance, and
  light its corresponding LED
  """
  f = notes[note][0]
  l = notes[note][1]
  GPIO.output(l, True)
  tone.note(f,duration)
  GPIO.output(l, False)

def check_progress():
  """
  Loop through every button the user has pressed so far
  and check they correspond to the notes in the current tune
  """
  global steps
  for idx, step in enumerate(steps):
    if not tunes[ current_tune ][ idx ][ 0 ] in get_notes(step):
      return False
  return True

while 1:
  current_tune = tunes.keys()[current_tune_idx]
 
  print("Playing " + current_tune + "...")

  # Switch to output mode
  setup_output()

  # Play through each note in the current tune
  for note in tunes[ current_tune ]:
    play_note(note)
    time.sleep(0.1)

  # Switch to input mode
  setup_input()
  
  steps = []
  failed = False
  running = True
  
  # Wait for the user to fail, or populate all the steps
  while check_progress() and len(steps) < len( tunes[ current_tune ] ): 
    pass
  running = False

  #  Wait until user releases all buttons
  for pin in pins:
    while GPIO.input(pin) == False:
      pass
    
  # Check if user has succeeded or failed
  if check_progress():
    print("Clever girl...")

    # Play success tone!
    for t in range(6):
      n = notes[notes_keys[t]][0]
      dur = 0.125
      if t == 5:
        dur = 0.5
      tone.note(n,dur)
    
    # Progress to the next tune
    current_tune_idx += 1
    if current_tune_idx >= len(tunes):
      current_tune_idx = 0
      print("You've made it!")
      print("Press the left button to continue...")
      while GPIO.input(pins[0]):
        pass
  else:
    print("What have you done!?")
    
    # Play fail tone
    for t in range(6):
      n = notes[notes_keys[6-t]][0]
      dur = 0.125
      if t == 5:
        dur = 0.5
      tone.note(n,dur)

    lives -= 1
    print(str(lives) + " lives left!")
    if lives == 0:
      lives = player_lives
      print("Whoops, you ran out of lives!")
      print("But you got to tune " + str(current_tune_idx))
      current_tune_idx = 0

  time.sleep(1)
  print("Get ready...")
  time.sleep(1)
