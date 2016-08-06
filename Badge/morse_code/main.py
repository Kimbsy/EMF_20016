### Author: Dave Kimber <https://github.com/Kimbsy>
### License: MIT
### Appname: Morse Code
### Description: Convert text to morse code.

import re
import pyb
import dialogs
import ugfx
import buttons

ugfx.init()
buttons.init()
buttons.disable_menu_reset()

# Map the latin alphabet to Morse code.
morse_map = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
}

# Set up the global timer.
t4 = pyb.Timer(4, freq=100, mode=pyb.Timer.CENTER)
t4.freq(440)

# Output a dot.
def dot():
    ch1 = t4.channel(1, pyb.Timer.PWM, pin=pyb.Pin("BUZZ"), pulse_width=(t4.period() + 1) // 2)
    pyb.delay(100)
    pyb.Pin("BUZZ", pyb.Pin.OUT).low()
    pyb.delay(100)
    
# Output a dash.
def dash():
    ch1 = t4.channel(1, pyb.Timer.PWM, pin=pyb.Pin("BUZZ"), pulse_width=(t4.period() + 1) // 2)
    pyb.delay(200)
    pyb.Pin("BUZZ", pyb.Pin.OUT).low()
    pyb.delay(100)

# Output the space between letters.
def letter_space():
    pyb.delay(200)

# Output the space between words.
def word_space():
    pyb.delay(400)

# Output a single letter in Morse code.
def convert_letter(letter):
    # Only convert alphanumeric characters.
    if letter in morse_map:
        morse = morse_map[letter]
        for char in morse:
            if char == ".":
                dot()
            else:
                dash()

# Output a string in Morse code.
def convert_string(string):
    words = string.split()
    for word in words:
        for letter in word:
            convert_letter(letter)
            letter_space()
        word_space()


# Get string input from user.
string = dialogs.prompt_text("Enter string to convert", init_text="", width = 310, height = 220)

if string:
    ugfx.area(0, 0, ugfx.width(), ugfx.height(), 0)
    ugfx.text(30, 60, "Morse Code...", 0xFFFF)
    convert_string(string.upper())
