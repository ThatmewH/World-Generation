import random, noise

def generateRandomMap(pixelNum):
    world = []
    for pixel in range(0, pixelNum):
        world.append(random.randint(0,200))
    return world

def generatePerlinMap(pixelNum, scale, octaves, persistence, lacunarity, xOffset, height):
    world = []

    scale = scale
    octaves = octaves
    persistence = persistence
    lacunarity = lacunarity
    height = height

    seed = xOffset*5

    for pixel in range(0, pixelNum):
        world.append(noise.pnoise1((pixel+seed)/scale+1,octaves=int(octaves), persistence=persistence, lacunarity=lacunarity)*height)
    return world
