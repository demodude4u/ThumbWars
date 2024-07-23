from tw_enums import *
from tw_defs import *


mapCols, mapRows, mapTiles = 15, 15, [54,52,52,58,2,3,2,2,2,2,5,34,3,1,2,
                                    59,1,3,1,1,3,3,2,34,2,10,8,44,47,1,
                                    3,18,15,15,15,15,19,2,1,3,2,5,1,16,44,
                                    1,16,34,1,3,1,25,15,15,15,15,26,15,23,34,
                                    1,16,1,1,1,34,16,2,34,1,2,5,1,16,3,
                                    4,27,4,8,1,18,20,3,1,1,2,5,1,16,2,
                                    3,16,34,5,1,16,34,1,3,1,2,5,34,16,2,
                                    1,16,35,5,3,21,15,15,15,19,3,5,35,16,1,
                                    2,16,34,5,2,1,3,1,34,16,1,5,34,16,3,
                                    2,16,1,5,2,1,1,3,18,20,1,10,4,27,4,
                                    3,16,1,5,2,1,34,2,16,34,1,1,1,16,1,
                                    34,25,15,26,15,15,15,15,23,1,3,1,34,16,1,
                                    39,16,1,5,2,3,1,2,21,15,15,15,15,20,3,
                                    1,42,39,10,8,2,34,2,3,3,1,1,3,1,57,
                                    2,1,3,34,5,2,2,2,2,3,2,60,52,52,56]
                                    
class Unit:
    def __init__(self, col, row, id, team, health=100, ready=False, capture=0, carry=None):
        self.col = col
        self.row = row
        self.id = id
        self.team = team
        self.health = health
        self.ready = ready
        self.capture = capture
        self.carry = carry

mapUnits = []

fundsPerProperty = 1000

class Player:
    def __init__(self, team):
        self.team = team
        self.funds = 0
        
        self.cursorCol = 0
        self.cursorRow = 0
        
        self.hq = None
        self.cities = []
        self.factories = []
        self.units = []
        self.unitsDestroyed = []
        
    def notifyCapture(self, col, row, typeID, prevTeam, team):
        lost = prevTeam == self.team
        gain = team == self.team
        if typeID == TILE_TYPE_HQ:
            if lost:
                self.hq = None
            if gain:
                self.hq = (col, row)
                self.cursorCol = col
                self.cursorRow = row
        elif typeID == TILE_TYPE_CITY:
            if lost:
                for i in range(len(self.cities)):
                    checkCol, checkRow = self.cities[i]
                    if checkCol == col and checkRow == row:
                        del self.cities[i]
                        break
            if gain:
                self.cities.append((col, row))
        elif typeID == TILE_TYPE_FACT:
            if lost:
                for i in range(len(self.factories)):
                    checkCol, checkRow = self.factories[i]
                    if checkCol == col and checkRow == row:
                        del self.factories[i]
                        break
            if gain:
                self.factories.append((col, row))
                
    def notifyUnitSpawn(self, unit):
        if unit.team == self.team:
            self.units.append(unit)
    
    def notifyUnitDestroy(self, unit):
        if unit.team == self.team:
            self.units.remove(unit)
            self.unitsDestroyed.append(unit)

day = 1
turn = TEAM_P1
players = [
    Player(TEAM_P1),
    Player(TEAM_P2),
]