import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler

import displayio
import terminalio
import busio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

keyboard = KMKKeyboard()

keyboard.row_pins = (board.D2, board.D3, board.D6, board.D7)   
keyboard.col_pins = (board.D10, board.D9, board.D8)            
keyboard.diode_orientation = DiodeOrientation.COL2ROW


keyboard.keymap = [
    [
        KC.N1, KC.N2, KC.N3,
        KC.N4, KC.N5, KC.N6,
        KC.N7, KC.N8, KC.N9,
        KC.N10, KC.N11, KC.N12,
    ]
]

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.D0, board.D1, None, False),)  
encoder_handler.map = [((KC.VOLU, KC.VOLD),)]
keyboard.modules.append(encoder_handler)

displayio.release_displays()
i2c = busio.I2C(board.SCL, board.SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

splash = displayio.Group()
display.root_group = splash
text_area = label.Label(terminalio.FONT, text="Hackpad", x=35, y=15)
splash.append(text_area)

if __name__ == '__main__':
    keyboard.go()
