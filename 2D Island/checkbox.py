import pygame
font = pygame.font.Font('freesansbold.ttf', 20)
class Checkbox:
    def __init__(self, pos, size,key, text, tabKey=None ,active=False, boxOffset=0):
        self.key = key
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        self.active = active
        self.mouseHeld = False
        self.tabKey = tabKey

        self.boxOffset = boxOffset

        self.text = font.render(text, True, (0,0,0))

    def update(self,win,mouseDown):
        self.returnValues = None, None
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos[0]-self.boxOffset, mousePos[1]+(self.text.get_rect().h//3)) and mouseDown and not(self.mouseHeld):
            self.active = not(self.active)
            self.returnValues =  self.key, self.active
        if mouseDown:
            self.mouseHeld = True
        else:
            self.mouseHeld = False
        self.draw(win)
        return self.returnValues
    def draw(self, win):
        win.blit(self.text, (self.pos[0] - self.text.get_rect().w, self.pos[1]-(self.text.get_rect().h//2)))
        pygame.draw.rect(win, (255,255,255), (self.pos[0]-self.boxOffset, self.pos[1]-(self.text.get_rect().h//3), self.size, self.size), 1)
        if self.active:
            pygame.draw.rect(win, (50,255,50), (self.pos[0]+3-self.boxOffset, self.pos[1]-(self.text.get_rect().h//3)+3, self.size-6, self.size-6))
