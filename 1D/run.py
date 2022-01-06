import pygame, mapGeneration, slide, checkbox, noise

width = 1000
height = 500

win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.init()

pixelNum = width
pixelSize = int(width/pixelNum)

mouseDown = False

tittleFont = pygame.font.Font('freesansbold.ttf', 20)

def drawWorld(world, yOffset):
    tempWorld = []
    xoffset = 0
    for pixel in range(0, len(world)):

        if checkBoxVariables["xNoise"]:
            xoffset = abs(noise.pnoise1((pixel+variables["totalXOffset"]*5)/(variables["xScale"]+1),octaves=int(variables["xOctaves"]), lacunarity=variables["xLacunarity"], persistence=variables["xPersistence"])*variables["xHeight"])
        pygame.draw.rect(win, (255,255,255), (pixel*pixelSize + xoffset, height-world[pixel]-pixelSize-yOffset, pixelSize, pixelSize))
        if checkBoxVariables["drawLines"]:
            tempWorld.append([pixel*pixelSize + xoffset, height-world[pixel]-pixelSize-yOffset])
    tempWorld.append([width, height-world[len(world)-1]-pixelSize-yOffset])
    if checkBoxVariables["drawLines"]:
        tempWorld.append([width,height])
        tempWorld.append([0, height])
        pygame.draw.polygon(win, (255,255,255), tempWorld)

variables = {"scale": 100, "octaves": 1, "persistence":0.1, "lacunarity":2, "yOffset":150, "totalXOffset":0, "height": 50,
             "xScale":100, "xOctaves":1, "xPersistence": 0.1, "xLacunarity":2, "xHeight":50}
# Sliders
sliders = []
sliders.append(slide.Slider(variables["scale"], 1, 300, (width*0.41, height*0.1), "Scale: ", "scale"))
sliders.append(slide.Slider(variables["height"], 0, 300, (width*0.42, height*0.15), "Height: ", "height"))
sliders.append(slide.Slider(variables["octaves"], 1, 10, (width*0.422, height*0.2), "Octave: ", "octaves", True))
sliders.append(slide.Slider(variables["lacunarity"], 1, 5, (width*0.46, height*0.25), "Lacunarity: ", "lacunarity"))
sliders.append(slide.Slider(variables["persistence"], 0.1, 10, (width*0.468, height*0.3), "Persistence: ", "persistence"))

sliders.append(slide.Slider(variables["xScale"], 1, 1000, (width*0.788, height*0.1), "Scale: ", "xScale"))
sliders.append(slide.Slider(variables["xHeight"], 0, 200, (width*0.8, height*0.15), "Height: ", "xHeight"))
sliders.append(slide.Slider(variables["xOctaves"], 1, 10, (width*0.802, height*0.2), "Octave: ", "xOctaves", True))
sliders.append(slide.Slider(variables["xLacunarity"], 1, 5, (width*0.841, height*0.25), "Lacunarity: ", "xLacunarity"))
sliders.append(slide.Slider(variables["xPersistence"], 0.1, 10, (width*0.85, height*0.3), "Persistence: ", "xPersistence"))

sliders.append(slide.Slider(variables["yOffset"], -50, 500, (width*0.1, height*0.1), "Y Offset: ", "yOffset"))
sliders.append(slide.Slider(variables["totalXOffset"], -500, 500, (width*0.1, height*0.15), "X Offset: ", "totalXOffset"))
# CheckBoxes
checkBoxes = []
checkBoxes.append(checkbox.Checkbox([width*0.13, height*0.2], 15, "drawLines", "Fill Ground: ",True, 30))
checkBoxes.append(checkbox.Checkbox([width*0.16, height*0.25], 15, "xNoise", "X-Offset Noise: ",True))
# Tittles
tittles = []
tittles.append([tittleFont.render("Controls", True, (180,180,180)), [width*0.08,10], None])
tittles.append([tittleFont.render("Height Noise", True, (180,180,180)), [width*0.4,10], None])
tittles.append([tittleFont.render("X-Offset Noise", True, (180,180,180)), [width*0.78,10], "xNoise"])

world = mapGeneration.generatePerlinMap(pixelNum, variables["scale"], variables["octaves"], variables["persistence"], variables["lacunarity"], variables["totalXOffset"], variables["height"])
checkBoxVariables = {"drawLines":True, "xNoise":True}
while True:
    generateWorld = False
    win.fill((0,0,0))
    drawWorld(world, variables["yOffset"])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
    for slider in sliders:
        if slider.key[0] != "x":
            key, updatedVariable = slider.update(win, mouseDown)
            if key != None:
                variables[key] = updatedVariable
                generateWorld = True
        elif slider.key[0] == "x" and checkBoxVariables["xNoise"]:
            key, updatedVariable = slider.update(win, mouseDown)
            if key != None:
                variables[key] = updatedVariable
                generateWorld = True
    for tempCheckBox in checkBoxes:
        key, value = tempCheckBox.update(win, mouseDown)
        if key != None:
            checkBoxVariables[key] = value
    if generateWorld:
        world = mapGeneration.generatePerlinMap(pixelNum, variables["scale"], variables["octaves"], variables["persistence"], variables["lacunarity"], variables["totalXOffset"], variables["height"])
    for tittle in tittles:
        if tittle[2] == None:
            win.blit(tittle[0], tittle[1])
        elif checkBoxVariables[tittle[2]]:
            win.blit(tittle[0], tittle[1])
    pygame.display.update()
    clock.tick(60)


