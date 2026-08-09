"""
Hack Club Stardance Hackpad — KMK firmware
Board: Seeed XIAO RP2040

Pin mapping below is taken directly from the project schematic
(Hackpad_for_stardance.kicad_sch / U1 MODULE-SEEEDUINO-XIAO):

  XIAO pin | Net      | board.<name>
  ---------|----------|--------------
  1        | GPIO 1   | D0   (rotary encoder A)
  2        | GPIO 2   | D1   (rotary encoder B)
  3        | ROW 1    | D2
  4        | ROW 2    | D3
  5        | SDA      | SDA  (OLED)
  6        | SCL      | SCL  (OLED)
  7        | ROW 3    | D6
  8        | ROW 4    | D7
  9        | COL 3    | D8
  10       | COL 2    | D9
  11       | COL 1    | D10
  12       | 3V3      | —
  13       | GND      | —
  14       | 5V       | —

The rotary encoder (SW2) only breaks out A/B/common — there's no
push-button pin on this encoder, so it's rotation-only (volume up/down).

12-key matrix (4 rows x 3 cols), each intersection through a 1N4148
diode. Keys are mapped to number keys 1-12, left-to-right / top-to-
bottom, matching the physical layout on the top plate.
"""
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

# --- Key matrix (4 rows x 3 cols = 12 keys) -----------------------------
keyboard.row_pins = (board.D2, board.D3, board.D6, board.D7)   # ROW1-4
keyboard.col_pins = (board.D10, board.D9, board.D8)            # COL1-3
keyboard.diode_orientation = DiodeOrientation.COL2ROW
# If keys register on the wrong row/col or don't register at all,
# flip this to DiodeOrientation.ROW2COL — depends on which way the
# diode cathodes face on the physical board.

keyboard.keymap = [
    [
        KC.N1, KC.N2, KC.N3,
        KC.N4, KC.N5, KC.N6,
        KC.N7, KC.N8, KC.N9,
        KC.N10, KC.N11, KC.N12,
    ]
]

# --- Rotary encoder: volume up/down (rotation only, no click) ----------
encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.D0, board.D1, None, False),)  # (pin_a, pin_b, button, is_inverted)
encoder_handler.map = [((KC.VOLU, KC.VOLD),)]
keyboard.modules.append(encoder_handler)

# --- OLED: static "Hackpad" splash --------------------------------------
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
