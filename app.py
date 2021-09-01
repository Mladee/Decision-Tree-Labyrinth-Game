import turtle
import math
import random


import pandas as pd
import time


import warnings
warnings.filterwarnings("ignore")


from sklearn.tree import DecisionTreeClassifier

global p

p = 1
Player_Ox = []
Player_Oy = []
Enemy_Ox = []
Enemy_Oy = []
all_states = []

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Basic Maze Game ")
wn.setup(700,700)
wn.tracer(0) #<- if not for this it would take 10 secs to make the labyrinth
# 24 * 24 blocks(for image compatibility purposes) => the length-width of the blocks will be 576px so I chose the 700,700 setup
# to have enough free space around my blocks for visibility purposes
# top right square coordinates: (-288,288)

turtle.register_shape("wizard-left.gif")
turtle.register_shape("wizard-right.gif")
turtle.register_shape("wall.gif")
turtle.register_shape("treasure.gif")
turtle.register_shape("monster.gif")

global decision_tree



class  Pen(turtle.Turtle):
        def  __init__(self):
                turtle.Turtle.__init__(self)
                self.shape("square")
                self.color("blue")
                self.penup()
                self.speed(0)

class  Player(turtle.Turtle):
        def  __init__(self):
                turtle.Turtle.__init__(self)
                self.shape("wizard-right.gif")
                self.color("red")
                self.penup()
                self.speed(0)
                self.gold = 0


        def go_up(self):
                move_to_X = player.xcor()
                move_to_Y = player.ycor() + 24

                if (move_to_X,move_to_Y) not in walls:
                        self.goto(move_to_X,move_to_Y)
                        Player_Ox.append(move_to_X)
                        Player_Oy.append(move_to_Y)

        def go_down(self):
                move_to_X = player.xcor()
                move_to_Y = player.ycor() - 24

                if (move_to_X, move_to_Y) not in walls:
                        self.goto(move_to_X, move_to_Y)
                        Player_Ox.append(move_to_X)
                        Player_Oy.append(move_to_Y)

        def go_left(self):
                move_to_X = player.xcor() - 24
                move_to_Y = player.ycor()
                self.shape("wizard-left.gif")
                if (move_to_X, move_to_Y) not in walls:
                        self.goto(move_to_X, move_to_Y)
                        Player_Ox.append(move_to_X)
                        Player_Oy.append(move_to_Y)

        def go_right(self):
                move_to_X = player.xcor() + 24
                move_to_Y = player.ycor()
                self.shape("wizard-right.gif")
                if (move_to_X, move_to_Y) not in walls:
                        self.goto(move_to_X, move_to_Y)
                        Player_Ox.append(move_to_X)
                        Player_Oy.append(move_to_Y)


        def is_collision(self,other):
                a = self.xcor() - other.xcor()
                b = self.ycor() - other.ycor()
                distance = math.sqrt((a ** 2) + (b ** 2))
                if distance < 2:
                        return True
                else:
                        return False


class  Treasure(turtle.Turtle):
        def  __init__(self,x,y):
                turtle.Turtle.__init__(self)
                self.shape("treasure.gif")
                self.color("gold")
                self.penup()
                self.speed(0)
                self.gold = 100
                self.goto(x,y)

        def destroy(self):
                self.goto(2000,2000)
                self.hideturtle()


class  Enemy(turtle.Turtle):
        def  __init__(self,x,y):
                turtle.Turtle.__init__(self)
                self.shape("monster.gif")
                self.penup()
                self.speed(0)
                self.goto(x,y)
                self.directions = random.choice(['up','down','left','right'])

        def move(self):
                if (self.directions == 'up'):
                        dx = 0
                        dy = 24
                elif (self.directions == 'down'):
                        dx = 0
                        dy = -24
                elif (self.directions == 'left'):
                        dx = -24
                        dy = 0
                elif (self.directions == 'right'):
                        dx = 24
                        dy = 0
                else:
                        dx = 0
                        dy = 0


                if self.is_close(player):
                        if player.xcor() < self.xcor():
                                self.directions = 'left'
                        elif player.xcor() > self.xcor():
                                self.directions = 'right'
                        elif player.ycor() < self.ycor():
                                self.directions = 'down'
                        elif player.ycor() > self.ycor():
                                self.directions = 'up'

                move_x = self.xcor() + dx
                move_y = self.ycor() + dy

                start_time = time.time()
                enemy_time = time.time() - start_time

                if enemy_time < 3:
                        if self.is_close(player):
                                turtle.ontimer(self.move, t=random.randint(70, 250))  # chasing speed
                        else:
                                turtle.ontimer(self.move, t=random.randint(100, 300))  # patrol speed
                elif enemy_time >= 5:
                        self.predict_speed()
                
                

                if (move_x,move_y) not in walls:
                        self.goto(move_x,move_y)
                        Enemy_Ox.append(move_x)
                        Enemy_Oy.append(move_y)
                        if self.is_close(player):
                                all_states.append('chasing')
                        elif self.is_collision(player):
                                all_states.append('lose')
                        else:
                                all_states.append('patrol')
                        
                        

                else:
                        self.directions = random.choice(['up', 'down', 'left', 'right'])




        def predict_speed(self):
                for i in p.index:
                        if p['Pred'][i] == 0:
                                turtle.ontimer(self.move, t=random.randint(100, 200))  # patrol speed
                        elif p['Pred'][i] == 1:
                                turtle.ontimer(self.move, t=random.randint(50, 150))  # chasing speed


        def is_close(self,other):
                a = self.xcor() - other.xcor()
                b = self.ycor() - other.ycor()
                distance = math.sqrt((a ** 2) + (b ** 2) )


                if distance < 200: # 8 blocks range( 24 * 8 = 192 but we will aproximate to 200)
                        return True
                else:
                        return False
        def is_collision(self,other):
                a = self.xcor() - other.xcor()
                b = self.ycor() - other.ycor()
                distance = math.sqrt((a ** 2) + (b ** 2) )


                if distance < 2:
                        return True
                else:
                        return False

        def destroy(self):
                self.goto(2000,2000)
                self.hideturtle()

