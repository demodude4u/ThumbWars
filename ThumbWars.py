from sys import path as syspath  # NOQA
syspath.insert(0, '/Games/ThumbWars')  # NOQA

from thumbyGrayscale import display, Sprite
from thumbyButton import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR

from tw_enums import *
from tw_defs import *
from tw_assets import *
from tw_state import *
from tw_draw import *

display.setFPS(30)

state = SS_INTRO
frame = 0

titleUnits = [
    UNIT_INF,
    UNIT_MCH,
    UNIT_RCN,
    UNIT_TNK,
    UNIT_APC,
    UNIT_ART,
]

display.setFont("/lib/font3x5.bin", 3, 5, 2)
while True:
    frame += 1
    display.fill(0)

    if state == SS_INTRO:
        y = -20+frame
        draw_blitFrame(bmpTitle,3,y,0)
        if frame == 20:
            state, frame = SS_START, 0

    elif state == SS_START:
        if frame % 150 < 5:
            f = frame % 150
        else :
            f = 0
        draw_blitFrame(bmpTitle,3,0,f)
        
        if (frame % 30) < 15:
            display.drawText("PRESS  START", 6, 23, 0b01)
        
        unitX = (frame//2) % 100
        unitID = titleUnits[((frame//2) // 100) % len(titleUnits)]
        f = (unitID-1)*3 + (0 if (((unitX)%4)<2) else 1)
        draw_blitMaskedFrame(bmpUnits, unitX-10, 30, f)
        
        if buttonA.justPressed():
            # state, frame = SS_MAP_SELECT, 0
            import tw_game
            break

    elif state == SS_MAP_SELECT:   
        pass

    elif state == SS_RULES_SELECT:
        pass

    display.update()