import random, noise

width = 800
height = 500

pixelNum = 100
pixelSize = int(500/pixelNum)

def generateMap(pixelNum, scale, octaves, persistence, lacunarity):
    worldMap = []
    for y in range(pixelNum):
        yStrip = []
        for x in range(pixelNum):
            height = (noise.pnoise2(x/scale/2, y/scale/2,octaves=octaves, persistence=persistence, base=0, lacunarity=lacunarity))
            yStrip.append(height)
        worldMap.append(yStrip)
    return worldMap
