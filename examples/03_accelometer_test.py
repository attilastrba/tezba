# SPDX-License-Identifier: CC-BY-4.0
# Creative Commons Attribution 4.0 International License
# https://creativecommons.org/licenses/by/4.0/

# Dieses Programm steuert eine LED-Leiste (NeoPixels) basierend auf der Neigung eines
# Beschleunigungssensors (LSM6DS3). Die LEDs leuchten in verschiedenen Farben auf, je nach
# Neigungsrichtung entlang der X- und Y-Achse: Links/rechts werden Rot/Grün und
# Vorwärts/rückwärts Blau/Gelb angezeigt. Zusätzlich werden die aktuellen X-, Y- und Z-Werte
# des Sensors über den Serial Logger ausgegeben, um die Neigung in Echtzeit zu überwachen.

import time
import board
import busio
import neopixel
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

# Initialisierung des I2C-Busses und des Beschleunigungssensors
i2c = busio.I2C(scl=board.GP7, sda=board.GP6)
sensor = LSM6DS3(i2c)

# Setup für NeoPixels
pixel_pin = board.GP12              # Pin für die NeoPixels
num_pixels = 4                      # Anzahl der NeoPixels
ORDER = neopixel.GRB                # Farbordnung (RGB oder GRB für NeoPixels)

# Erstellen eines NeoPixel-Objekts
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def update_pixels(x_tilt, y_tilt):
    """
    Aktualisiert die NeoPixels basierend auf der Neigung des Sensors entlang der X- und Y-Achse.

    Parameter:
    x_tilt (float): Neigungswert entlang der X-Achse.
    y_tilt (float): Neigungswert entlang der Y-Achse.

    Ablauf:
    - Die Anzahl der zu beleuchtenden LEDs wird durch den Neigungswert bestimmt.
    - Y-Achse steuert Rot/Grün (links/rechts), X-Achse steuert Blau/Gelb (vorwärts/rückwärts).
    """
    pixels.fill((0, 0, 0))  # Schaltet zunächst alle LEDs aus

    # Berechnet die Anzahl der LEDs, die basierend auf der Neigung beleuchtet werden sollen
    y_num_to_light = int(abs(y_tilt) / 10 * num_pixels)  # Y-Achse bestimmt Rot/Grün
    x_num_to_light = int(abs(x_tilt) / 10 * num_pixels)  # X-Achse bestimmt Blau/Gelb

    # Steuerung der Farben basierend auf Y-Achsen-Neigung (links/rechts)
    if y_tilt < 0:
        # Linksneigung - rote LEDs
        for i in range(y_num_to_light):
            pixels[i] = (255, 0, 0)  # Farbe Rot
    elif y_tilt > 0:
        # Rechtsneigung - grüne LEDs
        for i in range(y_num_to_light):
            pixels[i] = (0, 255, 0)  # Farbe Grün

    # Steuerung der Farben basierend auf X-Achsen-Neigung (vorwärts/rückwärts)
    if x_tilt > 0:
        # Vorwärtsneigung - blaue LEDs
        for i in range(x_num_to_light):
            pixels[i] = (0, 0, 255)  # Farbe Blau
    elif x_tilt < 0:
        # Rückwärtsneigung - gelbe LEDs
        for i in range(x_num_to_light):
            pixels[i] = (255, 255, 0)  # Farbe Gelb

    pixels.show()  # Aktualisiert die Anzeige der NeoPixels

# Hauptschleife
while True:
    # Liest die Beschleunigungswerte entlang der X-, Y- und Z-Achse vom Sensor
    x_tilt, y_tilt, z_tilt = sensor.acceleration

    # Begrenzen der X- und Y-Werte auf den Bereich -10 bis 10 für einfachere Skalierung
    x_tilt = max(min(x_tilt, 10), -10)
    y_tilt = max(min(y_tilt, 10), -10)

    # Ausgabe der Neigungswerte über den Serial Logger
    print(f"Neigungswerte - X-Achse: {x_tilt:.2f}, Y-Achse: {y_tilt:.2f}, Z-Achse: {z_tilt:.2f}")

    # Aktualisiert die NeoPixels basierend auf den Neigungswerten
    update_pixels(x_tilt, y_tilt)

    time.sleep(0.1)  # Kurze Verzögerung für Stabilität# Write your code here :-)
