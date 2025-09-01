import pygame as pg 

'''SPRITESHEET class by TheLostSamoerai'''
'''Made for pygame'''
'''HOW TO USE:
1. initialize the spritsheetclass by giving it a path
2. you can then load a single image via a coordinate or you can load a row
3. to load a row you need a starting coord, an amount of images to return and the width of th image'''

class Spritesheet:
    def __init__(self, sheet_path):
        self.spritesheet = pg.image.load(sheet_path).convert()


    def load_single(self, start_pos=[0,0], size_x=16, size_y=16, colorkey=(0,0,0), scale=1):
        image_surface = pg.Surface((size_x, size_y)).convert_alpha()
        image_surface.blit(self.spritesheet, (0, 0), (start_pos[0], start_pos[1], start_pos[0] + size_x, start_pos[1] + size_y))
        image_surface = pg.transform.scale(image_surface, (scale*size_x, scale*size_y))

        image_surface.set_colorkey(colorkey)

        return image_surface
    
    def load_row(self, start_pos=[0,0], size_x=16, size_y=16, amount=3, colorkey=(0,0,0), scale=1):
        images = []
        self.current_pos = start_pos
        for i in range(amount):
            image = self.load_single(start_pos=self.current_pos, size_x=size_x, size_y=size_y, colorkey=colorkey, scale=scale)
            images.append(image)
            self.current_pos[0] += size_x
    
        
        return images


    def load_multrows(self, start_pos=[0,0], size_x=16, size_y=16, amountx=3, amounty=3, colorkey=(0,0,0), scale=1):
        images = []
        self.current_pos = start_pos[:]
        for j in range(amounty):
            for i in range(amountx):
                image = self.load_single(start_pos=self.current_pos, size_x=size_x, size_y=size_y, colorkey=colorkey, scale=scale)
                images.append(image)
                self.current_pos[0] += size_x
            self.current_pos[1] += size_y
            self.current_pos[0] = start_pos[0]

        return images  


        