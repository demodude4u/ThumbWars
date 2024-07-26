import xml.etree.ElementTree as ET
import json
import struct
from array import array
from PIL import Image

# Color Codes
CC_BLACK = 0b00
CC_WHITE = 0b01
CC_DARK_GRAY = 0b10
CC_LIGHT_GRAY = 0b11
CC_TRANSPARENT = -1

CC_LOOKUP = {
    0xffffff: CC_WHITE,
    0xa2a2a2: CC_LIGHT_GRAY,
    0x4e4e4e: CC_DARK_GRAY,
    0x000000: CC_BLACK,
    0x008000: CC_TRANSPARENT
}


class PackWriter:
    def __init__(self):
        self.data = b''
        self.cd = ""

    def writeSection(self, data):
        size = len(data)
        sizeBytes = struct.pack('H', size)
        self.data += sizeBytes + data
        print("\t", size, " bytes")

    def writeImage(self, filePath, tile=None, masked=True):
        print("IM" if masked else "I", filePath)
        image = Image.open(self.cd+filePath).convert("RGB")

        if tile is None:
            tile = (image.width, image.height)
        tw, th = tile

        rows = (image.height+th-1) // th
        cols = (image.width+tw-1) // tw
        tileDataSize = tw * ((th + 7) // 8)
        bufferDataSize = tileDataSize * rows * cols
        bufferBW = bytearray(bufferDataSize)
        bufferGS = bytearray(bufferDataSize)
        bufferM = bytearray(bufferDataSize)

        pixels = image.getdata()
        i = 0
        for ty in range(0,image.height,th):
            for tx in range(0,image.width,tw):
                for y1 in range(ty,ty+th,8):
                    for x in range(tx,tx+tw):
                        vBW = 0
                        vGS = 0
                        vM = 0
                        b = 0
                        for y in range(y1,y1+8):
                            try:
                                if 0 <= x < image.width and 0 <= y < image.height and tx <= x < (tx+tw) and ty <= y < (ty+th):
                                    pixel = pixels[image.width*y+x]
                                    rgb = pixel[0] << 16 | pixel[1] << 8 | pixel[2]
                                    cc = CC_LOOKUP[rgb]
                                else:
                                    cc = CC_TRANSPARENT
                                
                                if cc == CC_TRANSPARENT:
                                    mask = 0
                                    cc = CC_BLACK
                                else:
                                    mask = 1

                                vBW |= (cc & 0b1) << b
                                vGS |= ((cc >> 1) & 0b1) << b
                                vM |= mask << b
                                b += 1
                            except KeyError:
                                raise ValueError(
                                    "Unknown color encountered: {:#06x}".format(rgb))
                        bufferBW[i] = vBW
                        bufferGS[i] = vGS
                        bufferM[i] = vM
                        i += 1
        self.writeSection(struct.pack('HH', tw, th))
        self.writeSection(bufferBW)
        self.writeSection(bufferGS)
        if masked:
            self.writeSection(bufferM)

    def save(self, filePath):
        with open(self.cd+filePath, 'wb') as file:
            file.write(self.data)
        print("Saved", filePath)

pack = PackWriter()

pack.cd = "../assets/"

pack.writeImage("title.png",(66,20),masked=False)

pack.writeImage("tiles.png",(8,6),masked=False)
pack.writeImage("tiles_tall.png",(8,12))
pack.writeImage("units.png",(10,10))
pack.writeImage("tile_cursor.png")
pack.writeImage("explosion.png",(20,20))
pack.writeImage("health.png",(7,7))
pack.writeImage("move.png",(8,8))
pack.writeImage("capture.png",(14,25))
pack.writeImage("capture_tiles.png",(15,32))
pack.writeImage("point.png")
pack.writeImage("damage.png",(5,7),masked=False)
pack.writeImage("status.png",(7,7))

pack.writeImage("info_units.png",(16,16))
pack.writeImage("info_tiles.png",(15,16),masked=False)
pack.writeImage("info_tiles_tall.png",(15,32))
pack.writeImage("info_player.png",(14,10))
pack.writeImage("info_star.png",(14,14))

pack.writeImage("battle_faces.png",(37,37),masked=False)
pack.writeImage("battle_numbers.png",(13,11))
pack.writeImage("battle_bar.png")

pack.cd = "../"

pack.save("data.pack")
