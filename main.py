from os import system
from random import randint, choice


class ship:  #generates ships with specificied size and position
    def __init__(self, length, First_x, Final_x, First_y, Final_y):
        self.length = length  #sounds pointless but is important
        self.x, self.y = [], []
        for i in range(self.length):
            self.x.append(First_x + ((Final_x - First_x) / self.length) * i)
            self.y.append(First_y + ((Final_y - First_y) / self.length) * i)

    def details(self):  #returns size and coordinates of the made ship
        coords = []
        for i in self.x:
            coords.append([i])
        for i in range(len(self.y)):
            coords[i].append(self.y[i])
        return coords


class grid:  #creates and draws the grid
    def __init__(self, x, y, shots, owned, owner):
        self.x = x
        self.y = 3 * round(y / 3)
        self.shots, self.owned, self.owner = shots, owned, owner
        self.shot()
        if self.owner == 0:
            self.draw()
        else:
            self.edraw()

    def shot(self):  #reformats some important lists for later use
        for i in range(len(self.shots)):
            self.shots[i][1] = int(round((self.shots[i][1] * 3) / 3))
            self.shots[i][0] = int(self.shots[i][0])
        for i in range(len(self.owned)):
            for s in range(len(self.owned[i])):
                self.owned[i][s][1] = int(round((self.owned[i][s][1] * 3) / 3))
                self.owned[i][s][0] = int(self.owned[i][s][0])
        #print(self.owned, "shot")

    def draw(self):  #draws the players grid
        column = "|"
        for i in range(self.y):
            for s in range(self.x):
                if (i + 1) % 3 == 0 and (i + 1) != self.y:
                    HSM = "___|"  #bottom of a row
                elif (i + 1) % 3 == 1:
                    HSM = "   |"  #top of a row
                else:  #central area, shows empty, ship or hit ship
                    for y in self.owned:
                        if [s, i] in y and [s, i] in self.shots:
                            HSM = " Ø |"
                            break
                        elif [s, i] in y and [s, i] not in self.shots:
                            HSM = " █ |"
                            break
                        elif [s, i] in self.shots and [s, i] not in y:
                            HSM = " + |"
                            break
                        else:
                            HSM = "   |"
                column += HSM
            print(column)  #shows the grid
            column = "|"

    def edraw(self):  #draws enemy grid, like draw
        column = "|"
        for i in range(self.y):
            for s in range(self.x):
                if (i + 1) % 3 == 0 and (i + 1) != self.y:
                    HSM = "___|"
                elif (i + 1) % 3 == 1:
                    HSM = "   |"
                else:
                    #print("this should be seen")
                    for y in self.owned:
                        if [s, i] in self.shots and [s, i] in y:
                            #if [s, i] in y:
                            HSM = " ◘ |"
                            break
                        elif [s, i] in self.shots and [s, i] not in y:
                            HSM = " × |"
                        else:
                            HSM = "   |"
                column += HSM
            print(column)
            column = "|"


class fleet:  #defines each sides fleets
    def __init__(self, number, lengths, owner, final, x, y):
        self.number, self.lengths, self.owner, self.final = number, lengths, owner, final  #stuff for the fleet
        self.x, self.y = x, y - 3  #grid size
        self.build()

    def details(self):  #returns a list of whats in each fleet
        return self.final, self.owner

    def build(self):  #builds ships using ship class
        Ship = []  #current ships coords
        while self.number > 0:
            current_ship = self.lengths[self.number - 1]
            up_down = randint(0, 1)  #vertical or horizontal
            fail = True
            if up_down == 0:
                while fail == True:
                    while True:
                        x, y = randint(0, self.x), randint(0, self.y)
                        y = 3 * round(y / 3) + 1
                        if x + current_ship < self.x and y < self.y:
                            break
                    Ship = (ship(current_ship, x, x + current_ship, y,
                                 y).details())
                    if len(self.final) == 0:
                        fail = False
                    else:
                        for i in self.final:
                            for s in i:
                                if s in Ship:
                                    fail = True
                                    break
                                else:
                                    fail = False
                            if fail == True:
                                break
                self.final.append(Ship)

            elif up_down == 1:
                while fail == True:
                    while True:
                        x, y = randint(0, self.x - 1), randint(0, self.y)
                        y = 3 * round(y / 3) + 1
                        if y + current_ship < self.y and x < self.x:
                            break
                    Ship = (ship(current_ship, x, x, y,
                                 y + current_ship).details())
                    if len(self.final) == 0:
                        fail = False
                    else:
                        for i in self.final:
                            for s in i:
                                if s in Ship:
                                    fail = True
                                    break
                                else:
                                    fail = False
                            if fail == True:
                                break
                for i in range(len(Ship)):
                    Ship[i][1] = Ship[i][1] + (i * 2)
                self.final.append(Ship)
            self.number -= 1
            if self.number == 0:
                break


