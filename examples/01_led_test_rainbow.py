# SPDX-License-Identifier: CC-BY-3.0
# Creative Commons Attribution 4.0 International License
# https://creativecommons.org/licenses/by/4.0/

# Dieses Programm zeigt einen kontinuierlichen Regenbogeneffekt auf einer NeoPixel-LED-Leiste an,
# indem die LEDs in den Farben des Regenbogens durchlaufen. Die Farben ändern sich schrittweise
# über die Zeit, um einen sanften Übergangseffekt zu erzeugen.

import time
import board
import neopixel

# Setup für NeoPixels
pixel_pin = board.GP12           # Pin, an den die NeoPixels angeschlossen sind
num_pixels = 4                   # Anzahl der NeoPixels
ORDER = neopixel.GRB             # Farbordnung der NeoPixels (Grün, Rot, Blau)
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def rainbow_cycle(wait):
    """
    Zeigt einen Regenbogeneffekt auf den NeoPixels an, bei dem die Farben kontinuierlich durchlaufen.

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
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

def colorwheel(pos):
    """
    Generiert RGB-Werte für eine gegebene Position im Regenbogenspektrum.

    Parameter:
    pos (int): Eine Zahl zwischen 0 und 255, die die Position auf dem Regenbogen angibt.

    Rückgabewert:
    tuple: Ein Tuple mit drei Werten für Rot, Grün und Blau, die die Farbe für die angegebene Position definieren.

    Ablauf:
    - Die Funktion unterteilt den Regenbogen in drei Hauptsegmente (Rot zu Grün, Grün zu Blau, Blau zu Rot).
    - Abhängig von der Position wird die entsprechende Farbe für jedes Segment berechnet und zurückgegeben.
    """
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# Hauptschleife, um den Regenbogeneffekt kontinuierlich zu zeigen
while True:
    # Funktion anrufen und Regenbogeneffekt auf den NeoPixels anzeigen
    rainbow_cycle(0.05)
