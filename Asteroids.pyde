#add_library('sound')
    # Add animation for player
    # Add aliens
    # Add Spawn and commands
    #
    
def randomChoice(ls) :
    l = len(ls)
    choice = int(random(0,l))
    return ls[choice]
 
class Laser :

    def __init__(self, X, Y):
        self.x = X
        self.y = Y
        self.speed = 19
        self.angle = PI/2.0
        self.lifespan = 575
        self.alive = False
        self.FireTime = -100000000
        self.xSpeed = 0
        self.ySpeed = 0
       
        
    def fire(self, X, Y, shipAngle) :
        self.x = X
        self.y = Y
        self.angle = shipAngle
        self.alive = True
        self.FireTime = millis()
        #global laserSound
        #laserSound.play()
       
        
        
    def draw(self) :
        fill(255,255,255)
        ellipse(self.x,self.y,2,2)
       
    def move(self) :
       
        if self.x < 0:
            self.x = width
        if self.x > width :
            self.x = 0
           
        if self.y < 0:
            self.y = height
           
        if self.y > height :
            self.y = 0
       
        self.ySpeed = self.speed * sin(self.angle - PI/2)
        self.xSpeed = self.speed * cos(self.angle - PI/2)
       
        self.y = self.y + self.ySpeed
        self.x = self.x + self.xSpeed
       
 
        if millis() > self.FireTime + self.lifespan :
            self.alive = False
       
                
 
class Spaceship :
    def __init__(self, X, Y):
            self.x = X
            self.y = Y
            self.w = 20
            self.h = 35
            self.cp1x = self.x - self.w
            self.cp2x = self.x + self.w
            self.cp3x = self.x
            self.cp1y = self.y + self.h
            self.cp2y = self.y + self.h
            self.cp3y = self.y + self.h/2
            self.speed = 0
            self.maxSpeed = 13
            self.speedIncrease = 0.2
            self.coastValue = 0.05
            self.angle = PI/2.0
            self.momentumAngle = 0
            self.rotationSpeed = 0.09
            self.xSpeed = 0
            self.ySpeed = 0
            self.alive = False
            self.lives = 3
            self.spawnX = [width/2, 1075, 1075, 250, 250]
            self.spawnY = [400, 262, 525, 525, 262]
            self.engineFlicker = 0
            

        #laser stuff
            self.lasers = []
            self.totalLaserNum = 5
            self.lastShotFrame = 0
            
            self.lasers.append( Laser(self.x,self.y) )
            self.lasers.append( Laser(self.x,self.y) )
            self.lasers.append( Laser(self.x,self.y) )
            self.lasers.append( Laser(self.x,self.y) )
            self.lasers.append( Laser(self.x,self.y) )
            self.lasers.append( Laser(self.x,self.y) )
            
    
    
    def draw(self) :
        if self.alive :
            stroke(255,255,255)
            pushMatrix()
            translate(self.x,self.y)
            rotate(self.angle)
            #line(0,1000,0,-1000)
            #line(1000,0,-1000,0)
            
            line(0 , -self.h/2 , 0 - self.w, -self.h/2 + self.h)
            line(0 , -self.h/2 , 0 + self.w, -self.h/2 + self.h)
            line(0 - self.w, -self.h/2 + self.h, 0 , -self.h/2 + self.h / 2)
            line(0 + self.w, -self.h/2 + self.h, 0 , -self.h/2 + self.h / 2)
            
            if self.engineFlicker < 4 :
                self.engineFlicker += 1
            else :
                self.engineFlicker = 0

            if wPressed and self.engineFlicker == 0:
                line(-self.w/2,self.h/4,0,self.h/1.5)
                line(self.w/2,self.h/4,0,self.h/1.5)
       
            popMatrix()
           
            fill(0,255,0)
            #ellipse(self.x,self.y,3,3)
            #ellipse(self.cp1x,self.cp1y,3,3)
            #ellipse(self.cp2x,self.cp2y,3,3)
            #ellipse(self.cp3x,self.cp3y,3,3)
            for laser in self.lasers :
                if laser.alive :
                    laser.draw()
       
        
        
        
        
    def move(self):
        if self.alive :
            global wPressed
            global aPressed
            global sPressed
            global dPressed
            global spacePressed
    
            if self.x < 0:
                self.x = width
            if self.x > width :
                self.x = 0
            
            if self.y < 0:
                self.y = height
            if self.y > height :
                self.y = 0
        
            self.cp1x = self.x - self.w
            self.cp2x = self.x + self.w
            self.cp3x = self.x
            self.cp1y = self.y + self.h
            self.cp2y = self.y + self.h
            self.cp3y = self.y + self.h/2
        
        
            if wPressed :
                if abs(self.momentumAngle - self.angle) > PI/3.0 :
                    self.speed = 0
                self.momentumAngle = self.angle
                if abs(self.speed) < self.maxSpeed :
                    self.speed += self.speedIncrease
            
            if aPressed :
                self.angle = self.angle - self.rotationSpeed
            
            if dPressed :
                self.angle = self.angle + self.rotationSpeed
            
            if spacePressed :
                if frameCount > self.lastShotFrame + 15 :
                    for laser in self.lasers: 
                        if not laser.alive :
                            laser.fire(self.x, self.y, self.angle)
                            self.lastShotFrame = frameCount
                            break
            
            
            
            for laser in self.lasers :
                if laser.alive :
                    laser.move()
                
            if self.speed != 0 :
                if self.speed > 0:
                    self.speed -= self.coastValue
                else :
                    self.speed += self.coastValue
                
            self.ySpeed = self.speed * sin(self.momentumAngle - PI/2)
            self.xSpeed = self.speed * cos(self.momentumAngle - PI/2)
            
            self.y = self.y + self.ySpeed
            self.x = self.x + self.xSpeed
            
            
     

            
            
