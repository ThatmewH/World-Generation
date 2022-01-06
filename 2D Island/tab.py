import pygame
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
class Tab:
    def __init__(self, pos, length, width, inactiveColour, activeColour, hoverColour, text, key, active=False):
        self.pos = pos
        self.length = length
        self.width = width
        self.key = key

        self.text = text
        self.textSurface = font.render(self.text, True, (0,0,0))
        self.textSurfaceRect = self.textSurface.get_rect(center=(self.pos[0]+(self.length/2), self.pos[1]+(self.width/2)))

        self.activeColour = activeColour
        self.inactiveColour = inactiveColour
        self.hoverColour = hoverColour

        self.active = active
        self.mouseHover = False
    def update(self, mouseDown, win, totalTabs):
        mousePos = pygame.mouse.get_pos()
        self.mouseHover = False
        if pygame.Rect((self.pos[0], self.pos[1], self.length, self.width)).collidepoint(mousePos[0], mousePos[1]):
            self.mouseHover = True
            if mouseDown:
                self.mouseHover = False
                self.active = True
                for tempTab in totalTabs:
                    if tempTab.active == True and tempTab != self:
                        tempTab.active = False
                self.draw(win)
                return self.key
        self.draw(win)
        return None
    def draw(self, win):
        if self.active:
            pygame.draw.rect(win, self.activeColour, (self.pos[0], self.pos[1], self.length, self.width))
        elif self.mouseHover:
            pygame.draw.rect(win, self.hoverColour, (self.pos[0], self.pos[1], self.length+1, self.width))
            pygame.draw.line(win, (0,0,0), (self.pos[0]+self.length-2, self.pos[1]+self.width-1), (self.pos[0]-2, self.pos[1]+self.width-1), 2)
            pygame.draw.line(win, (0,0,0), (self.pos[0]-2, self.pos[1]), (self.pos[0]-2, self.pos[1]+self.width-1), 2)
        else:
            pygame.draw.rect(win, self.inactiveColour, (self.pos[0], self.pos[1], self.length+1, self.width))
            pygame.draw.line(win, (0,0,0), (self.pos[0]+self.length-2, self.pos[1]+self.width-1), (self.pos[0]-2, self.pos[1]+self.width-1), 2)
            pygame.draw.line(win, (0,0,0), (self.pos[0]-2, self.pos[1]), (self.pos[0]-2, self.pos[1]+self.width-1), 2)
        win.blit(self.textSurface, self.textSurfaceRect)
        pygame.draw.line(win, (0,0,0), (self.pos[0]+self.length-2, self.pos[1]), (self.pos[0]+self.length-2, self.pos[1]+self.width-1), 2)
