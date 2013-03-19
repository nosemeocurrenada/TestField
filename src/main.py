'''
Created on 17/03/2013

@author: Nikita
'''
import math

def tsum(a , b):
    return (a[0]+b[0],a[1]+b[1])


  
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
    
 
 
class Region():
    def __init__(self, mother):
        """ inicializa una region con su region madre"""
        self.mother = mother
        
    mother = None    
    daugther = [[],[]]    
    waiting = []

    def update(self, lista):
        """llama a actualizar de las regiones hijas pasandole las entidades de la lista, mas las entidades que ya tenia.
        Devuelve una lista con las entidades que retornaron las hijas que deben moverse afuera de esta region. 
        Las que se pueden mover dentro de esta region, quedan almacenadas en waiting hasta al proximo update"""
        for i in range(0,2):
            for j in range(0,2):
                if hasattr(self.daugther[i][j],"update"):
                    gift = []
                    for ent in self.waiting:
                        if ent.passport[-1] == (i,j):
                            gift.append(self.waiting.pop(-1))
                    ret = self.daugther[i][j].update(gift)
                    for e in ret:
                        e.passport.append((i,j))
                    self.waiting.extend(ret)
                    
        gift = []
        toremove = []
        
        for ent in self.waiting:
            
            entdest = tsum(ent.passport[-1],ent.direction)
            
            ent.passport[-1] = entdest[0] % 2 , entdest[1] % 2  
            
            if entdest[0] >= 2 or entdest[0] < 0 or entdest[1] >= 2 or entdest[1] < 0:
                gift.append(ent)
                toremove.append(ent)
        
        
        for ent in toremove:
            self.waiting.remove(ent)
        
        return gift
            
class RegionMin():
    def __init__(self, name, mother):
        """ inicializa una region con su region madre"""
        self.mother = mother
        self.name = name
        self.content = []

    
    def update(self, lista):
        print self.name + " : " + "-".join([ent.name for ent in self.content])
        for ent in lista:
            ent.direction = (0,0)
        self.content.extend(lista)
        
        toremove = []
        
        for ent in self.content:
            if ent.direction != (0,0):
                toremove.append(ent)
                
        for ent in toremove:
            self.content.remove(ent)
            
        return toremove
            
            
        
        
    
class entidadViajera():
    def __init__(self, name, content):
        self.content = content
        self.name = name
    name = None
    passport = []
    """el pasaporte es una queue de posisiones a las que tiene que ir"""
    direction = (0,0)
    content  = None
    
import pygame

if __name__ == '__main__':
    regMOM = Region(None)
    
    regA = Region(None)
    regA00 = RegionMin("regA00",regA)
    regA01 = RegionMin("regA01",regA)
    regA10 = RegionMin("regA10",regA)
    regA11 = RegionMin("regA11",regA)
    regA.daugther = [[regA00,regA10],[regA01,regA11]]
    
    regB = Region(None)
    regB00 = RegionMin("regB00",regB)
    regB01 = RegionMin("regB01",regB)
    regB10 = RegionMin("regB10",regB)
    regB11 = RegionMin("regB11",regB)
    regB.daugther = [[regB00,regB10],[regB01,regB11]]
    
    regC = Region(None)
    regC00 = RegionMin("regC00",regC)
    regC01 = RegionMin("regC01",regC)
    regC10 = RegionMin("regC10",regC)
    regC11 = RegionMin("regC11",regC)
    regC.daugther = [[regC00,regC10],[regC01,regC11]]
    
    regD = Region(None)
    regD00 = RegionMin("regD00",regD)
    regD01 = RegionMin("regD01",regD)
    regD10 = RegionMin("regD10",regD)
    regD11 = RegionMin("regD11",regD)
    regD.daugther = [[regD00,regD10],[regD01,regD11]]
    
    regMOM.daugther = [[regA,regB],[regC,regD]]
    
    
    carlos = entidadViajera("Carlos",8)    
    regA01.content.append(carlos)    
    
    pygame.init()
    
    screen = pygame.display.set_mode((100,100))
        
    doExit = False
    
    while not doExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                doExit = True
            if event.type == pygame.K_d:
                carlos.direction = (0,1)
            if event.type == pygame.K_w:
                carlos.direction = (-1,)
            if event.type == pygame.K_a:
                carlos.direction = (0,-1)
            if event.type == pygame.K_s:
                carlos.direction = (1,0)
            if event.type == pygame.K_SPACE:
                carlos.direction = (0,0)
    
        print "-".join([ent.name for ent in regMOM.update([])])
        
        pygame.time.delay(100)
        
        screen.fill((0,0,0))
        pygame.display.flip()
    
    
#    import pygame
#    pygame.init()
#    size = width, height = 320, 240
#    black = 0, 0, 0
#
#    screen = pygame.display.set_mode(size)
 
    #while 1:
        
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT: 
                #exit()
                
        #habitacion.update()
        #habitacion.draw(screen)
#        pygame.time.delay(10)
    
    

    