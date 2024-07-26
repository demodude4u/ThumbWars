import struct
import gc

class PackReader:
    def __init__(self, filePath):
        self.filePath = filePath
        self.file = None

    def __enter__(self):
        self.file = open(self.filePath, 'rb')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        self.file = None
        gc.collect()

    def readSection(self):
        # gc.collect()
        # print("Free",gc.mem_free())
        sizeBytes = self.file.read(2)
        size = struct.unpack('H', sizeBytes)[0]
        sectionData = self.file.read(size)
        return sectionData

    def readBitmap(self):
        w, h = struct.unpack('HH', self.readSection())
        bufBW = self.readSection()
        bufGS = self.readSection()
        return (bufBW, bufGS, None, w, h)

    def readBitmapAndMask(self):
        w, h = struct.unpack('HH', self.readSection())
        bufBW = self.readSection()
        bufGS = self.readSection()
        bufM = self.readSection()
        return (bufBW, bufGS, bufM, w, h)


with PackReader("/Games/ThumbWars/data.pack") as pack:
    
    bmpTitle = pack.readBitmap()
    
    bmpTiles = pack.readBitmap()
    bmpTilesTall = pack.readBitmapAndMask()
    bmpUnits = pack.readBitmapAndMask()
    bmpTileCursor = pack.readBitmapAndMask()
    bmpExplosion = pack.readBitmapAndMask()
    bmpHealth = pack.readBitmapAndMask()
    bmpMove = pack.readBitmapAndMask()
    bmpCapture = pack.readBitmapAndMask()
    bmpCaptureTiles = pack.readBitmapAndMask()
    bmpPoint = pack.readBitmapAndMask()
    bmpDamage = pack.readBitmap()
    bmpStatus = pack.readBitmapAndMask()
    
    bmpInfoUnits = pack.readBitmapAndMask()
    bmpInfoTiles = pack.readBitmap()
    bmpInfoTilesTall = pack.readBitmapAndMask()
    bmpInfoPlayer = pack.readBitmapAndMask()
    bmpInfoStar = pack.readBitmapAndMask()
    
    bmpBattleFaces = pack.readBitmap()
    bmpBattleNumbers = pack.readBitmapAndMask()
    bmpBattleBar = pack.readBitmapAndMask()