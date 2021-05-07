"""
NAME: VIVIEN LI
DATE: MAY 28 2019
DESCRIPTION: WELCOME TO CHROMEY THE T-REX GAME! IN THIS GAME YOU ARE ABLE TO
SHOOT ROCKS, DUCK FROM BIRDS, AND JUMP OVER FLAMES! IT IS AN ENDLESS GAME, 
MEANING YOUR GOAL IS TO GET AS FAR AS POSSIBLE. THERE IS A HIGHSCORE KEEPER 
THAT KEEPS TRACK OF THE HIGHEST SCORE BUT RESETS EVERY TIME YOU EXIT THE
APPLICATION
"""
# I - Import and Initialize
import pygame, gameSprites, random
pygame.init()
pygame.mixer.init()

def startingScreen(score):
    """This is the starting screen function which is called upon before a player
    starts the game. It takes in a score number which represents the highest
    score obtained so far. It also returns keepGoing which will tell Python what
    to do (start game or quit game)"""
    # D - Display configuration
    screen = pygame.display.set_mode((640, 361))
    pygame.display.set_caption("Chromey the T-Rex")
 
    # E - Entities
    background = pygame.image.load("Background/StartingScreen.jpg")
    background = background.convert()
    #HIGHSCORE
    myCustomFont = pygame.font.Font("Santana-Bold.ttf", 30)
    highScore = myCustomFont.render("HIGHSCORE: " + str(score), True, (0, 0, 0))
    #MUSIC
    """background music, file was too loud to upload onto github"""
    #pygame.mixer.music.load("Sound/background.mp3")
    #pygame.mixer.music.set_volume(0.3)
    #pygame.mixer.music.play(-1)    
    
    # A - ACTION (broken down into ALTER steps)
    # A - Assign
    clock = pygame.time.Clock()
    startGoing = True
    keepGoing = True
    #L - LOOP!
    while startGoing:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                return keepGoing
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    keepGoing = True
                    pygame.mixer.music.fadeout(1000)
                    pygame.time.delay(1000)
                    return keepGoing
        screen.blit(background, (0, 0))
        screen.blit(highScore, (screen.get_width() - 220, 10))
        pygame.display.flip()        

def gameLoop(): 
    """This is the game loop function which is called when the player is ready
    to play the game. It contains the whole game portion! It returns the current
    score when player dies to see if it's beaten the current highscore"""
    
    # D - Display configuration
    screen = pygame.display.set_mode((640, 361))
    pygame.display.set_caption("Chromey the T-Rex")
 
    # E - Entities
    background = pygame.image.load("Background/StartingScreen.jpg")
    background = background.convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    gameOver = pygame.image.load("Background/gameover.png")
    gameOver.convert()

    #MUSIC/SOUND EFFECTS 
    #pygame.mixer.music.load("Sound/background.mp3")
    #pygame.mixer.music.set_volume(0.3)
    #pygame.mixer.music.play(-1)
    
    boom = pygame.mixer.Sound("Sound/bullet.wav")
    oof = pygame.mixer.Sound("Sound/oof.ogg")
    hop = pygame.mixer.Sound("Sound/hop.wav")
    
    #SPRITES
    endless = gameSprites.Background(screen)
    player = gameSprites.TRex(screen)
    endZone = gameSprites.Endzone(screen, 1)
    endZone2 = gameSprites.Endzone(screen, 2)
    bullets = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    scorekeeper = gameSprites.Scorekeeper(screen)
    allSprites = pygame.sprite.OrderedUpdates(endZone, endZone2, endless, scorekeeper, bullets, obstacles, player)  
    
    # A - Action (broken into ALTER steps)
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    startGoing = True
    keepGoing = True
    ready = True
    lastType = -1
    lost = False
                
        # L - Loop
    while keepGoing:
     
        # T - Timer to set frame rate
        clock.tick(60)
     
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if player.rect.colliderect(endZone):
                        if player.getDuckingState() == True:
                            player.rect.bottom = screen.get_height() - 57
                            player.revert()
                        player.jump()
                        hop.play()
                elif event.key == pygame.K_DOWN:
                    if player.rect.colliderect(endZone): 
                        player.ducking()
                elif event.key == pygame.K_SPACE:
                    if player.rect.colliderect(endZone) and len(bullets) < 3:
                        player.revert()
                        bullet = gameSprites.Bullet(screen)
                        bullets.add(bullet)
                        allSprites = pygame.sprite.OrderedUpdates(endZone, endZone2, endless, scorekeeper, bullets, obstacles, player)  
            #If keys are released            
            elif event.type == pygame.KEYUP:
                if player.rect.colliderect(endZone):
                        player.revert()
                        
        #If ready to spawn a new obstacle:     
        if ready:
            if random.randrange(30) == 7:
                kind = random.randrange(3)
                if lastType == 0 and kind == 2:
                    kind = random.randrange(2)
                newObstacle = gameSprites.Obstacle(screen, kind)
                lastType = newObstacle.getType()
                obstacles.add(newObstacle)
                allSprites = pygame.sprite.OrderedUpdates(endZone, endZone2, endless, scorekeeper, bullets, obstacles, player)  
                ready = False
        #If there are no obstacles
        elif len(obstacles) == 0:
            ready = True
                
        #if not ready to spawn, but no obstacle in endzone
        else:
            for obstacle in obstacles:
                if obstacle.rect.colliderect(endZone2):
                    ready = False
                    break
                else:
                    ready = True
                
        #Collision with bullet x rock
        for obstacle in obstacles:
            if obstacle.getType() == 1:
                for bullet in bullets:
                    if obstacle.rect.colliderect(bullet.rect):
                        obstacle.kill()
                        bullet.kill()
                        scorekeeper.setScore()
                        boom.play()
                        
        #Killing obstacles if it reaches end of screen
        for obstacles_here in obstacles:
            if obstacles_here.rect.right <= 0:
                obstacles_here.kill()
                scorekeeper.setScore()
                
        #Killing bullets if it reachs end of screen      
        for bullets_shot in bullets:
            if bullets_shot.rect.left == screen.get_width():
                bullets_shot.kill()
             
        #Dinosaur x obstacle collision     
        obstacles_hit = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_mask)
        if obstacles_hit:
            for obstacles_present in obstacles:
                if obstacles_present.rect.colliderect(player):
                    keepGoing = False
                    lost = True
                    oof.play()
  
        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
     
    # If the player loses, display game over sign + 3 second delay + fadeout
    if lost:
        screen.blit(gameOver, (30,125))
        pygame.display.flip()
        pygame.mixer.music.fadeout(3000)
        pygame.time.delay(3000)
    return scorekeeper.getScore()
    
def main():   
    """This function defines the 'mainline logic' for my t-rex game."""
    playGame = True
    highScore = 0
    while playGame:
        playGame = startingScreen(highScore)
        if playGame:
            score = gameLoop()
            highScore = max(score, highScore)
    pygame.quit()
        
main()