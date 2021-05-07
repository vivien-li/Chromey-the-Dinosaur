"""
NAME: Vivien Li
DATE: May 10th
DESCRIPTION: The sprites for my T-Rex game
"""
import pygame, random

class TRex(pygame.sprite.Sprite):
    """This is the T-Rex sprite, which represents the player"""
    def __init__(self, screen):
        """This is the the initializer method that takes the screen surface"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Define the image attributes for the paddle
        self.trexImages= [pygame.image.load("TRex/run1.png"), pygame.image.load("TRex/run2.png")]
        self.trexDuck = [pygame.image.load("TRex/duck.png"), pygame.image.load("TRex/duck2.png")]
        
        self.imageNum = 0
        #tracks which image should be displayed
        self.tracker = 0
        
        self.image = self.trexImages[self.imageNum]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = screen.get_height() - 58
        self.rect.left = 100
        self.speed = 0
        self.isJump = False
        self.window = screen
        self.duck = False
        
    def jump(self):
        """This is the method that is called when the player hits the up key to jump"""
        self.image = pygame.image.load("TRex/jump.png")
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.bottom == self.window.get_height() - 58:
            self.speed = -13
            self.isJump = True
            
    def ducking(self):
        """This is the method that will change the player image to a smaller version to duck"""
        self.image = pygame.image.load("TRex/duck.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = self.window.get_height() - 37
        self.duck = True
        
    def getDuckingState(self):
        """This will return the current state of the dinosaur"""
        return self.duck
        
    def revert(self):
        """This method will revert the state back to running image"""
        self.duck = False
        self.image = self.trexImages[self.imageNum]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = self.window.get_height() - 58
            
    def update(self):
        """This method is automatically called to reposition the player
        sprite on the screen."""
        if self.isJump == True:
            #if you're going down
            if self.speed > 0:
                if self.rect.bottom < self.window.get_height() - 58:
                    self.rect.top += self.speed
                    self.speed += 1
                else:
                    self.isJump == False
            else:
                self.rect.top += self.speed
                self.speed += 1
        #If you're touching the ground
        if self.rect.bottom == self.window.get_height() - 58:
            #If you're not ducking
            if self.duck == False:
                self.tracker += 1
                if self.tracker % 5 == 0:
                    self.imageNum = (self.imageNum + 1) % 2
                    self.image = self.trexImages[self.imageNum]
                    self.mask = pygame.mask.from_surface(self.image)
        #If you are ducking
        elif self.duck == True:
            self.tracker += 1
            if self.tracker % 5 == 0:
                self.imageNum = (self.imageNum + 1) % 2
                self.image = self.trexDuck[self.imageNum]
                self.mask = pygame.mask.from_surface(self.image)
        
        #If the tracker gets to 100, reset it to 1 (so the number doesn't get crazy big)
        if self.tracker == 100:
            self.tracker == 1


class Endzone(pygame.sprite.Sprite):
    """This class defines the sprite for our endzones"""
    def __init__(self, screen, kind):

        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #1 means horizontal endzone for trex, 2 is vertical for obstacles
        if kind == 1:
            # Our endzone sprite will be a 1 pixel wide black line.
            self.image = pygame.Surface((screen.get_width(), 1))
            self.image = self.image.convert()
            self.image.fill((0, 0, 0))
                 
            # Set the rect attributes for the endzone
            self.rect = self.image.get_rect()
            self.rect.bottom = screen.get_height() - 58
        else:
            #This endzone is a rectangle 90 pixels wide
            self.image = pygame.Surface((90, screen.get_height()))
            self.image = self.image.convert()
            self.image.fill((255, 0, 0))
                 
            # Set the rect attributes for the endzone
            self.rect = self.image.get_rect()
            self.rect.left = screen.get_width() - 90          
        
class Background(pygame.sprite.Sprite):
    """This class defines the endless background sprite"""
    def __init__(self, screen):
        '''This initializer will create the endless background'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("Background/goodbackground.png")
        self.rect= self.image.get_rect()
        self.window = screen
        self.speed = 5
    def update(self):
        """Called automatically during Refresh to update sprite's position"""
        #move 1 pixel to the left each time
        self.rect.left -= self.speed
        
        #what happens if there's no more image
        if self.rect.right <= self.window.get_width():
            self.rect.left = 0

class Bullet(pygame.sprite.Sprite):
    """This class defines the bullet sprite"""
    def __init__(self, screen):
        """This is the intializer that will create the bullet sprite"""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)     
        
        self.image = pygame.image.load("OtherSprites/bullet.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = 140
        self.rect.bottom = screen.get_height() - 85
    def update(self):
        """This is the special update method called every time to update sprite position"""
        self.rect.left += 5
        
class Obstacle(pygame.sprite.Sprite):
    """This class defines the obstacles sprite"""
    def __init__(self, screen, num):
        """This is the intializer that will create the bullet sprite
        0 = fire 1 = dino 2 = bird"""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)     
        
        self.imageNum = 0
        self.tracker = 0
        self.birdSpeed = 6
        self.kind = num
        self.birds = [pygame.image.load("FlappyBird/bird0.png"), pygame.image.load("FlappyBird/bird1.png")]
        
        #If it's the fire
        if self.kind == 0:
            self.image = pygame.image.load("OtherSprites/flame.png")
            self.rect = self.image.get_rect()
            self.rect.bottom = screen.get_height() - 58
            self.mask = pygame.mask.from_surface(self.image)
        #If it's the rock    
        elif self.kind == 1:
            self.image = pygame.image.load("OtherSprites/rock.png")
            self.rect = self.image.get_rect()
            self.rect.bottom = screen.get_height() - 40
            self.mask = pygame.mask.from_surface(self.image)
        #If it's the bird
        else:
            self.image = self.birds[self.imageNum]
            self.rect = self.image.get_rect()
            self.rect.bottom = screen.get_height() - 90
            self.mask = pygame.mask.from_surface(self.image)
    
        self.rect.left = screen.get_width()
    def getType(self):
        """This method will return the type of obstacle it is (0-2)"""
        return self.kind
        
    def update(self):
        """This is the special update method called everytime upon refreshing"""
        if self.kind == 2:
            self.tracker += 1
            if self.tracker % 5 == 0:
                self.imageNum = (self.imageNum + 1) % 2
                self.image = self.birds[self.imageNum]
            self.rect.left -= 6
        else:
            self.rect.left -= 5
        if self.tracker == 100:
            self.tracker == 1
        
class Scorekeeper(pygame.sprite.Sprite):
    """This class defines scorekeeper sprite"""
    def __init__(self, screen):
        """This initializer will load the custom font Santana-Bold and sets one variable to keep score the player"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Load font, set lives and score
        self.font = pygame.font.Font("Santana-Bold.ttf", 45)
        self.score = 0
        self.screen = screen
        
    def setScore(self):
        """This method will add one to the score"""
        self.score += 1
        
    def getScore(self):
        """This method will return the current score"""
        return self.score
    
    def update(self):
        """This is the updating method called every time the screen refreshes"""
        message = "SCORE: " + str(self.score)
        self.image = self.font.render(message, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen.get_width() - 120, 45)