level = [
"XXXXXXXXXXXXXXXXXXXXXXXX",
"XP  XXXXXXXXXE      XXXX",
"X    XXXXXXX      XXXXXX",
"X       XXXXXX     XXXX",
"X    E            XX   X",
"XXXXXX     XX     XXXXXX",
"XXXXXX     XX      XXXXX",
"XXXXXX     XX         XX",
"XXXXE     XXXXXXXXXXX XX",
"XXXX      XXXXXXXXXXX TX",
"XXXX   XXXXXXXXXX      X",
"XXXX      XXXXXXE  XXXXX",
"XXXXXXXX           XXXXX",
"XXXX      XXXXXX   EXXXX",
"XXXX                 XXX",
"XXXX XX X XXXXXXX    XXX",
"XXXX X  X XXXXXXX    XXX",
"XXXX      XXXXXXX  XTXXX",
"XXXX XXX    XXXXX X XXXX",
"XXXX      XXXT      XXXX",
"XXXXT     XXXXXXXX   XXX",
"XE    XX      XXXX XXXXX",
"XXXXXXXXXXX       TXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXX"]

treasures = []
enemies = []
def setup_maze(level):
        for y in range(len(level)):
                for x in range(len(level[y])):
                        character = level[y][x]
                        screen_x = -288 + (x * 24)
                        screen_y = 288 - (y * 24)

                        if character == "X":
                                pen.goto(screen_x, screen_y)
                                pen.shape("wall.gif")
                                pen.stamp()
                                walls.append((screen_x,screen_y))

                        if character == "P":
                                player.goto(screen_x, screen_y)

                        if character == "T":
                                treasures.append(Treasure(screen_x,screen_y))

                        if character == "E":
                                enemies.append(Enemy(screen_x, screen_y))





pen= Pen()
player = Player()

walls = []


def start_game():
        global game_state
        game_state = "game"
#Key bindings
turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_down,"Down")
turtle.onkey(player.go_up,"Up")

def quit():
        global running
        running = False


wn.listen()
wn.onkeypress(quit,"q")

running = True
setup_maze(level)
# print(walls) <- to check that the walls are where we expect them to be(coordinate wise)
wn.tracer(0)


#make the enemies move!
for enemy in enemies:
        turtle.ontimer(enemy.move, t = 250)

game_state = "game"
start_time = time.time()

while running:

        elapsed_time = time.time() - start_time

        #print(elapsed_time)

        if game_state == "victory":

                pen.clear()
                wn.bgpic('victory.gif')
                turtle.done()


        elif game_state == "lose":

                pen.clear()
                wn.bgpic('defeat.gif')
                turtle.done()


        elif game_state == "game":




                if ((elapsed_time > 3) and (elapsed_time < 4)):


                        dataframe = pd.DataFrame([Player_Ox,Player_Oy,Enemy_Ox,Enemy_Oy,all_states]).T
                        col_names = ['Player Ox','Player Oy','Enemy Ox','Enemy Oy','Action']
                        dataframe.columns = col_names
                        df = dataframe.iloc[:20,:]
                        df = df.fillna(method='ffill')
                        print(df)

                        # we encode the actions: patrol -> 0 chasing -> 1
                        for i in range(len(df['Action'])):
                                if df['Action'][i] == 'patrol':
                                        df['Action'][i] = 0
                                elif df['Action'][i] == 'chasing':
                                        df['Action'][i] = 1

                        df = df.astype(int)
                        X_train = df.drop(['Action'], axis=1)
                        y_train = df['Action']

                        #print(df.dtypes)

                        decision_tree = DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=2)
                        decision_tree.fit(X_train,y_train)

                        score = decision_tree.score(X_train,y_train)

                        print('Decision Tree Model Score: {}%'.format(score * 100))
                        print('0 ---> patrol')
                        print('1 ---> chasing')
                        print('---' * 15)

                if ((elapsed_time > 4) and (elapsed_time < 5)):

                        dataframe2 = pd.DataFrame([Player_Ox, Player_Oy, Enemy_Ox, Enemy_Oy]).T
                        col_names = ['Player Ox', 'Player Oy', 'Enemy Ox', 'Enemy Oy']
                        dataframe2.columns = col_names
                        df2 = dataframe2.iloc[:20, :]
                        df2 = df2.fillna(method='ffill')

                        print(df2)

                        X_test = df2.astype(int)
                        predictions = decision_tree.predict(X_test)
                        print('Decision Tree Action Predictions: {}'.format(predictions))
                        p = pd.DataFrame(predictions, columns = ['Pred'])




                for treasure in treasures:
                        if player.is_collision(treasure):
                                player.gold += treasure.gold
                                print('Player Gold: {}'.format(player.gold))
                                treasure.destroy()
                                treasures.remove(treasure)
                for enemy in enemies:
                        if (player.is_collision(enemy)):

                                for treasure in treasures:
                                        treasure.reset()
                                        treasure.hideturtle()
                                for enemy in enemies:
                                        enemy.reset()
                                        enemy.hideturtle()
                                player.reset()
                                player.hideturtle()


                                game_state = "lose"

                if player.gold >= 500:

                        for treasure in treasures:
                                treasure.reset()
                                treasure.hideturtle()
                        for enemy in enemies:
                                enemy.reset()
                                enemy.hideturtle()
                        player.reset()
                        player.hideturtle()
                        game_state = "victory"
        
        wn.update()
wn.bye()

