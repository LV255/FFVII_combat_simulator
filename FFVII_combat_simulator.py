import random
import time

gameRunning = True
campaign_mode = False

print()
print("### Welcome to the Final Fantasy VII combat simulator ###")
time.sleep(1)

def choose_single_multi():
    choice = input (""" 
Which game mode do you want to play?

(s) single player   - play one match against a computer opponent
(m) two player      - play against another person
(c) campaign        - play a series of matches against computer opponents

(type s, m or c and press enter): """).lower().strip()
    if choice == "s":
        time.sleep(0.5)
        choose_player1()
        comp_choose_player2()
        play_vs_computer()
    elif choice == "m":
        time.sleep(0.5)
        choose_player1()
        choose_player2()
        play_multi()
    elif choice == "c":
        time.sleep(0.5)
        global campaign_mode
        choose_player1()
        comp_choose_player2()
        campaign_mode = True
        play_vs_computer()
    else:
        time.sleep(0.5)
        print()
        print("Sorry, input not recognised.")
        time.sleep(1)
        choose_single_multi()

def choose_player1():
    print()
    print("Select player 1:")
    print()
    for num, name in zip(range(len(soldierlist)), soldierlist):
        print("{} {}".format(name.name, "("+ str(num+1) +")"))
    print()
    print("view character info (i)")
    print("view game explanation (e)")
    print()
    choice = input("type letter or number and press enter: ").lower().strip()
    try:
        if choice == "i":
            time.sleep(0.5)
            for list in soldierlist:
                print(list)
            time.sleep(1)
            choose_player1()
        elif choice == "e":
            time.sleep(0.5)
            print("""
Final Fantasy VII combat simulator is a turn based fighting game based on Final Fantasy VII.
Firstly, choose two players by selecting their number.
Then, fight against each other in a turn based fighting system.
Each character has unique strengths, weaknesses and abilities.
If a player loses a lot of health points they can use a "limit break" special attack.""")
            time.sleep(1)
            choose_player1()
        else:
            global player1
            time.sleep(0.5)
            x = soldierlist.pop(int(choice) - 1)
            deadsoldiers.append(x)
            player1 = x
    except (IndexError, ValueError):
        time.sleep(0.5)
        print()
        print("Sorry, input not recognised.")
        time.sleep(1)
        choose_player1()

def choose_player2():
    print()
    print("Select player 2:")
    print()
    for num, name in zip(range(len(soldierlist)), soldierlist):
        print("{} {}".format(name.name, "("+ str(num+1) +")"))
    print()
    print("view character info (i)")
    print("view game explanation (e)")
    print()
    choice = input("type letter or number and press enter: ").lower().strip()
    try:
        if choice == "i":
            time.sleep(0.5)
            for list in soldierlist:
                print(list)
            time.sleep(1)
            choose_player2()
        elif choice == "e":
            time.sleep(0.5)
            print("""
Final Fantasy VII combat simulator is a turn based fighting game based on Final Fantasy VII.
Firstly, choose two players by selecting their number.
Then, fight against each other in a turn based fighting system.
Each character has unique strengths, weaknesses and abilities.
If a player loses a lot of health points they can use a "limit break" special attack.""")
            time.sleep(1)
            choose_player2()
        else:
            global player2
            time.sleep(0.5)
            x = soldierlist.pop(int(choice) - 1)
            deadsoldiers.append(x)
            player2 = x
    except (IndexError, ValueError):
        time.sleep(0.5)
        print()
        print("Sorry, input not recognised.")
        time.sleep(1)
        choose_player2()

def comp_choose_player2():
    global player2
    r = random.randint(1, len(soldierlist))
    x = soldierlist.pop(int(r) - 1)
    deadsoldiers.append(x)
    player2 = x

def campaign_restart():
    global gameRunning
    if (len(soldierlist)) > 0:
        gameRunning = True
        comp_choose_player2()
        play_vs_computer()
    else:
        time.sleep(1)
        print()
        print("     WELL DONE! YOU WIN!     ")
        print()

deadsoldiers = []
soldierlist = []

