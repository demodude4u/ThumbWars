from tw_enums import *

unitDefs = {
    UNIT_INF: {
        "name": "Infantry",
        "id": 1,
        "move": MOVE_INF,
        "mp": 3,
        "atk": ATK_ADJACENT,
        "cost": 1000,
        "dmg": {
            "INF": (55,55),
            "MCH": (45,65),
            "RCN": (12,70),
            "TNK": (5,75),
            "ART": (15,90),
        }
    },
    UNIT_MCH: {
        "name": "Mech",
        "id": 2,
        "move": MOVE_MCH,
        "mp": 2,
        "atk": ATK_ADJACENT,
        "cost": 3000,
        "dmg": {
            "INF": (65,45),
            "MCH": (55,55),
            "RCN": (85,65),
            "TNK": (55,70),
            "ART": (70,85),
        }
    },
    UNIT_RCN: {
        "name": "Recon",
        "id": 3,
        "move": MOVE_TIRES,
        "mp": 8,
        "atk": ATK_ADJACENT,
        "cost": 4000,
        "dmg": {
            "INF": (70,12),
            "MCH": (65,85),
            "RCN": (35,35),
            "TNK": (6,85),
            "ART": (45,80),
        }
    },
    UNIT_TNK: {
        "name": "Tank",
        "id": 4,
        "move": MOVE_TREADS,
        "mp": 6,
        "atk": ATK_ADJACENT,
        "cost": 7000,
        "dmg": {
            "INF": (75,5),
            "MCH": (70,55),
            "RCN": (85,6),
            "TNK": (55,55),
            "ART": (70,70),
        }
    },
    UNIT_APC: {
        "name": "APC",
        "id": 5,
        "move": MOVE_TREADS,
        "mp": 6,
        "atk": ATK_NONE,
        "cost": 5000,
        "dmg": {
            "INF": (0,12),
            "MCH": (0,75),
            "RCN": (0,45),
            "TNK": (0,75),
            "ART": (0,70),
        }
    },
    UNIT_ART: {
        "name": "Cannon",
        "id": 6,
        "move": MOVE_TREADS,
        "mp": 5,
        "atk": ATK_ARTILLERY,
        "cost": 6000,
        "dmg": {
            "INF": (90,15),
            "MCH": (85,70),
            "RCN": (80,45),
            "TNK": (70,70),
            "ART": (75,75),
        }
    },
}

tileTypeDefs = {
    TILE_TYPE_PLN: {
        "name": "Plains",
        "ids": [TILE_PLN],
        "def": 1,
        "move": {
            MOVE_INF: 1,
            MOVE_MCH: 1,
            MOVE_TREADS: 1,
            MOVE_TIRES: 2
        }
    },
    TILE_TYPE_MTN: {
        "name": "Hills",
        "ids": [TILE_MTN],
        "def": 4,
        "move": {
            MOVE_INF: 2,
            MOVE_MCH: 1,
            MOVE_TREADS: 0,
            MOVE_TIRES: 0
        }
    },
    TILE_TYPE_WDS: {
        "name": "Woods",
        "ids": [TILE_WDS],
        "def": 2,
        "move": {
            MOVE_INF: 1,
            MOVE_MCH: 1,
            MOVE_TREADS: 2,
            MOVE_TIRES: 3
        }
    },
    TILE_TYPE_RVR: {
        "name": "River",
        "ids": [TILE_RVR_H,TILE_RVR_V,TILE_RVR_C,
                TILE_RVR_ES,TILE_RVR_SW,TILE_RVR_WN,TILE_RVR_NE,
                TILE_RVR_ESW,TILE_RVR_SWN,TILE_RVR_WNE,TILE_RVR_NES],
        "def": 0,
        "move": {
            MOVE_INF: 2,
            MOVE_MCH: 1,
            MOVE_TREADS: 0,
            MOVE_TIRES: 0
        }
    },
    TILE_TYPE_ROAD: {
        "name": "Road",
        "ids": [TILE_ROAD_H,TILE_ROAD_V,TILE_ROAD_C,
                TILE_ROAD_ES,TILE_ROAD_SW,TILE_ROAD_WN,TILE_ROAD_NE,
                TILE_ROAD_ESW,TILE_ROAD_SWN,TILE_ROAD_WNE,TILE_ROAD_NES,
                TILE_ROAD_HB,TILE_ROAD_VB],
        "def": 0,
        "move": {
            MOVE_INF: 1,
            MOVE_MCH: 1,
            MOVE_TREADS: 1,
            MOVE_TIRES: 1
        }
    },
    TILE_TYPE_SEA: {
        "name": "Sea",
        "ids": [TILE_SEA],
        "def": 0,
        "move": {
            MOVE_INF: 0,
            MOVE_MCH: 0,
            MOVE_TREADS: 0,
            MOVE_TIRES: 0
        }
    },
    TILE_TYPE_BCH: {
        "name": "Beach",
        "ids": [TILE_BCH_H,TILE_BCH_HN,TILE_BCH_V,TILE_BCH_VN],
        "def": 0,
        "move": {
            MOVE_INF: 1,
            MOVE_MCH: 1,
            MOVE_TREADS: 1,
            MOVE_TIRES: 1
        }
    },
    TILE_TYPE_HQ: {
        "name": "HQ",
        "ids": [TILE_HQ_P1,TILE_HQ_P2],
        "def": 4,
        "move": {
            MOVE_INF: 1,
            MOVE_MCH: 1,
            MOVE_TREADS: 1,
            MOVE_TIRES: 1
        }
    },
    TILE_TYPE_CITY: {
        "name": "City",
        "ids": [TILE_CITY_N,TILE_CITY_P1,TILE_CITY_P2],
        "def": 3,
        "move": {
            MOVE_INF: 1,
            MOVE_MCH: 1,
            MOVE_TREADS: 1,
            MOVE_TIRES: 1
        }
    },
    TILE_TYPE_FACT: {
        "name": "Factory",
        "ids": [TILE_FACT_N,TILE_FACT_P1,TILE_FACT_P2],
        "def": 3,
        "move": {
            MOVE_INF: 1,
            MOVE_MCH: 1,
            MOVE_TREADS: 1,
            MOVE_TIRES: 1
        }
    },
    TILE_TYPE_WALL: {
        "name": "Wall",
        "ids": [TILE_WALL_V,TILE_WALL_H,
                TILE_WALL_NE,TILE_WALL_ES,TILE_WALL_SW,TILE_WALL_WN,
                TILE_WALL_N,TILE_WALL_E,TILE_WALL_S,TILE_WALL_W],
        "def": 0,
        "move": {
            MOVE_INF: 0,
            MOVE_MCH: 0,
            MOVE_TREADS: 0,
            MOVE_TIRES: 0
        }
    }
}