class Asteroid :
   
    def __init__(self, X, Y, s, a):
          self.x = X
          self.y = Y
          self.r = 0
          self.size = s
          self.speed = 3/self.size
          self.speedIncrease = 0.2
          self.coastValue = 0.00001
          self.angle = a
          self.momentumAngle = self.angle
          self.rotationSpeed = random(-0.03,0.03)
         
    def draw(self):
        fill(255,255,255,0)
        stroke(255,0,0)
        #ellipse(self.x,self.y,self.r * 2, self.r * 2)
        fill(255,0,0)
        #text(self.size,self.x,self.y)
        stroke(255)
        
        pushMatrix()
        translate(self.x,self.y)
        rotate(self.angle)
        
        if self.size == 3 :
            line(0+40,0-44,0+60,0)        
            line(0+60,0,0+48,0+35)
            line(0+48,0+35,0+15,0+23)
            line(0+15,0+23,0+10,0+60)
            line(0+10,0+60,0-40,0+45)
            line(0-40,0+45,0-60,0)
            line(0-60,0,0-9,0-60)
            line(0-9,0-60,0+40,0-44)
            
        if self.size == 2 :
            line(0+0, 0+40,0+30, 0+25)
            line(0+30,0+25,0+40,0+0)
            line(0+40,0+0,0+15,0-5)
            line(0+15,0-5,0+35,0-20)
            line(0+35,0-20,0+0,0-40)
            line(0+0,0-40,0-35,0-20)
            line(0-35,0-20,0-35,0+20)
            line(0-35,0+20,0+0,0+40)
        
            
        if self.size == 1 :
            line(0+0, 0+20,0+17, 0+10)
            line(0+17,0+10,0+15,0-15)
            line(0+15,0-15,0+0,0-20)
            line(0+0,0-20,0-5,0-5)
            line(0-5,0-5,0-20,0+0)
            line(0-20,0+0,0-15,0+15)
            line(0-15,0+15,0+0,0+20)
            
        popMatrix()
            
            
            
            
            
        
        
        
        #line(200,200,235,220)
        #line(200,200,235,180)
        #line(235,220,260,200)
        #line(235,180,200,165)
        #line(200,165,235,150)
        #line(235,150,260,160)
        #line(260,160,270,180)
        #line(270,180,260,200)
        # Draw lines for the asteroid visuals here

    def move(self):
        if self.size == 3 :
            self.r = 60
        if self.size == 2 :
            self.r = 40
        if self.size == 1 :
            self.r = 20 
        #Movement outside screen
        if self.x < 0:
            self.x = width
        if self.x > width :
            self.x = 0
    
        if self.y < 0:
            self.y = height
        if self.y > height :
            self.y = 0
        #Move
        
        self.angle += self.rotationSpeed
        
        if self.speed != 0 :
            if self.speed > 0:
                self.speed -= self.coastValue
            else :
                self.speed += self.coastValue
            
        self.ySpeed = self.speed * sin(self.momentumAngle - PI/2)
        self.xSpeed = self.speed * cos(self.momentumAngle - PI/2)
        
        self.y = self.y + self.ySpeed
        self.x = self.x + self.xSpeed

 
       
    def isPointInBox(self, dotX, dotY) :
        a = self.x - dotX
        b = self.y - dotY
        c = sqrt(a*a + b*b)
        #print("a:" + str(a))
        #print("b:" + str(b))
        #print("c:" + str(c))
        #print("r:" + str(self.r))
       
        if c <= self.r :
            return True
        else :
            return False
        
        

            
