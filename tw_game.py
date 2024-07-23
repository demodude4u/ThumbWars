from sys import path as syspath  # NOQA
syspath.insert(0, '/Games/ThumbWars')  # NOQA

from thumbyGrayscale import display
from thumbyButton import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR

from tw_enums import *
from tw_defs import *
from tw_assets import *
from tw_state import *
from tw_draw import *

mapUnits.append(Unit(2,10,UNIT_ART,TEAM_P1))
mapUnits.append(Unit(5,11,UNIT_INF,TEAM_P1))
mapUnits.append(Unit(2,3,UNIT_RCN,TEAM_P1))
mapUnits.append(Unit(1,6,UNIT_TNK,TEAM_P1))
mapUnits.append(Unit(5,9,UNIT_APC,TEAM_P1))
mapUnits.append(Unit(5,8,UNIT_INF,TEAM_P1))
mapUnits.append(Unit(5,13,UNIT_MCH,TEAM_P1))
mapUnits.append(Unit(6,11,UNIT_INF,TEAM_P2))
mapUnits.append(Unit(7,13,UNIT_MCH,TEAM_P2))
mapUnits.sort(key=lambda u: u.row*mapCols+u.col)

for row in range(mapRows):
    for col in range(mapCols):
        id = mapTiles[row*mapCols+col]
        typeID = tileDefs[id]["type"]
        team = tileDefs[id]["team"]
        if team != TEAM_NEUTRAL:
            for player in players:
                player.notifyCapture(col, row, typeID, TEAM_NEUTRAL, team)
for unit in mapUnits:
    for player in players:
        player.notifyUnitSpawn(unit)

display.setFPS(15)

cCamX, cCamY = 0, 0
tCamX, tCamY = 0, 0

cursorCol, cursorRow = mapCols//2, mapRows//2
cursorUnit = None
updateCursorUnit = True
cCursorX, cCursorY = cursorCol*8, cursorRow*6
tCursorX, tCursorY = cCursorX, cCursorY

moveCol, moveRow = 0, 0
moveUnit = None

moveAnimX, moveAnimY = 0, 0
moveAnimIdx = 0

cPointX, cPointY = 0, 0
tPointX, tPointY = 0, 0
pointIdx = 0
pointOptions = []

state = SM_PLAYER_START
frame = 0
player = None

moveSteps = []
unloadOptions = []
attackOptions = []

