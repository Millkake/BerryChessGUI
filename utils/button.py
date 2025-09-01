import pygame as pg


class Button:
    def __init__(self, color, x, y, width, height, text='', on_click='button x was clicked'):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.on_click_return = on_click

        self.hover_color = (self.color[0] - 40, self.color[1] - 40, self.color[2] - 40)

    def draw(self, win, outline=(24,68,100)):
        color = self.color

        if self.is_over(pg.mouse.get_pos()):
            color = self.hover_color



        # Call this method to draw the button on the screen
        if outline:
            pg.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), border_radius=18)
            
        pg.draw.rect(win, color, (self.x, self.y, self.width, self.height), border_radius=18)
        
        if self.text != '':
            font = pg.font.SysFont('arial', 50)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
    
    def on_click(self):
        return self.on_click_return
    
