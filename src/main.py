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
        self.daugther = [[],[]]
        self.waiting = []
    
    def draw(self, indent):
        space = ""
        for i in range(0,indent):
            space = space + "           "
        for i in range(0,2):
            for j in range(0,2):
                print space + "reg " + str((i,j)) + ":"
                if hasattr(self.daugther[i][j],"draw"):
                    self.daugther[i][j].draw(indent+1)


    def update(self, lista):
        """llama a actualizar de las regiones hijas pasandole las entidades de la lista, mas las entidades que ya tenia.
        Devuelve una lista con las entidades que retornaron las hijas que deben moverse afuera de esta region. 
        Las que se pueden mover dentro de esta region, quedan almacenadas en waiting hasta al proximo update"""
        
        self.waiting.extend(lista)
        for i in range(0,2):
            for j in range(0,2):
                if hasattr(self.daugther[i][j],"update"):
                    gift = []
                    for ent in self.waiting:
                        if ent.passport[-1] == (i,j):
                            ent.backup.append(ent.passport.pop(-1))
                            gift.append(self.waiting.pop(-1))
                    ret = self.daugther[i][j].update(gift)
                    for e in ret:
                        e.passport.append((i,j))
                    self.waiting.extend(ret)
                else:
                    for ent in self.waiting:
                        if ent.passport[-1] == (i,j):
                            ent.direction = -ent.direction[0],-ent.direction[1]
                            
                            for i in range(0,ent.passport.__len__()-1):
                                ent.passport[i] = ( ent.passport[i][0] + ent.direction[0] ) % 2 , ( ent.passport[i][1] - ent.direction[1] ) % 2 
                             
        toremove = []
        
        for ent in self.waiting:
            if   ent.passport[-1][0] + ent.direction[0] > 1:
                toremove.append(ent)
            elif ent.passport[-1][0] + ent.direction[0] < 0:
                toremove.append(ent)
            elif ent.passport[-1][1] + ent.direction[1] > 1:
                toremove.append(ent)
            elif ent.passport[-1][1] + ent.direction[1] < 0:
                toremove.append(ent)
            
            ent.passport[-1] = (( ent.passport[-1][0] + ent.direction[0] ) % 2 , ( ent.passport[-1][1] + ent.direction[1] ) % 2 )
                
        if self.mother != None:
            for ent in toremove:
                self.waiting.remove(ent)
        else:
            for ent in toremove:
                for i in range(0,ent.passport.__len__()):
                    ent.passport[i] = ( ent.passport[i][0] + ent.direction[0] ) % 2 , ( ent.passport[i][1] - ent.direction[1] ) % 2 
            toremove = []
        
        return toremove
    
    
class RegionMin():
    def __init__(self, name, mother):
        """ inicializa una region con su region madre"""
        self.mother = mother
        self.name = name
        self.content = []
        
    def draw(self, indent):
        space = ""
        for i in range(0,indent):
            space = space + "           "
        print space + self.name + " : " + "-".join([ent.name for ent in self.content])
    
    def update(self, lista):
        for ent in lista:
            ent.direction = (0,0)
            ent.backup = []
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
        self.passport = []
        self.backup = []
        self.direction = (0,0)
    
import pygame

if __name__ == '__main__':
    regMOM = Region(None)
    
    regA = Region(regMOM)
    regA00 = RegionMin("regA00",regA)
    regA10 = RegionMin("regA10",regA)
    regA01 = RegionMin("regA01",regA)
    regA11 = RegionMin("regA11",regA)
    regA.daugther = [[regA00,regA01],[regA10,regA11]]
    
    regB = Region(regMOM)
    regB00 = RegionMin("regB00",regB)
    regB10 = RegionMin("regB10",regB)
    regB01 = RegionMin("regB01",regB)
    regB11 = RegionMin("regB11",regB)
    regB.daugther = [[regB00,regB01],[regB10,regB11]]
    
    regC = Region(regMOM)
    regC00 = RegionMin("regC00",regC)
    regC10 = RegionMin("regC10",regC)
    regC01 = RegionMin("regC01",regC)
    regC11 = RegionMin("regC11",regC)
    regC.daugther = [[regC00,regC01],[regC10,regC11]]
    
    regD = Region(regMOM)
    regD00 = RegionMin("regD00",regD)
    regD10 = RegionMin("regD10",regD)
    regD01 = RegionMin("regD01",regD)
    regD11 = RegionMin("regD11",regD)
    regD.daugther = [[regD00,regD01],[regD10,regD11]]
    
    regMOM.daugther = [[regA,regB],[regC,regD]]
    
    
    carlos = entidadViajera("Carlos",8)    
    regB01.content.append(carlos)    
    
    pygame.init()
    
    screen = pygame.display.set_mode((100,100))
        
    doExit = False
    
    while not doExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                doExit = True
                
            teclas = pygame.key.get_pressed()
            
            if teclas[pygame.K_d]:
                carlos.direction = (0,1)
            if teclas[pygame.K_w]:
                carlos.direction = (-1,0)
            if teclas[pygame.K_a]:
                carlos.direction = (0,-1)
            if teclas[pygame.K_s]:
                carlos.direction = (1,0)
            if teclas[pygame.K_SPACE]:
                carlos.direction = (0,0)
    
        print "-".join([ent.name for ent in regMOM.update([])])        
        regMOM.draw(0)
        
        pygame.time.delay(500)
        
        screen.fill((255,255,255))
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
    
    

    