class soldier:
    def __init__(self, name, hp, mp, weapon, damage, spell1, spell2, weak, armour, limitbreak):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.full_hp = hp
        self.weapon = weapon
        self.spell1 = spell1
        self.spell2 = spell2
        self.weapon_damage = damage
        self.weak_against = weak
        self.armour = armour
        self.hplost = 0
        self.limit_break = limitbreak
        soldierlist.append(self)
        self.has_scanned = False
        self.enemy_weakness = []

    def __repr__(self):
        description = """
---  {name}  ---             
Health points (hp):     {hp}     
Magic points (mp):      {mp}    
Weapon:                 {weapon} (damage: {damage})   
abilities:              attack(a), cast {spell1}({s1s}), cast {spell2}({s2s}), scan(s)""".format(name=self.name,
                                                                                 hp=self.hp,
                                                                                 mp=self.mp,
                                                                                 weapon=self.weapon,
                                                                                 damage=self.weapon_damage,
                                                                                 spell1=self.spell1,
                                                                                 spell2=self.spell2,
                                                                                 s1s=self.spell1[0],
                                                                                 s2s=self.spell2[0])
        if self.hplost >= (self.full_hp*0.7):
            description += """
LIMIT BREAK:            {limit} (x)""".format(limit=self.limit_break)
        return description

    def attack(self, other):
        other.hp -= (self.weapon_damage - other.armour)
        other.hplost += (self.weapon_damage - other.armour)
        print()
        print(self.name + " attacks " + other.name + " causing " + str(self.weapon_damage - other.armour) + " damage!")
        time.sleep(2)

    def castfire(self, other):
        if self.mp < 15:
            print()
            print("not enough MP!")
            time.sleep(2)
            self.move(other)
        elif self.mp >= 15 and other.weak_against == "fire":
            other.hp -= 45
            other.hplost += 45
            self.mp -= 15
            print()
            print(self.name + " casts fire causing 45 damage!")
            time.sleep(2)
        else:
            other.hp -= 35
            other.hplost += 35
            self.mp -= 15
            print()
            print(self.name + " casts fire causing 35 damage!")
            time.sleep(2)

    def castlightning(self, other):
        if self.mp < 15:
            print()
            print("not enough MP!")
            time.sleep(2)
            self.move(other)
        elif self.mp >= 15 and other.weak_against == "lightning":
            other.hp -= 45
            other.hplost += 45
            self.mp -= 15
            print()
            print(self.name + " casts lightning causing 45 damage!")
            time.sleep(2)
        else:
            other.hp -= 35
            other.hplost += 35
            self.mp -= 15
            print()
            print(self.name + " casts lightning causing 35 damage!")
            time.sleep(2)

    def castice(self, other):
        if self.mp < 15:
            print()
            print("not enough MP!")
            time.sleep(2)
            self.move(other)
        elif self.mp >= 15 and other.weak_against == "ice":
            other.hp -= 45
            other.hplost += 45
            self.mp -= 15
            print()
            print(self.name + " casts ice causing 45 damage!")
            time.sleep(2)
        else:
            other.hp -= 35
            other.hplost += 35
            self.mp -= 15
            print()
            print(self.name + " casts ice causing 35 damage!")
            time.sleep(2)

    def castpoison(self, other):
        if self.mp < 15:
            print()
            print("not enough MP!")
            time.sleep(2)
            self.move(other)
        elif self.mp >= 15 and other.weak_against == "poison":
            other.hp -= 45
            other.hplost += 45
            self.mp -= 15
            print()
            print(self.name + " casts poison causing 45 damage!")
            time.sleep(2)
        else:
            other.hp -= 35
            other.hplost += 35
            self.mp -= 15
            print()
            print(self.name + " casts poison causing 35 damage!")
            time.sleep(2)

    def castheal(self, other):
        if self.mp < 20:
            print()
            print("not enough MP!")
            time.sleep(2)
            self.move(other)
        elif self.mp >= 20 and self.hp >= (self.full_hp - 50):
            print()
            print(self.name + " heals by " + str(self.full_hp - self.hp) + "!")
            self.hp = self.full_hp
            self.mp -= 20
            time.sleep(2)
        elif self.mp >= 20:
            self.hp += 50
            self.mp -= 20
            print()
            print(self.name + " heals by 50!")
            time.sleep(2)

    def castrestore(self, other):
        if self.mp < 30:
            print()
            print("not enough MP!")
            time.sleep(2)
            self.move(other)
        elif self.mp >= 30:
            self.hp = self.full_hp
            self.mp -= 30
            print()
            print(self.name + " restores to full health!")
            time.sleep(2)

    def limitbreak(self, other):
        other.hp -= (70 - other.armour)
        other.hplost += (70 - other.armour)
        self.hplost = 0
        print()
        print(self.name + " attacks " + other.name + " with " + str(self.limit_break) + " causing "
              + str(70 - other.armour) + " damage!")
        time.sleep(2)

    def scan(self, other):
        print()
        print("{name} scans {name2}.".format(name=self.name, name2=other.name))
        time.sleep(1)
        print()
        print("{name} has level {armour} armour and is weak against {weak}.".format(name=other.name,
                                                                                    armour=other.armour,
                                                                              weak=other.weak_against))
        time.sleep(2)

    def move(self, other):
        time.sleep(0.5)
        print()
        print("*** " + self.name + "'s move ***")
        time.sleep(0.5)
        print()
        move = input("Select move (type letter and press enter): ").lower().strip()
        if move == "a":
            time.sleep(0.5)
            self.attack(other)
        elif move == "f" and ((self.spell1 == "fire") or (self.spell2 == "fire")):
            time.sleep(0.5)
            self.castfire(other)
        elif move == "l" and ((self.spell1 == "lightning") or (self.spell2 == "lightning")):
            time.sleep(0.5)
            self.castlightning(other)
        elif move == "i" and ((self.spell1 == "ice") or (self.spell2 == "ice")):
            time.sleep(0.5)
            self.castice(other)
        elif move == "p" and ((self.spell1 == "poison") or (self.spell2 == "poison")):
            time.sleep(0.5)
            self.castpoison(other)
        elif (move == "h") and ((self.spell1 == "heal") or (self.spell2 == "heal")):
            time.sleep(0.5)
            self.castheal(other)
        elif move == "r" and ((self.spell1 == "restore") or (self.spell2 == "restore")):
            time.sleep(0.5)
            self.castrestore(other)
        elif move == "s":
            time.sleep(0.5)
            self.scan(other)
        elif move == "x" and (self.hplost >= (self.full_hp * 0.7)):
            time.sleep(0.5)
            self.limitbreak(other)
        else:
            print()
            print("Invalid input.")
            time.sleep(2)
            self.move(other)

    def checkwin(self):
        global gameRunning
        global turn_count
        if player1.hp <= 0:
            print()
            print("     !!! " + str(player2.name) + " wins !!! ")
            gameRunning = False
            if campaign_mode == True:
                turn_count = 0
                time.sleep(1)
                campaign_restart()
        elif player2.hp <= 0:
            print()
            print("     !!! " + str(player1.name) + " wins !!! ")
            gameRunning = False
            if campaign_mode == True:
                turn_count = 0
                time.sleep(1)
                campaign_restart()

