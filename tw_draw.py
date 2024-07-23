
from thumbyGrayscale import display
        
@micropython.viper
def draw_blitFrame(src, x:int, y:int, frame:int):
    buffer = ptr8(display.buffer)
    shading = ptr8(display.shading)

    src1 = ptr8(src[0])
    src2 = ptr8(src[1])
    width = int(src[3])
    height = int(src[4])

    if x+width < 0 or x >= 72:
        return
    if y+height < 0 or y >= 40:
        return
    
    stride = width
    
    fsize = width * ((height+7)>>3)

    srcx = 0 ; srcy = 0
    dstx = x ; dsty = y
    sdx = 1
    if dstx < 0:
        srcx = 0 - dstx
        width += dstx
        dstx = 0
    if dstx+width > 72:
        width = 72 - dstx
    if dsty < 0:
        srcy = 0 - dsty
        height += dsty
        dsty = 0
    if dsty+height > 40:
        height = 40 - dsty

    srco = (srcy >> 3) * stride + srcx
    srcm = 1 << (srcy & 7)
    
    if frame > 0:
        srco += fsize * frame

    dsto = (dsty >> 3) * 72 + dstx
    dstm = 1 << (dsty & 7)
    dstim = 255 - dstm

    while height != 0:
        srcco = srco
        dstco = dsto
        i = width
        while i != 0:
            v = 0
            if src1[srcco] & srcm:
                v = 1
            if src2[srcco] & srcm:
                v |= 2
            if v & 1:
                buffer[dstco] |= dstm
            else:
                buffer[dstco] &= dstim
            if v & 2:
                shading[dstco] |= dstm
            else:
                shading[dstco] &= dstim
            srcco += sdx
            dstco += 1
            i -= 1
        dstm <<= 1
        if dstm & 0x100:
            dsto += 72
            dstm = 1
            dstim = 0xfe
        else:
            dstim = 255 - dstm
        srcm <<= 1
        if srcm & 0x100:
            srco += stride
            srcm = 1
        height -= 1
    
@micropython.viper
def draw_blitMaskedFrame(src, x:int, y:int, frame:int):
    buffer = ptr8(display.buffer)
    shading = ptr8(display.shading)

    src1 = ptr8(src[0])
    src2 = ptr8(src[1])
    maskp = ptr8(src[2])
    width = int(src[3])
    height = int(src[4])

    if x+width < 0 or x >= 72:
        return
    if y+height < 0 or y >= 40:
        return
    
    stride = width
    
    fsize = width * ((height+7)>>3)

    srcx = 0 ; srcy = 0
    dstx = x ; dsty = y
    sdx = 1
    if dstx < 0:
        srcx = 0 - dstx
        width += dstx
        dstx = 0
    if dstx+width > 72:
        width = 72 - dstx
    if dsty < 0:
        srcy = 0 - dsty
        height += dsty
        dsty = 0
    if dsty+height > 40:
        height = 40 - dsty

    srco = (srcy >> 3) * stride + srcx
    srcm = 1 << (srcy & 7)
    
    if frame > 0:
        srco += fsize * frame

    dsto = (dsty >> 3) * 72 + dstx
    dstm = 1 << (dsty & 7)
    dstim = 255 - dstm

    while height != 0:
        srcco = srco
        dstco = dsto
        i = width
        while i != 0:
            if maskp[srcco] & srcm:
                if src1[srcco] & srcm:
                    buffer[dstco] |= dstm
                else:
                    buffer[dstco] &= dstim
                if src2[srcco] & srcm:
                    shading[dstco] |= dstm
                else:
                    shading[dstco] &= dstim
            srcco += sdx
            dstco += 1
            i -= 1
        dstm <<= 1
        if dstm & 0x100:
            dsto += 72
            dstm = 1
            dstim = 0xfe
        else:
            dstim = 255 - dstm
        srcm <<= 1
        if srcm & 0x100:
            srco += stride
            srcm = 1
        height -= 1
        
@micropython.viper
def draw_blitMaskedMirroredFrame(src, x:int, y:int, mirrorX:int, mirrorY:int, frame:int):
    buffer = ptr8(display.buffer)
    shading = ptr8(display.shading)

    src1 = ptr8(src[0])
    src2 = ptr8(src[1])
    maskp = ptr8(src[2])
    width = int(src[3])
    height = int(src[4])

    if x+width < 0 or x >= 72:
        return
    if y+height < 0 or y >= 40:
        return
    
    stride = width
    
    fsize = width * ((height+7)>>3)

    srcx = 0 ; srcy = 0
    dstx = x ; dsty = y
    sdx = 1
    if mirrorX:
        sdx = -1
        srcx += width - 1
        if dstx < 0:
            srcx += dstx
            width += dstx
            dstx = 0
    else:
        if dstx < 0:
            srcx = 0 - dstx
            width += dstx
            dstx = 0
    if dstx+width > 72:
        width = 72 - dstx
    if mirrorY:
        srcy = height - 1
        if dsty < 0:
            srcy += dsty
            height += dsty
            dsty = 0
    else:
        if dsty < 0:
            srcy = 0 - dsty
            height += dsty
            dsty = 0
    if dsty+height > 40:
        height = 40 - dsty

    srco = (srcy >> 3) * stride + srcx
    srcm = 1 << (srcy & 7)
    
    if frame > 0:
        srco += fsize * frame

    dsto = (dsty >> 3) * 72 + dstx
    dstm = 1 << (dsty & 7)
    dstim = 255 - dstm

    while height != 0:
        srcco = srco
        dstco = dsto
        i = width
        while i != 0:
            if maskp[srcco] & srcm:
                if src1[srcco] & srcm:
                    buffer[dstco] |= dstm
                else:
                    buffer[dstco] &= dstim
                if src2[srcco] & srcm:
                    shading[dstco] |= dstm
                else:
                    shading[dstco] &= dstim
            srcco += sdx
            dstco += 1
            i -= 1
        dstm <<= 1
        if dstm & 0x100:
            dsto += 72
            dstm = 1
            dstim = 0xfe
        else:
            dstim = 255 - dstm
        if mirrorY:
            srcm >>= 1
            if srcm == 0:
                srco -= stride
                srcm = 0x80
        else:
            srcm <<= 1
            if srcm & 0x100:
                srco += stride
                srcm = 1
        height -= 1