#####################################################
 
global currentLevel
global allDestroyedTime
global lastAstLen
           
global player

global extraLifeScore

global asteroids


global wPressed
global aPressed
global sPressed
global dPressed
global spacePressed

global deathFrame

global score

global looping

#global laserSound
#global astExpSound

def increaseLevel():
    global allDestroyedTime
    allDestroyedTime = -10000
    global currentLevel
    currentLevel += 1
    for i in range(0,currentLevel) :
        
        astX = 0 
        astY = 0
        
        line = randomChoice(["w","h"])
        
        if line == "w" :
            astY = randomChoice([0,height])
            astX = random(0,width)
        else :
            astX = randomChoice([0,width])
            astY = random(0,height)
        
        asteroids.append( Asteroid(astX,astY,3,random(0,2*PI) ) )  
      
    #Stationary Asteroid for Debugging  
    #a = Asteroid(width/2height/2,3,random(0,2*PI))
    #a.speed = 0
    #asteroids.append(a)
    
    #b = Asteroid(1075,262,3,random(0,2*PI))
    #b.speed = 0
    #asteroids.append(b)
    
    #c = Asteroid(1075,525,3,random(0,2*PI))
    #c.speed = 0
    #asteroids.append(c)
    
    #d = Asteroid(250,525,3,random(0,2*PI))
    #d.speed = 0
    #asteroids.append(d)
    
    #e = Asteroid(250,262,3,random(0,2*PI))
    #e.speed = 0
    #asteroids.append(e)
                 
    



def killAsteroid(i) :
    parentX = asteroids[i].x
    parentY = asteroids[i].y
    parentS = asteroids[i].size
    parentA = asteroids[i].angle
    
    asteroids.pop(i)
    if parentS > 1 :
        asteroids.append( Asteroid(parentX,parentY,parentS -1, parentA + random(-PI/2,PI/2) ) )  
        asteroids.append( Asteroid(parentX,parentY,parentS -1, parentA + random(-PI/2,PI/2) ) ) 
        
    #global astExpSound
    #astExpSound.play()
    
 
def setup() :
    global currentLevel
    global allDestroyedTime
    global lastAstLen
    global player
    global extraLifeScore
    global asteroids
    global wPressed
    global aPressed
    global sPressed
    global dPressed
    global spacePressed
    global deathFrame
    global score
    global looping
    #global laserSound
    #global astExpSound
    
    currentLevel = 3
    allDestroyedTime = -100000
    lastAstLen = 0
            
    player = Spaceship(width/2,height/2)
    
    extraLifeScore = 10000
    
    asteroids = []
    
    wPressed = False
    aPressed = False
    sPressed = False
    dPressed = False
    spacePressed = False
    
    deathFrame = -200
    score = 0
    looping = True
    
    #laserSound = SoundFile(this, "Laser.aiff")
    #astExpSound = SoundFile(this,"AsteroidsExplosion.wav")
    
    
    
    noCursor()
    fullScreen()
    increaseLevel()
    