# add new characters here
# KEY: name, hp, mp, weapon, damage, spell1, spell2, weak, armour, limit break):

cloud = soldier("Cloud", 150, 100, "Buster Sword", 500, "fire", "lightning", "ice", 1, "Braver")
sephiroth = soldier("Sephiroth", 250, 25, "Masamune", 25, "poison", "heal", "poison", 1, "Masumune storm")
tiffa = soldier("Tiffa", 125, 50, "Leather glove", 15, "heal", "fire", "fire", 2, "Beat rush")
barret = soldier("Barret", 200, 75, "Gatling gun", 20, "poison", "fire", "poison", 3, "Big shot")
redxiii = soldier("Red XIII", 175, 100, "Mythril clip", 15, "heal", "fire", "fire", 3, "Sled fang")
aeris = soldier("Aeris", 100, 200, "Guard stick", 10, "ice", "restore", "poison", 3, "Deadly wind")
yuffie = soldier("Yuffie", 100, 100, "Shuriken", 10, "ice", "fire", "lightning", 1, "Greased lightning")
cid = soldier("Cid", 225, 25, "Spear", 20, "lightning", "poison", "ice", 2, "Boost jump")

campaign_mode_round = 1
turn_count = 0

def turn():
    global turn_count
    if (campaign_mode == True) and (turn_count == 0):
        global campaign_mode_round
        print()
        print("         Round " + str(campaign_mode_round) +"!")
        campaign_mode_round += 1
        time.sleep(1)
        print()
        print("      *** Start! ***      ")
        turn_count += 1
        time.sleep(1)
    elif (campaign_mode == True) and (turn_count > 0):
        print()
        print("      *** Next turn! ***      ")
        time.sleep(1)
    elif turn_count == 0:
        print()
        print("      *** Start! ***      ")
        turn_count += 1
        time.sleep(1)
    elif turn_count > 0:
        print()
        print("      *** Next turn! ***      ")
        time.sleep(1)

