import pygame
from mapGen import *
from tab import *
from menu import *
from button import *
from slide import *
from checkbox import *

def generateIsland():
    global totalMap, islandSurface, totalMaskMap, islandPreMap, draw
    totalMap = addMaps(totalMaskMap, islandPreMap, 1.8,0.8)
    islandSurface = drawMap(totalMap, checkBoxVariables["islandIsMask"])
    draw = True
def generateNoiseButton():
    global draw, islandPreMap, noiseSurface
    islandPreMap = generateNoise(sliderVariables["noiseScale"], 0)
    noiseSurface = drawMap(islandPreMap, True)

    draw = True
def clearMask():
    global totalMaskMap, draw, maskSurface
    totalMaskMap = genEmptyMap()
    maskSurface = drawMap(totalMaskMap, True)
    draw = True

win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.init()

mouseDown = False
draw = True
# Surfaces
noiseSurface = pygame.Surface((500,500)).convert()
mapSurface = pygame.Surface((500,500)).convert()
maskSurface = pygame.Surface((500,500)).convert()
# Map Generation
maskMaps = []
totalMaskMap = genEmptyMap()

islandPreMap = generateNoise(sliderVariables["noiseScale"], 0)


# Tabs
numberOfTabs = 3
totalTabs = []
tabVariables = {"mask":True, "noise":False, "island":False}
checkBoxVariables = {"islandIsMask":False}
totalTabs.append(Tab([500+(0*(400/numberOfTabs)), 0], 400/numberOfTabs, 30, (100,100,100), (200,200,200), (150,150,150), "Mask", "mask", True))
totalTabs.append(Tab([500+(1*(400/numberOfTabs)), 0], 400/numberOfTabs, 30, (100,100,100), (200,200,200), (150,150,150), "Noise", "noise"))
totalTabs.append(Tab([500+(2*(400/numberOfTabs)), 0], 400/numberOfTabs, 30, (100,100,100), (200,200,200), (150,150,150), "Island", "island"))
# Buttons
totalButtons = []
totalButtons.append(Button([625,400], 150, 25, generateIsland, (), (180,180,180), (100,100,100), (150,150,150), "Generate" ,"island"))
totalButtons.append(Button([625,400], 150, 25, generateNoiseButton, (), (180,180,180), (100,100,100), (150,150,150), "Generate" ,"noise"))

totalButtons.append(Button([625,400], 150, 25, clearMask, (), (180,180,180), (100,100,100), (150,150,150), "Clear" ,"mask"))
# Slider
totalSliders = []
totalSliders.append(Slider(sliderVariables["maskRadius"], 0, 300, [590,100], "Radius: ", "maskRadius", "mask", True))
totalSliders.append(Slider(sliderVariables["maskWeight"], 0.2, 2, [593,140], "Weight: ", "maskWeight", "mask"))
totalSliders.append(Slider(sliderVariables["maskDropOff"], 1, 2, [605,180], "Drop Off: ", "maskDropOff", "mask"))
totalSliders.append(Slider(sliderVariables["pixelNum"], 0, 260, [640,height*0.95], "Resolution: ", "pixelNum", "mask", intergise=True, values=[50,100,250,500], length=175))

totalSliders.append(Slider(sliderVariables["islandGreenCutoff"], 0, 255, [620,140], "Green CO: ", "islandGreenCutoff", "island", intergise=True))
totalSliders.append(Slider(sliderVariables["islandSandCutOff"], 0, 255, [610,180], "Sand CO: ", "islandSandCutOff", "island", intergise=True))

totalSliders.append(Slider(sliderVariables["noiseScale"], 1.01, 20, [640,height*0.15], "Scale: ", "noiseScale", "noise", intergise=False, length=175))
# Checkbox
totalCheckBox = []
totalCheckBox.append(Checkbox([580, 100], 15, "islandIsMask", "Mask: ", "island"))
###
islandSurface = drawMap(totalMap).convert()
maskSurface = drawMap(totalMaskMap, isMask=True).convert()
noiseSurface = drawMap(islandPreMap, isMask=True).convert()

while True:
    drawSideMenu(win, tabVariables)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            mousePos = [mousePos[0]/(500/sliderVariables["pixelNum"]), mousePos[1]/(500/sliderVariables["pixelNum"])]

            mouseDown = True

            if tabVariables["mask"] and mousePos[0]<sliderVariables["pixelNum"]:
                newMask = generateMapMask(mousePos, sliderVariables["maskRadius"]/(500/sliderVariables["pixelNum"]), sliderVariables["maskWeight"], sliderVariables["maskDropOff"])
                totalMaskMap = addMaps(totalMaskMap, newMask, 1.49, 1)

                maskSurface = drawMap(totalMaskMap, True)

                draw = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
    for tempTab in totalTabs:
        key = tempTab.update(mouseDown, win, totalTabs)
        if key != None:
            draw = True
            for tempKey in tabVariables:
                if tempKey == key:
                    tabVariables[key] = True
                else:
                    tabVariables[tempKey] = False

    for tempSlider in totalSliders:
        if tabVariables[tempSlider.tabKey]:
            valueKey, value = tempSlider.update(win, mouseDown)
            if valueKey != None:
                if valueKey == "pixelNum":
                    oldValue = sliderVariables[valueKey]
                    if oldValue != value:
                        sliderVariables[valueKey] = value
                        sliderVariables["pixelSize"] = int(500/sliderVariables[valueKey])
                        totalMaskMap = genEmptyMap()
                        maskSurface = drawMap(totalMaskMap, True)

                        islandPreMap = generateNoise(sliderVariables["noiseScale"], 0)
                        noiseSurface = drawMap(islandPreMap, True)
                        draw = True
                else:
                    sliderVariables[valueKey] = value

    for tempButton in totalButtons:
        if tabVariables[tempButton.tabKey] or tempButton.tabKey == None:
            tempButton.update(mouseDown, win)

    for tempCheckBox in totalCheckBox:
        if tabVariables[tempCheckBox.tabKey] or tempCheckBox.tabKey == None:
            key, isActive = tempCheckBox.update(win, mouseDown)
            if key != None:
                checkBoxVariables[key] = isActive

    if tabVariables["mask"] and draw:
        win.blit(maskSurface, (0,0))
        draw = False
    elif tabVariables["noise"] and draw:
        win.blit(noiseSurface, (0,0))
        draw = False
    elif tabVariables["island"] and draw:
        win.blit(islandSurface, (0,0))
        draw = False
    pygame.display.update()
    clock.tick(60)


