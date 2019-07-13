import pygame
from pygame.locals import *
import sys
import serial
import random
import time

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

music = pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)

#Game setting 
class CORLOR:
    def __init__(self): #background black, cell purple, next cell green, player yellow
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.RED = (255, 0, 0)
        self.BLUE = (143, 143, 143)
        self.GREEN = (0, 255, 0)
        self.PURPlE = (140,0,255)
        self.YELLOW = (255,251,0)


#The player 
class People(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor
        self.image = Point((0,0),(12,12),[1,1,23,23]) #pid, pos, rect
        self.rect= self.image.rect 
        self.rect.top=0
        self.rect.left=0
        self.corlor = Color(255, 251, 0)
        self.pid = [0,0]
        self.life = 3
    
    #movement 
    def move_left(self):
        if self.rect.left > 0:
            self.pid[0] -= 1
            self.rect.left -= 24
    
    def move_up(self):
        if self.rect.top > 0:
            self.pid[1] -= 1
            self.rect.top -= 24
    
    def move_down(self):
        if self.rect.top != 552 + 24:
            self.pid[1] += 1
            self.rect.top += 24
    
    def move_right(self):
        if self.rect.left != 720-24:
            self.pid[0] += 1
            self.rect.left += 24
        


    #restart
    def restart(self):
        self.pid = [0,0]
        self.rect.top = 0
        self.rect.left = 0

#the point 
class Point:
    def __init__(self,pid,pos,rect):
        self.pid = pid
        self.pos = pos
        self.rect = Rect(rect)
        self.state = 0

class Life_game:
    def __init__(self):
        self.point = self.map_maker()  # generating the map
        self.life_time = 3    # speed of reproduction
    
    # calculating the number of alive cells around
    def get_around_point_state(self,current_point):
        x_index = current_point[0] #x position of current point
        y_index = current_point[1]
        
        top_side_point_1 = self.get_point([x_index - 1 ,y_index - 1]) #top-left
        top_side_point_2 = self.get_point([x_index     ,y_index - 1]) #top
        top_side_point_3 = self.get_point([x_index + 1 ,y_index - 1]) #top-right
        left_side_point  = self.get_point([x_index - 1 ,y_index    ]) #left
        right_side_point = self.get_point([x_index + 1 ,y_index    ]) #right
        bottom_side_point_1 = self.get_point([x_index - 1 ,y_index + 1]) #bottom-left
        bottom_side_point_2 = self.get_point([x_index     ,y_index + 1]) #bottom
        bottom_side_point_3 = self.get_point([x_index + 1 ,y_index + 1]) #bottom-right
        
        alive_count = 0
        for point in [top_side_point_1,top_side_point_2,top_side_point_3,left_side_point,right_side_point,bottom_side_point_1,bottom_side_point_2,bottom_side_point_3]:
            if point:
                if point.state == 1: #alive
                    alive_count += 1
        return alive_count #number of alive cells

    # generating map 
    def map_maker(self):
        pos = []
        x = 12
        y = 12
        rect_x = 0
        rect_y = 0
        for i in range(30):#columns
            temp_pos = []
            for j in range(25): #rows
                temp_pos.append(Point([i,j],[x,y],[rect_x + 1,rect_y + 1,23,23]))
                rect_y += 24
                x += 12
            x = 12
            rect_y = 0
            y += 12
            rect_x += 24
            pos.append(temp_pos)
        return pos

    # set random point
    def random_point(self,current_pos,number = 5): 
        new_x_list = []
        for i in range(30):
            if i != current_pos[0] and i != 29:
                new_x_list.append(i)
        new_y_list = []
        for i in range(25):
            if i != current_pos[1] and i != 24:
                new_y_list.append(i)
        
        # if the current position already have point, change another one 
        count = 0
        while count < number:
            while True:
                x = random.choice(new_x_list)
                y = random.choice(new_y_list)
                if self.point[x][y].state == 1:
                    pass
                else:
                    self.point[x][y].state = 1
                    count += 1
                    break
    
    # getting the point
    def get_point(self,index_list):
        # if outside the map, return None
        try:
            if -1 in index_list:
                return None
            return self.point[index_list[0]][index_list[1]]
        except BaseException as e:
            return None
    # update point state, 1 = alive 
    def update_point(self,index_list):
        if self.point[index_list[0]][index_list[1]].state == 1:
            print("current point has been alive")
        else:
            self.point[index_list[0]][index_list[1]].state = 1
    # running an iteration of the game of life
    def life_loop(self):
        should_change_point = self.get_need_change_point()
        self.set_change_point(should_change_point)
    # getting the points that need to be changed 
    def get_need_change_point(self):
        should_change_point = []
        for line in self.point:
            for point in line:
                around_alive = self.get_around_point_state(point.pid)
                if around_alive == 3:
                    should_change_point.append((point,3,point.state))
                elif around_alive == 2:
                    pass
                else:
                    should_change_point.append((point,0))
        return should_change_point
    # setting the state of the changed points
    def set_change_point(self,point_list):
        should_change_point = point_list
        for point in should_change_point:
            if point[1] == 3:
                point[0].state = 1
            else:
                if point[1] == 0:        
                    point[0].state = 0

    # restart
    def restart(self):
        for line in self.point:
            for point in line:
                point.state = 0

# Change the coordinates to index format so that you can see which rectangle range is clicked
def click_point_change(pos):
    right_x_index = 0
    right_y_index = 0
    if pos[0] <= 24:
        right_x_index = 0
    else:
        right_x_index = (pos[0] // 24)
    if pos[1] <= 24:
        right_y_index = 0
    else:
        right_y_index = (pos[1] // 24)
    return [right_x_index,right_y_index]
    
def is_over(point):
    if point.pid == [29,24]: #win
        return True
    else:
        return False

width = 720   
height = 600  
size = width, height
pygame.init() 
screen = pygame.display.set_mode(size) 
game_corlor = CORLOR() 
life_game = Life_game() 
clock = pygame.time.Clock()
people = People()
life_time = 0
should_change_point = []
key_press_time = 0
bling_time = 0
bling_show = True
should_change_point = life_game.get_need_change_point()

#PySerial 
ser = serial.Serial(port='/dev/cu.usbmodem14301', baudrate=9600)
time.sleep(3) 
print('Ready')


#new points are generated if the player has not moved for more than twice iteration.
#Prevent players from simply waiting for life games to stabilize before moving
random_point_num = 10    # punishment
life_game.life_time = life_game.life_time   # iteration speed
setp_random_point = 5     # generate points when moving 

def hit_check(point):   #collision 
    if life_game.get_point(point.pid).state == 1:# if the position of the player has alive cell 
        if people.life <=0 and run == True: # if no life 
            print(people.life)
            return True
        if people.life >0: #if still have life 
            people.life -= 1
            people.move_right() #prevent counting the position too fast, so automatcaly jump to the next cell  
            #print(people.life)
            return False
    else:
        print(people.life)
        return False


def set_init_random():    # setting the random points in the begining 
    start_around = []
    for i in range(3):
        for j in range(3):
            start_around.append([i,j])
    end_around = []
    for i in range(3):
        for j in range(3):
            end_around.append([29 - i, 24 -j]) 
    for i in life_game.point:
        for point in i:
            if random.randint(1,3) == 1 and point.pid not in (start_around + end_around):
                # the points won't in the 3x3 range of starting point and ending point
                point.state = 1


# Cursor 
class Curor:
    def __init__(self):
        self.rect = Rect(110,110,20,20)  # position of the cursor
        self.current_choose = 0   # current choose 
        self.is_run = False   # if is run, should have 4 selections, if not, 5 selections  

    def move_up(self):  # moving up
        if self.current_choose - 1 == -1:
            self.current_choose = 2
            self.rect.top = 210
        else:
            self.current_choose -= 1
            self.rect.top -= 50
    
    def move_down(self): # moving down
        if self.is_run:
            select_num = 5
        else:
            select_num = 4
        if self.current_choose + 1 == select_num:
            self.current_choose = 0
            self.rect.top = 110
        else:
            self.current_choose += 1
            self.rect.top += 50

top_title = "HUMAN + MACHINE"   

run = False  
curor = Curor() 
print('START')
        
while True:
    for event in pygame.event.get():   
        if event.type == QUIT: 
            sys.exit()

    if run == False:  # If game is not running
        joystick=100
        if ser.in_waiting:
            joystick = int(ser.readline())
        #print(joystick)
        if joystick == 20:
            curor.move_up()
        if joystick == 25:
            curor.move_down()
        if joystick == 0:
            choose = curor.current_choose  # getting current status
            if choose == 3:  # could be "quit" or "continue" 
                if top_title == "stop":  # continue
                    run = True
                    curor.current_choose = 0
                    curor.rect.top = 110
                else:  # either stop or quit
                    sys.exit()
            else:
                if choose == 0:  # easy mode
                    people.life = 3
                    random_point_num = 15
                    life_game.life_time = 2
                    setp_random_point = 8
                elif choose == 1:  # mid mode
                    people.life = 3
                    random_point_num = 20
                    life_game.life_time = 1
                    setp_random_point = 10
                elif choose == 2:  # hard mode
                    people.life = 3
                    random_point_num = 40
                    life_game.life_time = 0.4
                    setp_random_point = 20
                elif choose == 4:  # quit
                    sys.exit()
                life_game.restart()  
                people.restart()  
                set_init_random()  
                curor.current_choose = 0  
                curor.rect.top = 110
                run = True  # game start!

    else:  # the game is running
        joystick = 100
        if ser.in_waiting:
            joystick = int(ser.readline())
        #if joystick == 0:
            #life_game.life_loop()  # press the joystick can have another iteration 
        if joystick == 20:  # move up
            key_press_time = 0  # setting the pressed time, for the punishment 
            life_game.random_point(people.pid, setp_random_point)  # random points
            people.move_up()  
        if joystick == 25:  # move down
            key_press_time = 0
            life_game.random_point(people.pid, setp_random_point)
            people.move_down()
        if joystick == 10:  # move left
            key_press_time = 0
            life_game.random_point(people.pid, setp_random_point)
            people.move_left()
        if joystick == 15:  # move right
            key_press_time = 0
            life_game.random_point(people.pid, setp_random_point)
            people.move_right()
        if joystick == 0:  # stop the game
            run = False
            top_title = "stop"

        #sending the number of life to arduino
        if people.life == 3: 
            ser.write(b'3')
        if people.life == 2:
            ser.write(b'2')
        if people.life == 1:
            ser.write(b'1')
        if people.life == 0:
            ser.write(b'0')
            
    display_window = pygame.Surface((400,400))   # menu
    display_window.fill((255,255,255))
    font1 = pygame.font.SysFont('Time', 30)
    font2 = pygame.font.SysFont('Time', 25)
    title_ = font1.render(top_title,True,(0,0,0))
    easy_ = font2.render("easy mode",True,(0,0,0))
    mid_ = font2.render("mid mode",True,(0,0,0))
    hard_ = font2.render("hard mode",True,(0,0,0))
    continue_ = font2.render("continue",True,(0,0,0))
    quit_ = font2.render("QUIT",True,(0,0,0))
    display_window.blit(title_,(170,40))
    display_window.blit(easy_,(150,110))
    display_window.blit(mid_,(150,160))
    display_window.blit(hard_,(150,210))


    dimg=[pygame.image.load("img/d"+str(i+1)+".jpg") for i in range(13)] 
    mimg=[pygame.image.load("imgmoon/m"+str(i+1)+".jpg") for i in range(38)] 
    gimg=[pygame.image.load("img/g"+str(i+1)+".jpg") for i in range(4)] 

    if top_title == "stop":       # logic of the menu, the number of the selections
        display_window.blit(continue_,(150,260))
        display_window.blit(quit_,(150,310))
        display_window.blit(dimg[int(time.time()*10%13)],(36,300,228,114))#every 0.1s change image
        display_window.blit(mimg[int(time.time()*10%38)],(0,0,100,180))
        display_window.blit(gimg[int(time.time()*10%4)],(300,100,100,180))
    else:
        display_window.blit(quit_,(150,260))
        display_window.blit(dimg[int(time.time()*10%13)],(36,300,228,114))
        display_window.blit(mimg[int(time.time()*10%38)],(0,0,100,180))
        display_window.blit(gimg[int(time.time()*10%4)],(300,100,100,180))
    screen.fill(game_corlor.WHITE)
    pygame.draw.rect(display_window,(255,255,0),curor.rect)   # cursor

    # wire frames
    y = 0  
    for i in range(25):
        pygame.draw.line(screen,game_corlor.BLACK , (0, y), (720, y), 1)
        y += 24
    x = 0
    for i in range(30):
        pygame.draw.line(screen,game_corlor.BLACK , (x, 0), (x,600), 1)
        x += 24

    # alive cells
    for line in life_game.point:
        for point in line:
            if point.state == 1:
                pygame.draw.rect(screen,(140,0,255),point.rect)

    # if game is running, start the game logic
    if run == True:
        time_passed = clock.tick()    
        time_passed_second = time_passed / 1000  # ms
        key_press_time += time_passed_second # key pressed time
        bling_time += time_passed_second  # blink point time
        life_time += time_passed_second # updated generation


        if life_time >= life_game.life_time:    # should update
            life_game.life_loop()   # update
            bling_show = True    # start blink points
            should_change_point = life_game.get_need_change_point() # getting the blink points
            life_time = 0 # reset
        
        # blink point
        for point in should_change_point:
            if point[1] == 3 and point[2] == 0:
                if bling_time < life_game.life_time / 2 and bling_show:
                    #s = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    pygame.draw.rect(screen,game_corlor.GREEN,point[0].rect)
                else:
                    bling_time = 0
                    bling_show = False
        # if the press time greater than twice iterations
        if key_press_time >= life_game.life_time * 2:
            life_game.random_point(people.pid,random_point_num)
            key_press_time = 0

        # position of player
        pygame.draw.rect(screen,people.corlor,people.rect)

            
        # collision
        if hit_check(people):
            run = False
            top_title = "you fail!"

        # if player reach the end point
        if is_over(people):
            run = False
            top_title = "you win!"
    # if game is not running, display the menu    
    if run == False:
        if top_title == "stop":
            curor.is_run = True
        else:
            curor.is_run = False
        screen.blit(display_window,(160,100))
    # update
    pygame.display.flip()