def draw():
    background(0,0,0)   
    #IMPORTANT
    player.move()
    
    global deathFrame
    global score
    global extraLifeScore

    for i in range(0,len(asteroids)) :
        asteroidHit = False
        for laser in player.lasers :
            if laser.alive and asteroids[i].isPointInBox(laser.x,laser.y) :
                laser.alive = False
                if asteroids[i].size == 1 :
                    score += 100
                if asteroids[i].size == 2 :
                    score += 50
                if asteroids[i].size == 3 :
                    score += 25
                
                killAsteroid(i)
                asteroidHit = True
                break
        if asteroidHit : break
        if player.alive and ( asteroids[i].isPointInBox(player.x,player.y) or asteroids[i].isPointInBox(player.cp1x,player.cp1y) or asteroids[i].isPointInBox(player.cp2x,player.cp2y) or asteroids[i].isPointInBox(player.cp3x,player.cp3y) ):
            player.alive = False
            player.lives -= 1
            deathFrame = frameCount
            killAsteroid(i)
            break

    if score > extraLifeScore :
        player.lives += 1
        extraLifeScore += 10000

    #Respawn
    if not player.alive and player.lives > 0 and frameCount > deathFrame + 200 :
        for i in range(0,len(player.spawnX)) :
            find = False
            for a in asteroids :
                if a.isPointInBox(player.spawnX[i],player.spawnY[i]) :
                    find = True
                    break
            if find == False :
                player.x = player.spawnX[i]
                player.y = player.spawnY[i]
                break
                    
        player.angle = PI/2.0
        player.speed = 0
        player.alive = True
       
    #IMPORTANT
    for a in asteroids :
        a.move()
        a.draw()
    player.draw()
    fill(255,255,255)
    textSize(12)
    text("FPS : " + str(round(frameRate,3)),100,105)
    textSize(18)
    text("Lives : " + str(player.lives),100,140)
    text("Level : " + str(currentLevel-3),width-100,140)
    text("Score : " + str(score),width/2,75)
    
    
    
    
    global allDestroyedTime
    global lastAstLen
    
    if len(asteroids) == 0 and lastAstLen != len(asteroids) :
        allDestroyedTime = millis()
        
    if millis() > allDestroyedTime + 3000 and allDestroyedTime > 0 :
        increaseLevel()
    
    lastAstLen = len(asteroids)
    
    if player.lives == 0 :
        textSize(48)
        text("Game Over",width/2-100,height/2)     
   
   
def keyPressed() :
    global wPressed
    global aPressed
    global sPressed
    global dPressed
    global spacePressed
    global looping
    
    #print "HIT " + key
    if key == "w" or key == "W" :
        wPressed = True
    if key == "a" or key == "A" :
        aPressed = True
    if key == "s" or key == "S" :
        sPressed = True
    if key == "d" or key == "D" :
        dPressed = True
    if key == "p" or key == "P" :
         if (looping) :
            noLoop()
            looping = False
            text("Paused",width/2,height/2)
         else : 
             loop() 
             looping = True
    if key == "R" :
        setup()
    
     
    if key == CODED :
        if keyCode == UP : 
            wPressed = True
        if keyCode == LEFT :
            aPressed = True
        if keyCode == DOWN :
            sPressed = True
        if keyCode == RIGHT :
            dPressed = True    
        
    if key == " " :
        spacePressed = True            

def keyReleased() :
    global wPressed
    global aPressed
    global sPressed
    global dPressed
    global spacePressed
    
    #print "RELEASE " + key
    if key == "w" or key == "W" :
        wPressed = False
    if key == "a" or key == "A" :
        aPressed = False
    if key == "s" or key == "S" :
        sPressed = False
    if key == "d" or key == "D" :
        dPressed = False
        
    if key == CODED :
        if keyCode == UP : 
            wPressed = False
        if keyCode == LEFT :
            aPressed = False
        if keyCode == DOWN :
            sPressed = False
        if keyCode == RIGHT :
            dPressed = False 
    
    if key == " " :
        spacePressed = False           

            

    
