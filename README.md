Babbage Lights & Sounds
-----------------------

A re-imagining of the classic Simon game, challenging you to remember and repeat the pattern of lights and sounds!

Requirements
------------

You'll need pd installed, that's what we use to create lovely tones to accompany your lights. You should also plug in a pair of headphones or speakers.

    sudo apt-get install pd

Giving it a go!
---------------

The lights and sounds game will play a variety of tunes, and challenge you to repeat them by pressing the buttons next to the corresponding lights.

Get it wrong and you lose a life, get it right and you progress to the next tune!

Are you a musical ninja, or a tone-deaf sea-dog, give it a try and find out!

    sudo ./blas.py

Making it your own
------------------

We've tried to comment everything so you can make changes. You'll probably want to start with changing the list of tunes.

A tune is a list of tuples containing the musical note ( from the notes list ) and the duration ( in seconds ). Here's an example:

    [('a',0.5),('a',0.5),('b',0.5),('c',0.5)]
