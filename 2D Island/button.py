import pygame
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
class Button:
    def __init__(self, pos, length, width, functionOnPress, functionPar,colour, inactiveColour, hoverColour, text, tabKey=None):
        self.pos = pos
        self.length = length
        self.width = width

        self.text = text
        self.textSurface = font.render(self.text, True, (0,0,0))
        self.textSurfaceRect = self.textSurface.get_rect(center=(self.pos[0]+(self.length/2), self.pos[1]+(self.width/2)))

        self.func = functionOnPress
        self.funcPar = functionPar
        self.tabKey = tabKey

        self.mouseHover = False
        self.mouseWasDown = False

        self.colour = colour
        self.hoverColour = hoverColour
        self.inactiveColour = inactiveColour
    def update(self, mouseDown, win):
        self.mouseHover = False

        mousePos = pygame.mouse.get_pos()
        if pygame.Rect((self.pos[0],self.pos[1],self.length,self.width)).collidepoint(mousePos[0], mousePos[1]):
            self.mouseHover = True
        if mouseDown:
            self.mouseWasDown = True
        if not(mouseDown) and self.mouseWasDown and self.mouseHover:
            self.mouseWasDown = False
            self.draw(win, mouseDown)
            self.func(*self.funcPar)
        if not(mouseDown):
            self.mouseWasDown = False

        self.draw(win, mouseDown)
    def draw(self, win, mouseDown):
        if mouseDown and self.mouseHover:
            pygame.draw.rect(win, self.colour, (self.pos[0],self.pos[1],self.length, self.width))
        elif self.mouseHover:
            pygame.draw.rect(win, self.hoverColour, (self.pos[0],self.pos[1],self.length, self.width))
        else:
            pygame.draw.rect(win, self.inactiveColour, (self.pos[0],self.pos[1],self.length, self.width))
        win.blit(self.textSurface, self.textSurfaceRect)
