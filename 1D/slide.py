import pygame, math
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)

def mapNum(value, min1, max1, min2, max2):
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2

class Slider:
    def __init__(self, value, minValue, maxValue, pos, text, key, intergise=False):
        value = value
        if intergise:
            value = int(value)

        self.minValue = minValue
        self.maxValue = maxValue

        self.key = key
        self.lenght = 100
        self.pos = pos
        self.circlePos = [int(self.pos[0]+(mapNum(value, self.minValue, self.maxValue, 0, self.lenght))), int(self.pos[1])]

        self.held = False
        self.moving = False

        self.text = font.render(text, True, (150,150,150))
        self.textValue = font.render(str(value), True, (150,150,150))

        self.integer = intergise
    def update(self, win, mouseDown):
        mousePos = pygame.mouse.get_pos()
        distanceToMouse = math.sqrt((self.circlePos[0] - mousePos[0])**2 + (self.circlePos[1] - mousePos[1])**2)
        if not(mouseDown):
            self.held = False
            self.moving = False
        else:
            self.held = True
        if distanceToMouse < 5 and self.held:
            self.moving = True
        if self.moving:
            self.circlePos[0] = mousePos[0]

        if self.circlePos[0] > self.pos[0] + self.lenght:
            self.circlePos[0] = self.pos[0] + self.lenght
        if self.circlePos[0] < self.pos[0]:
            self.circlePos[0] = self.pos[0]
        self.draw(win)
        # Update Value
        if self.held and self.moving:
            value = mapNum(self.circlePos[0], self.pos[0], self.pos[0]+self.lenght, self.minValue, self.maxValue)
            if self.integer:
                value = int(value)
            self.textValue = font.render(str(round(value,2)), True, (150,150,150))
            return self.key, value
        return None, None
    def draw(self, win):
        win.blit(self.text, (self.pos[0]-self.text.get_rect().w, self.pos[1] - (self.text.get_rect().h//2)))
        win.blit(self.textValue, (self.pos[0] + self.lenght+15, self.pos[1] - (self.textValue.get_rect().h//2)))
        pygame.draw.line(win, (150,150,150), (self.pos[0], self.pos[1]), (self.pos[0]+self.lenght, self.pos[1]))
        pygame.draw.circle(win, (200,200,200), (int(self.circlePos[0]), int(self.circlePos[1])), 5)
