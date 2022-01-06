import math, pygame,noise
width = 900
height = 500

# Sliders
sliderVariables = {"maskRadius":50, "pixelNum":100, "pixelSize":int(500/100), "noiseScale":20, "maskWeight":1, "maskDropOff":1, "islandGreenCutoff":200, "islandSandCutOff":150}

def mapNum(value, min1, max1, min2, max2):
    if value > max1:
        value = max1
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2
def distance(point1, point2):
    return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)

def generateMapMask(pos, radius, maskWeight, maskDropOff):
    islandMap = []
    rowsToAdd = 0
    for y in range(int(pos[1]-radius)):
        if y > 0:
            mapColoumn = []
            for x in range(sliderVariables["pixelNum"]):
                mapColoumn.append(0)
            islandMap.append(mapColoumn)
        else:
            rowsToAdd += 1

    for y in range(int(pos[1]-radius), int(pos[1]+radius)):
        if y > 0:
            mapColoumn = []
            for x in range(sliderVariables["pixelNum"]):
                distanceFromMiddle = distance([x,y], pos)
                if distanceFromMiddle <= radius:
                    distanceFromMiddle /= maskDropOff
                mapColoumn.append(mapNum(distanceFromMiddle, 0, radius, 255, 0)*maskWeight)
            islandMap.append(mapColoumn)
        else:
            rowsToAdd += 1

    for y in range(int(pos[1]+radius), sliderVariables["pixelNum"]):
        mapColoumn = []
        for x in range(sliderVariables["pixelNum"]):
            mapColoumn.append(0)
        islandMap.append(mapColoumn)

    for row in range(rowsToAdd):
        mapColoumn = []
        for x in range(sliderVariables["pixelNum"]):
            mapColoumn.append(0)
        islandMap.append(mapColoumn)
    return islandMap
def generateNoise(scale, seed):
    islandMap = []
    for y in range(sliderVariables["pixelNum"]):
        mapColoumn = []
        for x in range(sliderVariables["pixelNum"]):
            mapColoumn.append((noise.pnoise2((x+seed)/scale,(y+seed)/scale)+1)*127.5)
        islandMap.append(mapColoumn)
    return islandMap
def genEmptyMap():
    emptyMap = []
    for y in range(sliderVariables["pixelNum"]):
        mapColoumn = []
        for x in range(sliderVariables["pixelNum"]):
            mapColoumn.append(0)
        emptyMap.append(mapColoumn)
    return emptyMap
totalMap = genEmptyMap()
def drawMap(map, isMask=False):
    tempSurface = pygame.Surface((500,500))
    for y in range(len(map)):
        for x in range(len(map[y])):
            height = map[y][x]
            if not(isMask):
                if height > sliderVariables["islandGreenCutoff"]:
                    height = mapNum(height, sliderVariables["islandGreenCutoff"], 300, 150, 255)
                    colour = (50,height,50)
                elif height > sliderVariables["islandSandCutOff"]:
                    colour = (194,175,128)
                else:
                    height = mapNum(height, 0, 150, 100, 150)
                    colour = (0,0, height)
            else:
                colour = (height, height, height)
            pygame.draw.rect(tempSurface, colour, (x*sliderVariables["pixelSize"], y*sliderVariables["pixelSize"], sliderVariables["pixelSize"], sliderVariables["pixelSize"]))
            # pygame.draw.rect(win,(colour, colour, colour), (x*pixelSize, y*pixelSize, pixelSize, pixelSize))
    return tempSurface
def addMaps(maskMap, noiseMap, maskMapScale, noiseMapScale):
    addMap = []
    for y in range(len(maskMap)):
        addMapCol = []
        for x in range(len(maskMap[y])):
            height = (maskMap[y][x]*maskMapScale + noiseMap[y][x]*noiseMapScale)
            addMapCol.append(mapNum(height, 0, 380, 0, 255))
        addMap.append(addMapCol)
    return addMap
def addMasks(totalMasksMaps):
    currentMaskMap = genEmptyMap()
    for tempMaskMap in totalMasksMaps:
        currentMaskMap = addMaps(currentMaskMap, tempMaskMap, 1.5, 1)
    return currentMaskMap

# for y in range(int(pos[1]-radius), int(pos[1]+radius)):
#         mapColoumn = []
#         for x in range(pixelNum):
#             distanceFromMiddle = distance([x,y], pos)
#             mapColoumn.append(mapNum(distanceFromMiddle, 0, radius, 255, 0))
#         islandMap.append(mapColoumn)
