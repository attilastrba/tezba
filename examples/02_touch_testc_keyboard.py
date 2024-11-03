# SPDX-License-Identifier: CC-BY-4.0
# Creative Commons Attribution 4.0 International License
# https://creativecommons.org/licenses/by/4.0/

# Dieses Programm steuert eine LED-Leiste (NeoPixels) und eine angeschlossene Tastatur
# über Touch-Eingaben auf einem Mikrocontroller. Bei Berührung einer der Touchpads
# auf dem Mikrocontroller werden die NeoPixels in eine bestimmte Farbe gesetzt,
# und ein entsprechender Tastendruck (z. B. "A", "D", "W", "S") an den angeschlossenen
# Computer gesendet. Zusätzlich kann ein Regenbogeneffekt auf den LEDs angezeigt werden,
# wenn das untere Touchpad aktiviert wird.

import time
import board
import neopixel
import touchio
from adafruit_debouncer import Button
import usb_hid
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_de import KeyboardLayout
from adafruit_hid.keycode import Keycode

# Initialisierung der Tastatur und Layout für deutsche Tastatur
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayout(keyboard)

# Setup für NeoPixels
pixel_pin = board.GP12            # Pin, an den die NeoPixels angeschlossen sind
num_pixels = 4                    # Anzahl der NeoPixels
ORDER = neopixel.GRB              # Farbordnung der NeoPixels (GRB)
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Farbe auf Blau setzen und anzeigen
pixels.fill((0, 0, 255))
pixels.show()

# Touch-Empfindlichkeit und -Setup
THRESHOLD = 1000                  # Schwellenwert für Touch-Empfindlichkeit
t_r = touchio.TouchIn(board.GP16)
t_r.threshold = t_r.raw_value + THRESHOLD
touchpad_r = Button(t_r, value_when_pressed=True)

t_l = touchio.TouchIn(board.GP14)
t_l.threshold = t_l.raw_value + THRESHOLD
touchpad_l = Button(t_l, value_when_pressed=True)

t_u = touchio.TouchIn(board.GP15)
t_u.threshold = t_u.raw_value + THRESHOLD
touchpad_u = Button(t_u, value_when_pressed=True)

t_d = touchio.TouchIn(board.GP17)
t_d.threshold = t_d.raw_value + THRESHOLD
touchpad_d = Button(t_d, value_when_pressed=True)

def wheel(pos):
    """
    Gibt eine Farbe aus dem Regenbogenspektrum für eine gegebene Position zurück.

    Parameter:
    pos (int): Position im Bereich 0 bis 255, die eine bestimmte Farbe im Regenbogen darstellt.

    Rückgabewert:
    tuple: Ein Tupel mit drei Werten für Rot, Grün und Blau.

    Ablauf:
    - Die Funktion unterteilt das Farbspektrum in drei Hauptsegmente (Rot zu Grün, Grün zu Blau, Blau zu Rot).
    - Abhängig von der Position wird die entsprechende Farbe berechnet und zurückgegeben.
    """
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbow_cycle(wait):
    """
    Führt einen Regenbogeneffekt auf den NeoPixels aus, bei dem die Farben kontinuierlich durchlaufen.

    Parameter:
    wait (float): Zeitverzögerung zwischen den Farbwechseln in Sekunden.

    Ablauf:
    - Die Funktion durchläuft 255 Schritte und berechnet für jeden Pixel eine Farbe,
      um einen sanften Übergang durch den Regenbogen zu erzeugen.
    - Die Farben werden nach jedem Schritt angezeigt und eine kurze Zeit gewartet,
      bevor der nächste Farbwechsel erfolgt.
    """
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

# Hauptschleife zur Steuerung der NeoPixels und Tastaturereignisse
while True:
    touchpad_l.update()
    if touchpad_l.rose:  # Wenn der linke Touchpad aktiviert wird
        pixels.fill((255, 0, 0))  # Farbe auf Rot setzen
        pixels.show()
        keyboard.send(Keycode.A)  # Sendet die Taste "A"

    touchpad_r.update()
    if touchpad_r.rose:  # Wenn der rechte Touchpad aktiviert wird
        pixels.fill((0, 255, 0))  # Farbe auf Grün setzen
        pixels.show()
        keyboard.send(Keycode.D)  # Sendet die Taste "D"

    touchpad_u.update()
    if touchpad_u.rose:  # Wenn der obere Touchpad aktiviert wird
        pixels.fill((0, 255, 255))  # Farbe auf Cyan setzen
        pixels.show()
        keyboard.send(Keycode.W)  # Sendet die Taste "W"

    touchpad_d.update()
    if touchpad_d.rose:  # Wenn der untere Touchpad aktiviert wird
        rainbow_cycle(0.001)  # Regenbogen-Effekt für 1 ms Verzögerung pro Schritt
        pixels.fill((255, 255, 0))  # Farbe auf Gelb setzen
        pixels.show()
        keyboard.send(Keycode.S)  # Sendet die Taste "S"# Write your code here :-)
