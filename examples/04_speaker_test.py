# SPDX-License-Identifier: CC-BY-4.0
# Creative Commons Attribution 4.0 International License
# https://creativecommons.org/licenses/by/4.0/

# Dieses Programm steuert eine LED-Leiste (NeoPixels) und gibt bei Berührung eines
# Touchpads einen Ton über einen Lautsprecher aus. Die Frequenz des Tons erhöht sich
# bei Berührung des rechten Touchpads und verringert sich bei Berührung des linken Touchpads.
# Die LED-Farbe zeigt den Status der Berührung an.

import time
import board
import neopixel
import touchio
from adafruit_debouncer import Button
import pwmio

# Setup für NeoPixels
pixel_pin = board.GP12             # Pin, an den die NeoPixels angeschlossen sind
num_pixels = 4                     # Anzahl der NeoPixels
ORDER = neopixel.GRB               # Farbordnung der NeoPixels (GRB)
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Farbe auf Blau setzen und anzeigen
pixels.fill((0, 0, 255))
pixels.show()

# Touch-Empfindlichkeit und -Setup für zwei Touchpads
THRESHOLD = 1000                    # Schwellenwert für Touch-Empfindlichkeit
t_r = touchio.TouchIn(board.GP16)
t_r.threshold = t_r.raw_value + THRESHOLD
touchpad_r = Button(t_r, value_when_pressed=True)

t_l = touchio.TouchIn(board.GP14)
t_l.threshold = t_l.raw_value + THRESHOLD
touchpad_l = Button(t_l, value_when_pressed=True)

# PWM-Setup für Tonausgabe (Lautsprecher verbunden mit GP20)
pwm = pwmio.PWMOut(board.GP20, duty_cycle=2 ** 15, variable_frequency=True)

def play_tone(frequency, duration=0.5):
    """
    Spielt einen Ton mit der angegebenen Frequenz und Dauer.

    Parameter:
    frequency (int): Frequenz des Tons in Hertz.
    duration (float): Dauer des Tons in Sekunden.
    """
    pwm.frequency = frequency
    time.sleep(duration)
    pwm.duty_cycle = 0  # Ton ausschalten nach Ablauf der Dauer

# Hauptschleife zur Steuerung der LEDs und Tonfrequenz basierend auf Berührungseingaben
frequency = 440  # Startfrequenz in Hz

while True:
    touchpad_r.update()
    touchpad_l.update()

    if touchpad_r.rose:  # Wenn das rechte Touchpad gedrückt wird
        pwm.duty_cycle = 2**15
        pixels.fill((0, 255, 0))  # Farbe auf Grün ändern
        pixels.show()
        frequency += 100  # Erhöht die Frequenz bei Berührung des rechten Pads
        play_tone(frequency, 0.1)  # Ton mit aktueller Frequenz für 0,5 Sekunden abspielen

    elif touchpad_l.rose:  # Wenn das linke Touchpad gedrückt wird
        pwm.duty_cycle = 2**15
        pixels.fill((0, 0, 255))  # Farbe auf Blau ändern
        pixels.show()
        frequency -= 100  # Verringert die Frequenz bei Berührung des linken Pads
        play_tone(frequency, 0.1)  # Ton mit aktueller Frequenz für 0,5 Sekunden abspielen

    elif touchpad_r.fell or touchpad_l.fell:  # Wenn Berührung an einem der Pads losgelassen wird
        pixels.fill((255, 0, 0))  # Farbe auf Rot ändern
        pixels.show()
        pwm.duty_cycle = 0  # Ton ausschalten