def showPlayerStartScreen(day, team, funds, income, unitsDestroyed):
    display.fill(0)
    display.setFont("/lib/font5x7.bin", 5, 7, 1)
    dayStr = "DAY "+str(day)
    display.drawText(dayStr,36-(len(dayStr)*6)//2,0,0b01)
    display.setFont("/lib/font8x8.bin", 8, 8, 1)
    display.drawText("PLAYER "+str(team-1),0,16,0b01)
    display.setFont("/lib/font3x5.bin", 3, 5, 2)
    display.update()
    
    frame = 0
    while not buttonA.justPressed():
        frame += 1
        display.drawText("START",24,30,0b01 if ((frame%12)<6) else 0b00)
        display.update()
    
    display.fill(0)
    for _ in range(10):
        display.update()
    display.setFont("/lib/font3x5.bin", 3, 5, 2)
    display.drawText("Income: "+str(income),0,0,0b01)
    for _ in range(10):
        display.update()
    display.setFont("/lib/font5x7.bin", 5, 7, 1)
    if len(unitsDestroyed) > 0:
        display.drawText("Lost:",0,7,0b01)
        x, y = 30, 6
        for unit in unitsDestroyed:
            for _ in range(5):
                display.update()
            if x > 62:
                x, y = 0, y + 10
            mx = (unit.team == TEAM_P2)
            f = (unit.id-1)*3
            draw_blitMaskedMirroredFrame(bmpUnits, x, y, mx, 0, f)
            x += 10
            display.update()
        for _ in range(10):
            display.update()
    display.drawText("Funds:"+str(funds),0,33,0b11)
    for _ in range(5):
        display.update()
    display.setFPS(200)
    rate = max(9900/200,income/200)
    fundsAnim = funds
    while fundsAnim < funds+income:
        fundsAnim += rate
        display.drawFilledRectangle(0,33,72,7,0b00)
        display.drawText("Funds:"+str(int(fundsAnim)),0,33,0b11)
        display.update()
    display.setFPS(15)
    display.update()
    display.drawFilledRectangle(0,33,72,7,0b00)
    display.drawText("Funds:"+str(funds+income),0,33,0b01)
    display.update()
    for _ in range(5):
        display.update()
    while not buttonA.justPressed():
        display.update()

def showInfoScreen(unit, tileID):
    display.fill(0b00)
    display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    tileDef = tileDefs[tileID]
    tileType = tileDef["type"]
    tileTeam = tileDef["team"]
    
    tileTypeDef = tileTypeDefs[tileType]
    tileName = tileTypeDef["name"]
    tileDefence = tileTypeDef["def"]
    tileInfoFrame, tileInfoTall = tileTypeDef["info"]
    
    # XXX Janky hardcode
    if tileType == TILE_TYPE_HQ:
        tileInfoFrame = 0 if (tileTeam == TEAM_P1) else 1
    
    if tileTeam == TEAM_NEUTRAL:
        tileColor = 0b10
    elif tileTeam == turn:
        tileColor = 0b01
    else:
        tileColor = 0b11
        
    display.drawText(tileName,20,3,0b01)
    display.drawRectangle(0,2,19,36,tileColor)
    if tileInfoTall:
        display.drawFilledRectangle(2,4,15,32,tileColor)
        draw_blitMaskedFrame(bmpInfoTilesTall,2,4,tileInfoFrame)
        if tileTeam != TEAM_NEUTRAL:
            f = (tileTeam-TEAM_P1) * 2 + (0 if (tileTeam == turn) else 1)
            draw_blitMaskedFrame(bmpInfoPlayer,3,5,f)
    else:
        display.drawFilledRectangle(2,4,15,16,0b01)
        draw_blitFrame(bmpInfoTiles,2,20,tileInfoFrame)
        
    if tileDefence > 0:
        draw_blitMaskedFrame(bmpInfoStar,21,13,tileDefence-1)
        
    if unit is not None:
        unitDef = unitDefs[unit.id]
        unitName = unitDef["name"]
        unitHealth = unit.health
        unitColor = 0b01 if (unit.team == turn) else 0b11
        display.drawText(unitName,52-len(unitName)*4,32,0b01)
        display.drawRectangle(52,2,20,36,unitColor)
        display.drawFilledRectangle(54,4,16,32,unitColor)
        mx = (unit.team == TEAM_P2)
        draw_blitMaskedMirroredFrame(bmpInfoUnits,54,20,mx,0,unit.id-1)
        f = (unit.team-TEAM_P1) * 2 + (0 if (unit.team == turn) else 1)
        draw_blitMaskedFrame(bmpInfoPlayer,55,5,f)
        f = max(1,unitHealth//10)
        draw_blitMaskedFrame(bmpBattleNumbers,38,14,f)
        
    # TODO Show capture points
    # TODO Show APC carry unit
    
    display.update()
    while not buttonB.justPressed():
        display.update()
        
def showPlayerMenu(day, team, funds):
    display.fill(0b00)
    display.setFont("/lib/font3x5.bin", 3, 5, 1)
    display.drawText("Player "+str(team-1)+" - Day "+str(day),0,0,0b01)
    display.drawText("Funds:"+str(funds),0,35,0b01)
    options = ["View Map","End Turn"]
    selection = 0
    display.setFont("/lib/font5x7.bin", 5, 7, 1)
    while True:
        if buttonD.justPressed():
            selection = (selection + 1) % len(options)
        if buttonU.justPressed():
            selection = (selection + len(options) - 1) % len(options)
        if buttonB.justPressed():
            return False
        if buttonA.justPressed():
            return options[selection] == "End Turn"
        y = 8
        for i in range(len(options)):
            if i == selection:
                bg, fg, dx = 0b01, 0b00, 2
            else:
                bg, fg, dx = 0b00, 0b01, 0
            display.drawFilledRectangle(0,y,72,8,bg)
            display.drawText(options[i],dx,y,fg)
            y += 8
        display.update()
        
def showBuyMenu(day, team, funds):
    display.fill(0b00)
    display.setFont("/lib/font3x5.bin", 3, 5, 1)
    display.drawText("Player "+str(team-1)+" - Day "+str(day),0,0,0b01)
    display.drawText("Funds:"+str(funds),0,35,0b01)
    options = [
        UNIT_INF,
        UNIT_MCH,
        UNIT_RCN,
        UNIT_APC,
        UNIT_TNK,
    ]
    selection = 0
    frame = 0
    while True:
        frame += 1
        if buttonD.justPressed():
            selection = (selection + 1) % len(options)
        if buttonU.justPressed():
            selection = (selection + len(options) - 1) % len(options)
        if buttonB.justPressed():
            return None
        if buttonA.justPressed() and unitDefs[options[selection]]["cost"] <= funds:
            return options[selection]
        start = max(1,min(len(options)-2,selection))-1
        y = 8
        display.setFont("/lib/font3x5.bin", 3, 5, 1)
        for i in range(start,start+3):
            unitDef = unitDefs[options[i]]
            cost = unitDef["cost"]
            if cost <= funds:
                if i == selection:
                    bg, fg = 0b01, 0b00
                else:
                    bg, fg = 0b00, 0b01
            else:
                if i == selection:
                    bg, fg = 0b10, 0b00
                else:
                    bg, fg = 0b00, 0b10
            display.drawFilledRectangle(0,y,72,8,bg)
            mx = (team == TEAM_P2)
            f = (unitDef["id"]-1)*3
            if cost <= funds:
                f += 0 if ((frame % 8) < 4) else 1
            else:
                f += 2
            draw_blitMaskedMirroredFrame(bmpUnits,0,y-1,10,10,-1,mx,0,bmpUnits[2],f)
            display.drawText(unitDef["name"],36,y+1,fg)
            y += 8
        display.setFont("/lib/font5x7.bin", 5, 7, 1)
        y = 8
        for i in range(start,start+3):
            unitDef = unitDefs[options[i]]
            cost = unitDef["cost"]
            if cost <= funds:
                if i == selection:
                    fg = 0b00
                else:
                    fg = 0b01
            else:
                if i == selection:
                    fg = 0b00
                else:
                    fg = 0b10
            display.drawText(str(cost),11,y,fg)
            y += 8
        display.update()
        

def showUnitMenu(day, team, funds, options):
    display.fill(0b00)
    display.setFont("/lib/font3x5.bin", 3, 5, 1)
    display.drawText("Player "+str(team-1)+" - Day "+str(day),0,0,0b01)
    display.drawText("Funds:"+str(funds),0,35,0b01)
    selection = 0
    display.setFont("/lib/font5x7.bin", 5, 7, 1)
    while True:
        if buttonD.justPressed():
            selection = (selection + 1) % len(options)
        if buttonU.justPressed():
            selection = (selection + len(options) - 1) % len(options)
        if buttonB.justPressed():
            return None
        if buttonA.justPressed():
            return options[selection]
        start = max(1,min(len(options)-2,selection))-1
        y = 8
        for i in range(start,start+min(3,len(options))):
            if i == selection:
                bg, fg, dx = 0b01, 0b00, 2
            else:
                bg, fg, dx = 0b00, 0b01, 0
            display.drawFilledRectangle(0,y,72,8,bg)
            display.drawText(options[i],dx,y,fg)
            y += 8
        display.update()

def showCaptureAnimation(tileID, captureHealth, captureAmount):
    if tileID == TILE_HQ_P1:
        tfr, yCap = 0, 15
    elif tileID == TILE_HQ_P2:
        tfr, yCap = 5, 15
    elif tileDefs[tileID]["type"] == TILE_TYPE_CITY:
        tfr, yCap = 10, 21
    else:
        tfr, yCap = 15, 25
    yCap -= 25
        
    captureStage = 4-((captureHealth+4)//5)
    tf = tfr + captureStage
        
    x1, y1 = 10, 9
        
    display.setFPS(30)
    display.setFont("/lib/font8x8.bin", 8, 8, 1)
        
    display.fill(0b00)
    display.drawRectangle(26,2,19,36,0b11)
    display.drawFilledRectangle(28,4,15,32,0b11)
    draw_blitMaskedFrame(bmpCaptureTiles,28,4,tf)
    draw_blitMaskedFrame(bmpCapture,x1,y1,0)
    display.drawText(str(captureHealth), 46, 16, 0b01)
    for _ in range(5):
        display.update()
    
    x2, y2 = 28, yCap + (((y1-yCap)*captureStage)//4)
    
    for frame in range(10):
        x = x1 + ((x2-x1)*frame)//10
        y = y1 + ((y2-y1)*frame)//10
        y -= 5-abs(frame-5)
        display.fill(0b00)
        display.drawRectangle(26,2,19,36,0b11)
        display.drawFilledRectangle(28,4,15,32,0b11)
        draw_blitMaskedFrame(bmpCaptureTiles,28,4,tf)
        draw_blitMaskedFrame(bmpCapture,x,y,1)
        display.drawText(str(captureHealth), 46, 16, 0b01)
        display.update()
        
    for frame in range(20):
        cf = 0 if ((frame % 15) < 6) else 1
        dy = 1 - cf
        display.fill(0b00)
        display.drawRectangle(26,2,19,36,0b11)
        display.drawFilledRectangle(28,4,15,32,0b11)
        draw_blitMaskedFrame(bmpCaptureTiles,28,4+dy,tf)
        draw_blitMaskedFrame(bmpCapture,x2,y2+dy,cf)
        display.drawText(str(captureHealth), 46, 16, 0b01)
        display.update()
        
    delay = 1 + (10-captureAmount) // 3
    for _ in range(captureAmount):
        captureHealth -= 1
        captureStage = 4-((captureHealth+4)//5)
        tf = tfr + captureStage
        y = yCap + (((y1-yCap)*captureStage)//4)
        display.fill(0b00)
        display.drawRectangle(26,2,19,36,0b11)
        display.drawFilledRectangle(28,4,15,32,0b11)
        draw_blitMaskedFrame(bmpCaptureTiles,28,4,tf)
        draw_blitMaskedFrame(bmpCapture,x2,y,cf)
        display.drawText(str(captureHealth), 46, 16, 0b01)
        for _ in range(delay+1):
            display.update()
            
    y3 = y
    for frame in range(10):
        x = x2 + ((x1-x2)*frame)//10
        y = y3 + ((y1-y3)*frame)//10
        y -= 5-abs(frame-5)
        display.fill(0b00)
        display.drawRectangle(26,2,19,36,0b11)
        display.drawFilledRectangle(28,4,15,32,0b11)
        draw_blitMaskedFrame(bmpCaptureTiles,28,4,tf)
        draw_blitMaskedFrame(bmpCapture,x,y,1)
        display.drawText(str(captureHealth), 46, 16, 0b01)
        display.update()
        
    if captureHealth == 0:
        for _ in range(20):
            captureHealth += 1
            captureStage = 4-((captureHealth+4)//5)
            tf = tfr + captureStage
            y = yCap + (((y1-yCap)*captureStage)//4)
            display.fill(0b00)
            display.drawRectangle(26,2,19,36,0b01)
            display.drawFilledRectangle(28,4,15,32,0b01)
            draw_blitMaskedFrame(bmpCaptureTiles,28,4,tf)
            draw_blitMaskedFrame(bmpCapture,x1,y1,2)
            display.drawText(str(captureHealth), 46, 16, 0b01)
            display.update()
        for _ in range(10):
            display.update()
    else:
        display.fill(0b00)
        display.drawRectangle(26,2,19,36,0b11)
        display.drawFilledRectangle(28,4,15,32,0b11)
        draw_blitMaskedFrame(bmpCaptureTiles,28,4,tf)
        draw_blitMaskedFrame(bmpCapture,x1,y1,0)
        display.drawText(str(captureHealth), 46, 16, 0b01)
        for _ in range(30):
            display.update()
    
    display.setFPS(15)
    
def checkUnloadOptions(col, row):
    ret = []
    for dCol, dRow in ((1,0),(0,1),(-1,0),(0,-1)):
        checkCol = col + dCol
        checkRow = row + dRow
        if 0 <= checkCol < mapCols and 0 <= checkRow < mapRows:
            tileID = mapTiles[checkRow*mapCols+checkCol]
            typeID = tileDefs[tileID]
            if typeID in [TILE_TYPE_WALL,TILE_TYPE_SEA]:
                continue
            occupied = False
            for checkUnit in mapUnits:
                if checkCol == checkUnit.col and checkRow == checkUnit.row:
                    occupied = True
                    break
            if occupied:
                continue
            ret.append((checkCol, checkRow))
    return ret
    
def checkAttackOptions(col, row, team, atk, moved):
    ret = []
    for unit in mapUnits:
        if unit.team == team:
            continue
        dist = abs(col-unit.col)+abs(row-unit.row)
        if atk == ATK_ADJACENT and dist == 1:
            ret.append(unit)
        elif atk == ATK_ARTILLERY and not moved and 2 <= dist <= 3:
            ret.append(unit)
    return ret

while True:
    frame += 1
    
    if state == SM_PLAYER_START:
        player = players[turn-2]
        income = fundsPerProperty*(1+len(player.cities)+len(player.factories))
        showPlayerStartScreen(day,turn,player.funds,income,player.unitsDestroyed)
        
        player.funds += income
        player.unitsDestroyed = []
        for unit in player.units:
            unit.ready = True
        
        cursorCol = player.cursorCol
        cursorRow = player.cursorRow
        updateCursorUnit = True
        tCursorX = cursorCol*8
        tCursorY = cursorRow*6
        
        # XXX This is a janky hack
        if turn == TEAM_P1:
            visualRemap = [
                (TILE_HQ_P1, TILE_HQ_P1),
                (TILE_HQ_P2, TILE_HQ_P2),
                (TILE_CITY_P1, TILE_CITY_P1),
                (TILE_CITY_P2, TILE_CITY_P2),
                (TILE_FACT_P1, TILE_FACT_P1),
                (TILE_FACT_P2, TILE_FACT_P2),
            ]
        elif turn == TEAM_P2:
            visualRemap = [
                (TILE_HQ_P1, TILE_HQ_P2),
                (TILE_HQ_P2, TILE_HQ_P1),
                (TILE_CITY_P1, TILE_CITY_P2),
                (TILE_CITY_P2, TILE_CITY_P1),
                (TILE_FACT_P1, TILE_FACT_P2),
                (TILE_FACT_P2, TILE_FACT_P1),
            ]
        for tileID, visualID in visualRemap:
            for f in range(len(tileTallFrameOrder)):
                if tileTallFrameOrder[f] == visualID:
                    tileDrawFrames[tileID] = (True,f)
                    break
        
        state, frame = SM_TILE_SELECT, 0
        
    elif state == SM_PLAYER_MENU:
        endTurn = showPlayerMenu(day, player.team, player.funds)
        if endTurn:
            player = players[turn-2]
            player.cursorRow = cursorRow
            player.cursorCol = cursorCol
            turn = TEAM_P2 if (turn == TEAM_P1) else TEAM_P1
            state, frame = SM_PLAYER_START, 0
        else:
            state, frame = SM_TILE_SELECT, 0
            
    elif state == SM_TILE_UNIT_INFO:
        tileID = mapTiles[cursorRow*mapCols+cursorCol]
        showInfoScreen(cursorUnit, tileID)
        state, frame = SM_TILE_SELECT, 0
        
    elif state == SM_BUY_MENU:
        unitID = showBuyMenu(day,turn,player.funds)
        if unitID is not None:
            player.funds -= unitDefs[unitID]["cost"]
            unit = Unit(cursorCol,cursorRow,unitID,turn)
            mapUnits.append(unit)
            mapUnits.sort(key=lambda u: u.row*mapCols+u.col)
            for player in players:
                player.notifyUnitSpawn(unit)
            updateCursorUnit = True
        state, frame = SM_TILE_SELECT, 0
    
    elif state == SM_TILE_SELECT:
        if buttonU.justPressed() and cursorRow > 0:
            cursorRow -= 1
            updateCursorUnit = True
        if buttonD.justPressed() and cursorRow < mapRows-1:
            cursorRow += 1
            tCursorY = cursorRow*6
            updateCursorUnit = True
        if buttonL.justPressed() and cursorCol > 0:
            cursorCol -= 1
            tCursorX = cursorCol*8
            updateCursorUnit = True
        if buttonR.justPressed() and cursorCol < mapCols-1:
            cursorCol += 1
            updateCursorUnit = True
            
        tCursorX = cursorCol*8
        tCursorY = cursorRow*6
        
        if updateCursorUnit:
            updateCursorUnit = False
            cursorUnit = None
            for unit in mapUnits:
                if unit.col != cursorCol or unit.row != cursorRow:
                    continue
                cursorUnit = unit
                break
            
        tCamX = max(3,min(mapCols-4,cursorCol))*8+4
        tCamY = max(2,min(mapRows-3,cursorRow))*6+3
        
        if buttonB.justPressed():
            state, frame = SM_TILE_UNIT_INFO, 0
        elif buttonA.justPressed():
            tileID = mapTiles[cursorRow*mapCols+cursorCol]
            tileDef = tileDefs[tileID]
            if tileDef["type"] == TILE_TYPE_FACT and tileDef["team"] == turn and cursorUnit is None:
                state, frame = SM_BUY_MENU, 0
            elif cursorUnit is not None and cursorUnit.team == turn and cursorUnit.ready:
                moveUnit = cursorUnit
                moveCol = moveUnit.col
                moveRow = moveUnit.row
                movePoints = unitDefs[moveUnit.id]["mp"]
                moveType = unitDefs[moveUnit.id]["move"]
                moveSteps = [(moveCol,moveRow,None,movePoints)]
                state, frame = SM_MOVE_SELECT, 0
            else:
                state, frame = SM_PLAYER_MENU, 0
    
    elif state == SM_MOVE_SELECT:
        nextMove = None
        if buttonU.justPressed() and moveRow > 0:
            nextMove = (moveCol, moveRow-1, MOVE_UP)
        if buttonD.justPressed() and moveRow < mapRows-1:
            nextMove = (moveCol, moveRow+1, MOVE_DOWN)
        if buttonL.justPressed() and moveCol > 0:
            nextMove = (moveCol-1, moveRow, MOVE_LEFT)
        if buttonR.justPressed() and moveCol < mapCols-1:
            nextMove = (moveCol+1, moveRow, MOVE_RIGHT)
        
        if buttonB.justPressed():
            state, frame = SM_TILE_SELECT, 0
        elif buttonA.justPressed():
            validMove = True
            if len(moveSteps) > 1:
                for unit in mapUnits:
                    if moveCol==unit.col and moveRow==unit.row:
                        if moveUnit.id in [UNIT_INF,UNIT_MCH] and unit.id == UNIT_APC and unit.carry is None:
                            validMove = True
                            break
                        if unit.id != moveUnit.id or unit.health == 100:
                            validMove = False
                            break
            if validMove:
                mapUnits.remove(moveUnit)
                moveAnimX = moveUnit.col*8
                moveAnimY = moveUnit.row*6
                moveAnimIdx = 0
                state, frame = SM_MOVE_ANIM, 0
        
        if nextMove is not None:
            moveRewind = False
            if len(moveSteps) > 1:
                for i in range(0,len(moveSteps)):
                    checkMove = moveSteps[i]
                    if checkMove[0] == nextMove[0] and checkMove[1] == nextMove[1]:
                        for j in range(len(moveSteps)-1,i,-1):
                            del moveSteps[j]
                        moveCol, moveRow, _, movePoints = checkMove
                        moveRewind = True
                        break
            if not moveRewind:
                tileID = mapTiles[nextMove[1]*mapCols+nextMove[0]]
                moveCost = tileTypeDefs[tileDefs[tileID]["type"]]["move"][moveType]
                if moveCost > 0 and movePoints >= moveCost:
                    blocked = False
                    for unit in mapUnits:
                        if nextMove[0]==unit.col and nextMove[1]==unit.row:
                            if unit.team != turn:
                                blocked = True
                                break
                    if not blocked:
                        movePoints -= moveCost
                        moveCol, moveRow, moveDir = nextMove
                        moveSteps.append((moveCol,moveRow,moveDir,movePoints))
                    
            tCamX = max(3,min(mapCols-4,moveCol))*8+4
            tCamY = max(2,min(mapRows-3,moveRow))*6+3
        
    elif state == SM_UNIT_MENU:
        options = []
        
        occupied = False
        occUnit = None
        for unit in mapUnits:
            if moveCol == unit.col and moveRow == unit.row:
                occupied = True
                occUnit = unit
                if unit.id == moveUnit.id and unit.health < 100:
                    options.append("Join")
                break
        
        tileID = mapTiles[moveRow*mapCols+moveCol]
        typeID = tileDefs[tileID]["type"]
        tileTeam = tileDefs[tileID]["team"]
        
        if moveUnit.id in [UNIT_INF,UNIT_MCH]:
            if occupied and occUnit.id == UNIT_APC and occUnit.carry is None:
                options.append("Load")
            if not occupied and typeID in [TILE_TYPE_HQ,TILE_TYPE_CITY,TILE_TYPE_FACT] and turn != tileTeam:
                options.append("Capture")
        
        if moveUnit.id == UNIT_APC and not occupied and moveUnit.carry is not None:
            unloadOptions = checkUnloadOptions(moveCol, moveRow)
            if len(unloadOptions) > 0:
                options.append("Unload")
        
        unitAtk = unitDefs[moveUnit.id]["atk"]
        if not occupied and unitAtk != ATK_NONE:
            unitMoved = (len(moveSteps) > 1)
            attackOptions = checkAttackOptions(moveCol, moveRow, turn, unitAtk, unitMoved)
            if len(attackOptions) > 0:
                options.append("Attack")
        
        if not occupied:
            options.append("Wait")
            
        act = showUnitMenu(day,turn,player.funds,options)
        
        if act is None:
            mapUnits.append(moveUnit)
            mapUnits.sort(key=lambda u: u.row*mapCols+u.col)
            state, frame = SM_MOVE_SELECT, 0
            
        elif act == "Wait":
            moveUnit.col = moveCol
            moveUnit.row = moveRow
            moveUnit.ready = False
            if len(moveSteps) > 0:
                moveUnit.capture = 0
            mapUnits.append(moveUnit)
            mapUnits.sort(key=lambda u: u.row*mapCols+u.col)
            cursorCol = moveCol
            cursorRow = moveRow
            updateCursorUnit = True
            state, frame = SM_TILE_SELECT, 0
            
        elif act == "Join":
            occUnit.health = min(100, occUnit.health + moveUnit.health)
            cursorCol = moveCol
            cursorRow = moveRow
            updateCursorUnit = True
            state, frame = SM_TILE_SELECT, 0
        
        elif act == "Capture":
            # TODO show capture in unit info screen
            moveUnit.col = moveCol
            moveUnit.row = moveRow
            moveUnit.ready = False
            mapUnits.append(moveUnit)
            mapUnits.sort(key=lambda u: u.row*mapCols+u.col)
            cursorCol = moveCol
            cursorRow = moveRow
            updateCursorUnit = True
            state, frame = SM_CAPTURE_ANIM, 0
        
        elif act == "Load":
            # TODO show carry in unit info screen
            occUnit.carry = moveUnit
            cursorCol = moveCol
            cursorRow = moveRow
            updateCursorUnit = True
            state, frame = SM_TILE_SELECT, 0
            
        elif act == "Unload":
            pointIdx = 0
            pointOptions = []
            for col, row in unloadOptions:
                pointOptions.append((col*8+4,row*6+3,(col, row)))
            cPointX, cPointY, _ = pointOptions[0]
            tPointX, tPointY = cPointX, cPointY
            state, frame = SM_UNLOAD_SELECT, 0
            
        elif act == "Attack":
            pointIdx = 0
            pointOptions = []
            for unit in attackOptions:
                col, row = unit.col, unit.row
                pointOptions.append((col*8+4,row*6-1,unit))
            cPointX, cPointY, _ = pointOptions[0]
            tPointX, tPointY = cPointX, cPointY
            state, frame = SM_ATTACK_SELECT, 0
    
    elif state == SM_CAPTURE_ANIM:
        tileID = mapTiles[moveRow*mapCols+moveCol]
        captureHealth = 20-moveUnit.capture
        captureAmount = max(1,min(captureHealth,moveUnit.health//10))
        showCaptureAnimation(tileID, captureHealth, captureAmount)
        moveUnit.capture += captureAmount
        if moveUnit.capture == 20:
            moveUnit.capture = 0
            typeID = tileDefs[tileID]["type"]
            oldTeam = tileDefs[tileID]["team"]
            if typeID == TILE_TYPE_HQ:
                tileID = TILE_HQ_P1 if turn == TEAM_P1 else TILE_HQ_P2
            elif typeID == TILE_TYPE_CITY:
                tileID = TILE_CITY_P1 if turn == TEAM_P1 else TILE_CITY_P2
            elif typeID == TILE_TYPE_FACT:
                tileID = TILE_FACT_P1 if turn == TEAM_P1 else TILE_FACT_P2
            mapTiles[moveRow*mapCols+moveCol] = tileID
            for player in players:
                player.notifyCapture(moveCol, moveRow, typeID, oldTeam, turn)
        state, frame = SM_TILE_SELECT, 0
        
    elif state == SM_UNLOAD_SELECT:
        if buttonL.justPressed() or buttonU.justPressed():
            pointIdx = (pointIdx + len(pointOptions) - 1) % len(pointOptions)
        if buttonR.justPressed() or buttonD.justPressed():
            pointIdx = (pointIdx + 1) % len(pointOptions)
        
        if buttonB.justPressed():
            state, frame = SM_UNIT_MENU, 0
        elif buttonA.justPressed():
            unit = moveUnit.carry
            moveUnit.carry = None
            unit.col, unit.row = pointOptions[pointIdx][2]
            unit.ready = False
            moveUnit.col = moveCol
            moveUnit.row = moveRow
            moveUnit.ready = False
            mapUnits.append(unit)
            mapUnits.append(moveUnit)
            mapUnits.sort(key=lambda u: u.row*mapCols+u.col)
            cursorCol = moveCol
            cursorRow = moveRow
            updateCursorUnit = True
            state, frame = SM_TILE_SELECT, 0
        
        tPointX, tPointY, _ = pointOptions[pointIdx]
        
    elif state == SM_ATTACK_SELECT:
        if buttonL.justPressed() or buttonU.justPressed():
            pointIdx = (pointIdx + len(pointOptions) - 1) % len(pointOptions)
        if buttonR.justPressed() or buttonD.justPressed():
            pointIdx = (pointIdx + 1) % len(pointOptions)
        
        if buttonB.justPressed():
            state, frame = SM_UNIT_MENU, 0
        elif buttonA.justPressed():
            attackedUnit = pointOptions[pointIdx][2]
            # TODO
            moveUnit.col = moveCol
            moveUnit.row = moveRow
            moveUnit.ready = False
            mapUnits.append(unit)
            mapUnits.append(moveUnit)
            mapUnits.sort(key=lambda u: u.row*mapCols+u.col)
            cursorCol = moveCol
            cursorRow = moveRow
            updateCursorUnit = True
            state, frame = SM_TILE_SELECT, 0
        
        tPointX, tPointY, _ = pointOptions[pointIdx]
        
    
    display.fill(0b00)
    
    if abs(tCamX-cCamX) > 1:
        cCamX += (tCamX - cCamX) >> 1
    else:
        cCamX = tCamX
    if abs(tCamY-cCamY) > 1:
        cCamY += (tCamY - cCamY) >> 1
    else:
        cCamY = tCamY
    
    if abs(tCursorX-cCursorX) > 1:
        cCursorX += (tCursorX - cCursorX) >> 1
    else:
        cCursorX = tCursorX
    if abs(tCursorY-cCursorY) > 1:
        cCursorY += (tCursorY - cCursorY) >> 1
    else:
        cCursorY = tCursorY
        
    if abs(tPointX-cPointX) > 1:
        cPointX += (tPointX - cPointX) >> 1
    else:
        cPointX = tPointX
    if abs(tPointY-cPointY) > 1:
        cPointY += (tPointY - cPointY) >> 1
    else:
        cPointY = tPointY
    
    sx, sy = cCamX-36, cCamY-20
    
    unitIdx = 0
    for row in range(mapRows):
        y = row*6 - sy
        if y <= -6 or y >= 40:
            continue
        for col in range(mapCols):
            x = col*8 - sx
            if x <= -8 or x >= 72:
                continue
            i = row*mapCols+col
            id = mapTiles[i]
            tall, f = tileDrawFrames[id]
            if tall:
                draw_blitMaskedFrame(bmpTilesTall,x,y-6,f)
            else:
                draw_blitFrame(bmpTiles, x, y, f)
        while unitIdx < len(mapUnits):
            unit = mapUnits[unitIdx]
            if unit.row > row:
                break
            unitIdx += 1
            ux = unit.col*8 - sx - 1
            uy = unit.row*6 - sy - 4
            if uy <= -10 or uy >= 40:
                continue
            if ux <= -10 or ux >= 72:
                continue
            mx = (unit.team == TEAM_P2)
            f = (unit.id-1)*3
            if turn == unit.team:
                if unit.ready:
                    f += 0 if ((frame % 8) < 4) else 1
                else:
                    f += 2
            draw_blitMaskedMirroredFrame(bmpUnits,ux,uy,mx,0,f)
        
    if state == SM_MOVE_SELECT and len(moveSteps) > 1:
        for i in range(len(moveSteps)):
            col, row, m1, _ = moveSteps[i]
            m2 = moveSteps[i+1][2] if (i < len(moveSteps)-1) else None
            x = col*8 - sx
            y = row*6 - sy
            f, mx, my = moveDraws[(m1,m2)]
            draw_blitMaskedMirroredFrame(bmpMove,x,y-1,mx,my,f)
        
    # TODO show city being captured when cursored over
    # TODO show APC is carrying unit when cursored over
    if state == SM_TILE_SELECT and ((frame % 10) < 5):
        x = cCursorX - sx
        y = cCursorY - sy
        draw_blitMaskedFrame(bmpTileCursor,x-2,y-2,0)
        
    if state == SM_UNLOAD_SELECT or state == SM_ATTACK_SELECT:
        x = cPointX - sx
        y = cPointY - sy
        if ((frame % 4) < 2):
            y -= 1
        draw_blitMaskedFrame(bmpPoint,x-3,y-7,0)
        mx = (moveUnit.team == TEAM_P2)
        f = (moveUnit.id-1)*3
        draw_blitMaskedMirroredFrame(bmpUnits,moveAnimX-sx-1,moveAnimY-sy-3,mx,0,f)
        
    if state == SM_MOVE_ANIM:
        if moveAnimIdx == len(moveSteps):
            state, frame = SM_UNIT_MENU, 0
        else:
            col, row, _, _ = moveSteps[moveAnimIdx]
            x, y = col*8, row*6
            if x > moveAnimX:
                moveAnimX += 2
            elif x < moveAnimX:
                moveAnimX -= 2
            elif y > moveAnimY:
                moveAnimY += 2
            elif y < moveAnimY:
                moveAnimY -= 2
            else:
                moveAnimIdx += 1
            mx = (moveUnit.team == TEAM_P2)
            f = (moveUnit.id-1)*3 + (0 if (((moveAnimX+moveAnimY)%4)<2) else 1)
            draw_blitMaskedMirroredFrame(bmpUnits,moveAnimX-sx-1,moveAnimY-sy-3,mx,0,f)
                
    if state == SM_TILE_SELECT and cursorUnit is not None:
        if cursorUnit.team == TEAM_P1:
            x = (cCursorX-9) - sx
        else:
            x = (cCursorX+8) - sx
        y = (cCursorY-1) - sy
        f = max(1,unit.health//10)-1
        draw_blitFrame(bmpHealth, x, y, f)
    
    display.update()
    