tileTallFrameOrder = [
    TILE_MTN,
    TILE_WDS,
    TILE_HQ_P1,
    TILE_HQ_P2,
    TILE_CITY_N,
    TILE_CITY_P1,
    TILE_CITY_P2,
    TILE_FACT_N,
    TILE_FACT_P1,
    TILE_FACT_P2,
    TILE_WALL_V,
    TILE_WALL_H,
    TILE_WALL_NE,
    TILE_WALL_ES,
    TILE_WALL_SW,
    TILE_WALL_WN,
    TILE_WALL_N,
    TILE_WALL_E,
    TILE_WALL_S,
    TILE_WALL_W,
]

infoTileTypeFrameOrder = [
    TILE_TYPE_PLN,
    TILE_TYPE_MTN,
    TILE_TYPE_WDS,
    TILE_TYPE_RVR,
    TILE_TYPE_ROAD,
    TILE_TYPE_SEA,
    TILE_TYPE_BCH,
    TILE_TYPE_WALL
]
infoTileTallTypeFrameOrder = [
    TILE_TYPE_HQ,
    TILE_TYPE_HQ,
    TILE_TYPE_CITY,
    TILE_TYPE_FACT
]

moveDraws = { # frame, mirrorX, mirrorY
    (MOVE_DOWN,MOVE_DOWN): (0,0,0),
    (MOVE_RIGHT,MOVE_RIGHT): (1,0,0),
    (MOVE_DOWN,MOVE_RIGHT): (2,0,0),
    (MOVE_DOWN,MOVE_LEFT): (2,1,0),
    (MOVE_UP,MOVE_RIGHT): (2,0,1),
    (MOVE_UP,MOVE_LEFT): (2,1,1),
    (MOVE_RIGHT,None): (3,0,0),
    (MOVE_LEFT,None): (3,1,0),
    (MOVE_DOWN,None): (4,0,0),
    (MOVE_UP,None): (4,0,1),
    (None,MOVE_DOWN): (5,0,0),
    (None,MOVE_UP): (5,0,1),
    (None,MOVE_RIGHT): (6,0,0),
    (None,MOVE_LEFT): (6,1,0),
}

tileDefs = {}
for typeID in tileTypeDefs:
    for tileID in tileTypeDefs[typeID]["ids"]:
        tileDefs[tileID] = {
            "type": typeID,
            "team": TEAM_NEUTRAL,
        }
        
for tileID in [TILE_HQ_P1,TILE_CITY_P1,TILE_FACT_P1]:
    tileDefs[tileID]["team"] = TEAM_P1
    
for tileID in [TILE_HQ_P2,TILE_CITY_P2,TILE_FACT_P2]:
    tileDefs[tileID]["team"] = TEAM_P2

for f in range(len(infoTileTypeFrameOrder)):
    typeID = infoTileTypeFrameOrder[f]
    tileTypeDefs[typeID]["info"] = (f,False)
for f in range(len(infoTileTallTypeFrameOrder)):
    typeID = infoTileTallTypeFrameOrder[f]
    tileTypeDefs[typeID]["info"] = (f,True)
    
tileDrawFrames = [(False,i-1) for i in range(61)]
for f in range(len(tileTallFrameOrder)):
    id = tileTallFrameOrder[f]
    tileDrawFrames[id] = (True,f)
    
for k, v in [(k, moveDraws[k]) for k in moveDraws]:
    m1, m2 = k
    if m1 is None or m2 is None:
        continue
    moveDraws[((m2+2)%4,(m1+2)%4)] = v
    
    