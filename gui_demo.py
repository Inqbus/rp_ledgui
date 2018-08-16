#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from sense_hat import SenseHat

import pigpio


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class ColorDialog(QtWidgets.QColorDialog):
    def __init__(self, *args, **kwargs):
        if 'led' in kwargs:
            self.led = kwargs.pop('led')
        super(ColorDialog, self).__init__(*args, **kwargs)
        self.currentColorChanged.connect(self.color_changed)

    def color_changed(self, color):
        t_RGBA = color.getRgb() # (r, g, b, a)
        t_RGB = t_RGBA[0:3]
        self.led.set_RGBA(t_RGBA)


RED = 'red'
GREEN = 'green'
BLUE = 'blue'
WHITE = 'white'

LED_GPIO = { RED : 17, GREEN : 22, BLUE : 24, WHITE : 27 }

COLORS = [RED, GREEN, BLUE, WHITE]

class LEDController(object):

    def __init__(self):
        self.pio = pigpio.pi()
        self.set_black()

    def set_black(self):
        for color in COLORS:
            gpio = LED_GPIO[color]
            self.pio.set_PWM_dutycycle( gpio, 0)

    def set_RGBA(self, RGBA):
        print(RGBA)
        for color, value in zip(COLORS, RGBA):
            if color == WHITE:
                value = 0
            gpio = LED_GPIO[color]
            self.pio.set_PWM_dutycycle( gpio, value)

    def stop_io(self):
        self.set_black()
        self.pio.stop()

def main():
    led = LEDController()

    app = QtWidgets.QApplication(sys.argv)
    color_dlg = ColorDialog(led=led)
    color_dlg.open()
    exit_code = app.exec_()

    led.stop_io()

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