def computer():
    print(player1)
    print(player2)
    time.sleep(0.5)
    print()
    print("*** " + player2.name + "'s move ***")
    time.sleep(1)

    if (player2.hp < 50) and ((player2.spell1 == "restore") or (player2.spell2 == "restore")) and (player2.mp >= 30):
        x = random.randint(0, 3)
        time.sleep(0.5)
        if x <= 2:
            player2.castrestore(player1)
        elif x == 3:
            player2.attack(player1)
    elif (player2.hp < 75) and ((player2.spell1 == "heal") or (player2.spell2 == "heal")) and (player2.mp >= 20):
        x = random.randint(0, 1)
        time.sleep(0.5)
        if x == 0:
            player2.castheal(player1)
        elif x == 1:
            player2.attack(player1)
    elif player2.hplost >= (player2.full_hp * 0.7):
        x = random.randint(0, 3)
        time.sleep(0.5)
        if x <= 2:
            player2.limitbreak(player1)
        elif x == 3:
            player2.attack(player1)
    elif player2.has_scanned == False:
        x = random.randint(0, 1)
        time.sleep(0.5)
        if x == 0:
            player2.scan(player1)
            player2.enemy_weakness.append(player1.weak_against)
            player2.has_scanned = True
            print()
            print("\"I know you are weak against " + str(player2.enemy_weakness[0]) +"!\"")
            time.sleep(2)
        elif x == 1:
            player2.attack(player1)
    elif ((player2.spell1 == "fire") or (player2.spell2 == "fire")) and (player2.enemy_weakness[0] == "fire") and (player2.mp >= 15):
        x = random.randint(0, 1)
        time.sleep(0.5)
        if x == 0:
            player2.castfire(player1)
        elif x == 1:
            player2.attack(player1)
    elif ((player2.spell1 == "lightning") or (player2.spell2 == "lightning")) and (player2.enemy_weakness[0] == "lightning") and (player2.mp >= 15):
        x = random.randint(0, 1)
        time.sleep(0.5)
        if x == 0:
            player2.castlightning(player1)
        elif x == 1:
            player2.attack(player1)
    elif ((player2.spell1 == "ice") or (player2.spell2 == "ice")) and (player2.enemy_weakness[0] == "ice") and (player2.mp >= 15):
        x = random.randint(0, 1)
        time.sleep(0.5)
        if x == 0:
            player2.castice(player1)
        elif x == 1:
            player2.attack(player1)
    elif ((player2.spell1 == "poison") or (player2.spell2 == "poison")) and (player2.enemy_weakness[0] == "poison") and (player2.mp >= 15):
        x = random.randint(0, 1)
        time.sleep(0.5)
        if x == 0:
            player2.castpoison(player1)
        elif x == 1:
            player2.attack(player1)
    elif player2.mp >= 15:
        x = random.randint(0, 1)
        time.sleep(0.5)
        if x == 0:
            temp_spell_list = []
            temp_spell_list.append(player2.spell1)
            temp_spell_list.append(player2.spell2)
            x = random.randint(0, 1)
            if temp_spell_list[x] == "fire":
                player2.castfire(player1)
            elif temp_spell_list[x] == "lightning":
                player2.castlightning(player1)
            elif temp_spell_list[x] == "ice":
                player2.castice(player1)
            elif temp_spell_list[x] == "poison":
                player2.castpoison(player1)
        elif x == 1:
            player2.attack(player1)
    else:
        time.sleep(0.5)
        player2.attack(player1)

def play_vs_computer():
    x = random.randint(0, 1)
    if x == 0:
        def round2():
            while gameRunning:
                turn()
                computer()
                player1.checkwin()
                round1()

        def round1():
            while gameRunning:
                turn()
                time.sleep(1)
                print(player1)
                print(player2)
                player1.move(player2)
                player1.checkwin()
                round2()
        round1()

    else:
        def round2():
            while gameRunning:
                turn()
                time.sleep(1)
                print(player1)
                print(player2)
                player1.move(player2)
                player1.checkwin()
                round1()

        def round1():
            while gameRunning:
                turn()
                computer()
                player1.checkwin()
                round2()

        round1()

def play_multi():
    x = random.randint(0, 1)
    if x == 0:
        def round2():
            while gameRunning:
                turn()
                time.sleep(1)
                print(player1)
                print(player2)
                player2.move(player1)
                player2.checkwin()
                player2.checkwin()
                round1()

        def round1():
            while gameRunning:
                turn()
                time.sleep(1)
                print(player1)
                print(player2)
                player1.move(player2)
                player1.checkwin()
                round2()

        round1()

    else:
        def round2():
            while gameRunning:
                turn()
                time.sleep(1)
                print(player1)
                print(player2)
                player1.move(player2)
                player1.checkwin()
                round1()

        def round1():
            while gameRunning:
                turn()
                time.sleep(1)
                print(player1)
                print(player2)
                player2.move(player1)
                player2.checkwin()
                round2()

        round1()

choose_single_multi()






