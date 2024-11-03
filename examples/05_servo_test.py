# SPDX-License-Identifier: CC-BY-4.0
# Creative Commons Attribution 4.0 International License
# https://creativecommons.org/licenses/by/4.0/

# Dieses Programm steuert der Servomotor der Auf GPIO10 angeschlossen ist. Der Braune Kabel soll GND.
# Der Servo bewegt sich  in drei Positionen: 0 Grad, 90 Grad und 180 Grad. Die Steuerung erfolgt über den PWM-Ausgang,
# und der Winkel wird durch das Anpassen des Duty Cycles bestimmt.

from time import sleep
import pwmio, board

# PWM-Setup auf dem entsprechenden Pin
pwm = pwmio.PWMOut(board.GP10, frequency=50)  # PWM auf GP10 mit 50 Hz

# Duty-Cycle-Einstellungen für verschiedene Winkel
max_duty = 7864          # Duty Cycle für 180 Grad
min_duty = 1802          # Duty Cycle für 0 Grad
half_duty = int(max_duty / 2)  # Duty Cycle für 90 Grad

try:
    while True:
        # Servo auf 0 Grad drehen
        pwm.duty_cycle = min_duty
        print("0 Grad drehen")
        sleep(2)  # 2 Sekunden warten

        # Servo auf 90 Grad drehen
        pwm.duty_cycle = half_duty
        print("90 Grad drehen")
        sleep(2)  # 2 Sekunden warten

        # Servo auf 180 Grad drehen
        pwm.duty_cycle = max_duty
        print("180 Grad drehen")
        sleep(2)  # 2 Sekunden warten

except KeyboardInterrupt:
    print("Tastaturabbruch erkannt")
    # PWM ausschalten
    pwm.deinit()# Write your code here :-)