class gun:
    def __init__(self, x, y, shots, enemy):
        self.x, self.y = x, y
        self.shots, self.enemy = shots, enemy

    def e_shoot(self):
        fire = ""
        checking = True
        while checking == True:
            for i in self.enemy:
                for s in i:
                    if s in self.shots:
                        if s[0] + 1 in self.shots:
                            fire += "LEFT" + str(s) + "," + str(i) + " "
                        if s[0] - 1 in self.shots:
                            fire += "RIGHT" + str(s) + str(i) + " "
                        if s[1] + 3 in self.shots:
                            fire += "UP" + str(s) + str(i) + " "
                        if s[1] - 3 in self.shots:
                            fire += "DOWN" + str(s) + str(i) + " "
                        break
            if fire == "":
                fire += "RAND"
            try:
                firing = fire.split(" ")
            except:
                firing = ["RAND"]
            if len(firing) >= 2:
                firing = [choice(firing)]
            firing = firing[0]
            if firing == "RAND":
                while True:
                    attack = [
                        randint(0, self.x),
                        3 * round(randint(0, self.y) / 3) + 1
                    ]
                    if attack not in self.shots:
                        checking = False
                        break
            if "LEFT" in firing:
                loca = firing[4:]
                loca = loca.split(",")
                loca[1] = 3 * round(int(loca[1]) / 3) + 1
                loca[0] = int(loca[0]) - 1
                attack = loca
                checking = False
            elif "RIGHT" in firing:
                loca = firing[5:]
                loca = loca.split(",")
                loca[1] = 3 * round(int(loca[1]) / 3) + 1
                loca[0] = int(loca[0]) + 1
                attack = loca
                checking = False
            elif "UP" in firing:
                loca = firing[2:]
                loca = loca.split(",")
                loca[1] = 3 * round(int(loca[1]) / 3) + 4
                loca[0] = int(loca[0])
                attack = loca
                checking = False
            elif "DOWN" in firing:
                loca = firing[4:]
                loca = loca.split(",")
                loca[1] = 3 * round(int(loca[1]) / 3) - 2
                loca[0] = int(loca[0])
                attack = loca
                checking = False
        return attack

    def my_shoot(self):
        print("the grids are", self.x, "by", self.y // 3)
        firing = True
        while firing == True:
            try:
                loca = input(
                    "please input the coordinates you want to fire at, seperated by a space. "
                )
                if loca[0] == " ":
                    loca = loca[1:]
                print(loca)
                attack = loca.split(" ")
                if len(attack) == 2:
                    for i in range(len(attack)):
                        attack[i] = int(attack[i])
                    attack[1] *= 3
                    attack[1] = 3 * round(attack[1] / 3) + 1
                    if (attack[0] >= 0 and attack[0] <= self.x
                            and attack[1] >= 0 and attack[1] <= self.y):
                        if attack not in self.shots:
                            firing = False
                            break
                        else:
                            print("you have already fired there")
                    else:
                        print("something is wrong with that input, try again",
                              "\n")
            except:
                print("something is wrong with that input, try again", "\n")
                pass
        return attack


def victor(e_shots, my_shots, p_fleet, e_fleet):
    p_win, e_win = True, True
    for i in p_fleet:
        for s in i:
            if s not in e_shots:
                e_win = False
    for i in e_fleet:
        for s in i:
            if s not in my_shots:
                p_win = False
    if p_win == True:
        return False, 1
    elif e_win == True:
        return False, 2
    else:
        return True, 0


def run():
    x, y = 25, 3 * round(22 / 3)
    play = True
    my_shots = []
    e_shots = []
    player_fleet = fleet(7, [3, 3, 5, 2, 4, 5, 6, 3, 2], 0, [], x, y)
    player_deets = player_fleet.details()
    enemy_fleet = fleet(7, [3, 3, 5, 2, 4, 5, 6, 3, 2], 1, [], x, y)
    enemy_deets = enemy_fleet.details()
    while play == True:
        system("clear")
        print("your grid:")
        grid(x, y, e_shots, player_deets[0], player_deets[1])
        print()

        print("enemy grid:")
        grid(x, y, my_shots, enemy_deets[0], enemy_deets[1])
        my_shots.append(gun(x, y, my_shots, enemy_deets[0]).my_shoot())
        e_shots.append(gun(x, y, e_shots, player_deets[0]).e_shoot())

        end = victor(e_shots, my_shots, player_deets[0], enemy_deets[0])
        play = end[0]
    if end[1] == 1:
        print("the player has won! grats")
    elif end[1] == 2:
        print("the enemy has won! big sad")


run()
