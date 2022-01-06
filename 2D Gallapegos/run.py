import pygame, slide
from mapGeneration import *



win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.init()



variables = {"octave":1, "greenCutOff":200, "sandCutOff":150, "scale":10, "persistence":0.2, "lacunarity":2.0}
sliders = []
sliders.append(slide.Slider(variables["scale"], 2, 20, (width*0.725, height*0.05), "Scale: ", "scale", True))
sliders.append(slide.Slider(variables["octave"], 1, 10, (width*0.74, height*0.1), "Octave: ", "octave", True))
sliders.append(slide.Slider(variables["persistence"], 0.1, 5, (width*0.8, height*0.15), "Persistence: ", "persistence"))
sliders.append(slide.Slider(variables["lacunarity"], 1, 5, (width*0.79, height*0.2), "Lacunarity: ", "lacunarity"))



sliders.append(slide.Slider(variables["greenCutOff"], 0, 255, (width*0.77, height*0.9), "Green CO: ", "greenCutOff", True))
sliders.append(slide.Slider(variables["sandCutOff"], 0, 255, (width*0.76, height*0.95), "Sand CO: ", "sandCutOff", True))
def mapNum(value, min1, max1, min2, max2):
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2
def drawMap(worldMap):
    win.fill((150,150,150))
    for yStrip in range(len(worldMap)):
        for x in range(len(worldMap[yStrip])):
            height = worldMap[yStrip][x]
            height = mapNum(height, -1, 1, 0, 255)
            if height > variables["greenCutOff"]:
                colour = (50,height,50)
            elif height > variables["sandCutOff"]:
                colour = (194,175,128)
            else:
                height = mapNum(height, 0, variables["sandCutOff"], 175, 255)
                colour = (0,0, height)
            pygame.draw.rect(win, colour, (x*pixelSize, yStrip*pixelSize, pixelSize, pixelSize))
worldMap = generateMap(pixelNum, variables["scale"], variables["octave"], variables["persistence"], variables["lacunarity"])
drawMap(worldMap)
mouseDown = False
renderWorld = True
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
    for slider in sliders:
        key, value = slider.update(win, mouseDown)
        if key != None:
            variables[key] = value
            renderWorld = True
    if renderWorld:
        worldMap = generateMap(pixelNum, variables["scale"], variables["octave"], variables["persistence"], variables["lacunarity"])
        drawMap(worldMap)
        for slider in sliders:
            slider.draw(win)
    pygame.display.update()
    clock.tick(60)
    renderWorld = False


