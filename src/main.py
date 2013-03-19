'''
Created on 17/03/2013

@author: Nikita
'''
    
class Entity():    
    def __init__(self, image, pos):
        """inicializa a la entidad con una imagen y una posision"""
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
    def update(self):
        print "YO (" + str(self) + ") ME UPDATIE"
    
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        
    image = None
    rect = None
    
    
class Pelota(Entity):    
    def __init__(self, image, pos, screenSize, speed):
        """inicializa a la entidad con una imagen y una posision"""
        Entity.__init__(self, image, pos)
        self.screenSize = screenSize
        self.speed = speed
        
    screenSize = None
    speed = [2,2]
        
    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.screenSize[0]:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > self.screenSize[1]:
            self.speed[1] = -self.speed[1]
    
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        
 
import random
    
class PersonaBoluda(Entity):
    def __init__(self, image, pos):
        """inicializa a la entidad con una imagen y una posision"""
        Entity.__init__(self, image, pos)
        
    def update(self):
        rnd = random.Random()
        rnd.seed()
        self.rect = self.rect.move(rnd.randint(-2, 2),rnd.randint(-2,2))
    
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        
        
        
class PersonaBoludaLenta(Entity):    
    def __init__(self, image, pos):
        """inicializa a la entidad con una imagen y una posision"""
        Entity.__init__(self, image, pos)
        
    def update(self):
        rnd = random.Random()
        rnd.seed()        
        self.rect = self.rect.move(rnd.randint(-1, 1),rnd.randint(-1,1))
    
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        
        
class PersonaBoludaRapida(Entity):
    def __init__(self, image, pos):
        """inicializa a la entidad con una imagen y una posision"""
        Entity.__init__(self, image, pos)
        
    def update(self):
        rnd = random.Random()
        rnd.seed()
        self.rect = self.rect.move(rnd.randint(-5, 5),rnd.randint(-5,5))
    
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        

class PersonaSumisa(Entity):
    def __init__(self, image, pos):
        """inicializa a la entidad con una imagen y una posision"""
        Entity.__init__(self, image, pos)
        
    def update(self):
        speed = [0,0]
        if pygame.key.get_pressed()[pygame.K_s]:
            speed[1] = speed[1] + 1
        if pygame.key.get_pressed()[pygame.K_w]:
            speed[1] = speed[1] - 1
        if pygame.key.get_pressed()[pygame.K_d]:
            speed[0] = speed[0] + 1
        if pygame.key.get_pressed()[pygame.K_a]:
            speed[0] = speed[0] - 1
            
        self.rect = self.rect.move(speed)
    
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        
        



class Room():
    def __init__(self, size):
        self.size = size
        
    size = None
    entitiesList = []
    
    def update(self):
        for entity in self.entitiesList:
            if hasattr(entity,"update"):
                entity.update()
            
    def draw(self, screen):
        screen.fill(( 0, 0, 0))
        for entity in self.entitiesList:
            if hasattr(entity,"draw"):
                entity.draw(screen)
        pygame.display.flip()
    
    
    
    
# TEMIBLE MAIN !!!!
    
if __name__ == '__main__':
    import pygame
    pygame.init()
    size = width, height = 320, 240
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    pelota = Pelota(pygame.image.load("resources/images/ball.png"), (90,90), size, [1,1])
    pepe = PersonaBoluda(pygame.image.load("resources/images/pepe.png"), (250,180))
    carlos = PersonaSumisa(pygame.image.load("resources/images/carlos.png"), (150,180))
    jacinto = PersonaBoludaLenta( pygame.image.load("resources/images/jacinto.bmp"), (70,120))
    juan = PersonaBoludaRapida(pygame.image.load("resources/images/juan.bmp"), (50,80))
    habitacion = Room(size)
    habitacion.entitiesList.append(jacinto)    
    habitacion.entitiesList.append(pelota)
    habitacion.entitiesList.append(pepe)
    habitacion.entitiesList.append(juan)
    habitacion.entitiesList.append(carlos)
    
    while 1:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()
                
        habitacion.update()
        habitacion.draw(screen)
        pygame.time.delay(10)
    
    

    