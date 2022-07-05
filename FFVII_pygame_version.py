import pygame, sys, random

# initialise pygame
pygame.init()

# set fps
clock = pygame.time.Clock()
fps = 60

current_time = 0
timer = 0
# count for flashing text
count = 0

# create screen
screen = pygame.display.set_mode((1280, 720))

# whose turn is it?
turn = "player"
highlight = "player"


# current screen state
screen_state = "menu"


# set title, icon and background
pygame.display.set_caption("FFVII fight simulation")
icon = pygame.image.load('buster_icon.png')
pygame.display.set_icon(icon)

# define fonts
font = pygame.font.SysFont('Arial', 26)

# define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
dark_white = (150, 150, 150)

# upload images
background = pygame.image.load('midgar ff7 png.png')
panel = pygame.image.load('ff7 menu blank.png')
good_health = pygame.image.load("good_health_bar.png")
bad_health = pygame.image.load("bad_health_bar.png")
fifty_button = pygame.image.load("ff7 menu blank - 50.png")
small_button = pygame.image.load("ff7 small button.png")
small_panel = pygame.image.load("ff7 menu blank - sephiroth.png")
long_button = pygame.image.load("ff7 long button.png")
photo_border = pygame.image.load("photo border.jpg")

def draw_intro_screen():
    screen.blit(background, (0, 0))

def action_screen():
    draw_game_background()
    text_button.draw()
    draw_text(message_for_turn, font, white, 350, 85)

def draw_menu_screen():
    global screen_state
    global game_running
    screen.blit(background, (0, 0))

    screen.blit(panel, (50, 350))
    draw_text("Welcome to the Final Fantasy VII combat", font, white, 75, 365)
    draw_text("simulator.", font, white, 75, 395)
    draw_text("In this version you play as Cloud.", font, white, 75, 435)
    draw_text("You will fight against Sephiroth.", font, white, 75, 475)
    draw_text("More characters and game modes will be ", font, white, 75, 515)
    draw_text("introduced in the future.", font, white, 75, 545)

    if button_start.draw():
        screen_state = "game"
    if button_exit.draw():
        game_running = False


# used for countdown of hp and mp
cloud_current_hp = 0
sephiroth_current_hp = 0

cloud_current_mp = 0
sephiroth_current_mp = 0


def draw_game_background():
    global turn
    global end_announcment
    global screen_state
    screen.blit(background, (0, 0))

    # draw panels
    draw_panels()

    # draw health bars
    cloud_health_bar.draw(cloud_current_hp)
    sephiroth_health_bar.draw(sephiroth_current_hp)

    # draw mp bars
    cloud_mp_bar.draw_mp(cloud_current_mp)
    sephiroth_mp_bar.draw_mp(sephiroth_current_mp)

    # draw cloud buttons
    if button_2.draw() and turn == "player":
        cloud.attack(sephiroth)

    if button_3.draw() and turn == "player":
        cloud.castfire(sephiroth)

    if button_4.draw() and turn == "player":
        cloud.castlightning(sephiroth)

    if button_5.draw() and turn == "player":
        cloud.scan(sephiroth)

    if cloud.hplost >= (cloud.full_hp * 0.7):
        if button_6.draw() and turn == "player":
            cloud.limitbreak(sephiroth)
    # limit break only appear if we have limit break...

    if current_time - timer > 2500 and turn == "game over":
        if reset_button.draw():
            cloud.hp = cloud.full_hp
            cloud.mp = cloud.full_mp
            sephiroth.hp = sephiroth.full_hp
            sephiroth.mp = sephiroth.full_mp
            cloud.hplost = 0
            sephiroth.hplost = 0
            end_announcment = 0

            turn = "player"

        if return_menu_button.draw():
            cloud.hp = cloud.full_hp
            cloud.mp = cloud.full_mp
            sephiroth.hp = sephiroth.full_hp
            sephiroth.mp = sephiroth.full_mp
            cloud.hplost = 0
            sephiroth.hplost = 0
            end_announcment = 0

            turn = "player"

            screen_state = "menu"





    if highlight == "player":
        screen.blit(photo_border, (98, 48))

    if highlight == "computer":
        screen.blit(photo_border, (948, 48))

        # draw fighter images - in future should be done auto when selected
    cloud.draw()
    sephiroth.draw()

# function to draw panels and text
def draw_panels():
    # left
    screen.blit(panel, (50, 350))
    draw_text(f"{cloud.name}", font, white, 75, 365)
    draw_text(f"HP: {cloud.hp}/{cloud.full_hp}                  MP: {cloud.mp}", font, white, 75, 400)
    # right
    screen.blit(small_panel, (700, 350))
    draw_text(f"{sephiroth.name}", font, white, 725, 365)
    if sephiroth.hp >= 0:
        draw_text(f"HP: {sephiroth.hp}/{sephiroth.full_hp}                  MP: {sephiroth.mp}", font, white, 725, 400)
    elif sephiroth.hp < 0:
        draw_text(f"HP: 0/{sephiroth.full_hp}                               MP: {sephiroth.mp}", font, white, 725, 400)

# some values
end_announcment = 0

class soldier:
    def __init__(self, name, hp, mp, weapon, damage, spell1, spell2, weak, armour, limitbreak, image, image_x, image_y):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.full_hp = hp
        self.full_mp = mp
        self.weapon = weapon
        self.spell1 = spell1
        self.spell2 = spell2
        self.weapon_damage = damage
        self.weak_against = weak
        self.armour = armour
        self.hplost = 0
        self.limit_break = limitbreak
        self.has_scanned = False
        self.enemy_weakness = []
        self.image = pygame.image.load(image)
        self.image_x = image_x
        self.image_y = image_y


    def draw(self):
        screen.blit(self.image, (self.image_x, self.image_y)) # coordinate in function call?

    def attack(self, other):
        global screen_state
        global timer
        global message_for_turn
        global turn
        other.hp -= (self.weapon_damage - other.armour)
        other.hplost += (self.weapon_damage - other.armour)
        screen_state = "text screen"
        timer = pygame.time.get_ticks()
        message_for_turn = self.name + " attacks " + other.name + " causing " + str(self.weapon_damage - other.armour) + " damage!"
        turn = "computer"

    def castfire(self, other):
        global screen_state
        global timer
        global message_for_turn
        global turn

        if self.mp < 15:
            screen_state = "text screen"
            timer = pygame.time.get_ticks()
            message_for_turn = "not enough MP!"

        elif self.mp >= 15 and other.weak_against == "fire":
            other.hp -= 45
            other.hplost += 45
            self.mp -= 15
            screen_state = "text screen"
            timer = pygame.time.get_ticks()
            message_for_turn = self.name + " casts fire causing 45 damage!"
            turn = "computer"


        else:
            other.hp -= 35
            other.hplost += 35
            self.mp -= 15
            screen_state = "text screen"
            timer = pygame.time.get_ticks()
            message_for_turn = self.name + " casts fire causing 35 damage!"
            turn = "computer"

    def castlightning(self, other):
        global screen_state
        global timer
        global message_for_turn
        global turn

        if self.mp < 15:
            screen_state = "text screen"
            timer = pygame.time.get_ticks()
            message_for_turn = "not enough MP!"
        elif self.mp >= 15 and other.weak_against == "lightning":
            other.hp -= 45
            other.hplost += 45
            self.mp -= 15
            screen_state = "text screen"
            timer = pygame.time.get_ticks()
            message_for_turn = self.name + " casts lightning causing 45 damage!"
            turn = "computer"


        else:
            other.hp -= 35
            other.hplost += 35
            self.mp -= 15
            screen_state = "text screen"
            timer = pygame.time.get_ticks()
            message_for_turn = self.name + " casts lightning causing 35 damage!"
            turn = "computer"

    def scan(self, other):
        global screen_state
        global timer
        global message_for_turn
        global turn

        screen_state = "text screen"
        timer = pygame.time.get_ticks()
        message_for_turn = "{enemyname} is weak against {weak}.".format(enemyname=other.name,
                                                                        weak=other.weak_against)
        turn = "computer"



    def limitbreak(self, other):
        global screen_state
        global timer
        global message_for_turn
        global turn


        other.hp -= (70 - other.armour)
        other.hplost += (70 - other.armour)
        self.hplost = 0

        screen_state = "text screen"
        timer = pygame.time.get_ticks()
        message_for_turn = self.name + " attacks with " + str(self.limit_break) + " causing " \
                           + str(70 - other.armour) + " damage!"
        turn = "computer"



########### computer AI #################

    def computer(self):
        global screen_state
        global timer
        global message_for_turn
        global turn

        if (sephiroth.hp < 75) and (sephiroth.mp >= 20):
            x = random.randint(0, 1)
            if x == 0 and sephiroth.mp < 20:
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = "not enough MP!"

            elif x == 0 and sephiroth.mp >= 20 and sephiroth.hp >= (sephiroth.full_hp - 50):
                sephiroth.hp = sephiroth.full_hp
                sephiroth.mp -= 20
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " heals by " + str(sephiroth.full_hp - sephiroth.hp) + "!"
                turn = "player"

            elif x == 0 and sephiroth.mp >= 20:
                sephiroth.hp += 50
                sephiroth.mp -= 20
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " heals by 50!"
                turn = "player"

            elif x == 1:
                cloud.hp -= (sephiroth.weapon_damage - cloud.armour)
                cloud.hplost += (sephiroth.weapon_damage - cloud.armour)
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " attacks " + cloud.name + " causing " + str(
                    sephiroth.weapon_damage - cloud.armour) + " damage!"
                turn = "player"

        elif sephiroth.hplost >= (sephiroth.full_hp * 0.7):
            x = random.randint(0, 3)
            if x <= 2:
                cloud.hp -= (70 - cloud.armour)
                cloud.hplost += (70 - cloud.armour)
                sephiroth.hplost = 0

                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " attacks with " + str(sephiroth.limit_break) + " causing " \
                                   + str(70 - cloud.armour) + " damage!"
                turn = "player"

            elif x == 3:
                cloud.hp -= (sephiroth.weapon_damage - cloud.armour)
                cloud.hplost += (sephiroth.weapon_damage - cloud.armour)
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " attacks " + cloud.name + " causing " + str(
                    sephiroth.weapon_damage - cloud.armour) + " damage!"
                turn = "player"

        elif sephiroth.has_scanned == False:
            x = random.randint(0, 1)
            if x == 0:
                sephiroth.scan(cloud)
                sephiroth.enemy_weakness.append(cloud.weak_against)
                sephiroth.has_scanned = True
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = "{enemyname} is weak against {weak}.".format(enemyname=cloud.name,
                                                                                weak=cloud.weak_against)
                turn = "player"


            elif x == 1:
                cloud.hp -= (sephiroth.weapon_damage - cloud.armour)
                cloud.hplost += (sephiroth.weapon_damage - cloud.armour)
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " attacks " + cloud.name + " causing " + str(
                    sephiroth.weapon_damage - cloud.armour) + " damage!"
                turn = "player"

        elif ((sephiroth.spell1 == "poison") or (sephiroth.spell2 == "poison")) and (sephiroth.enemy_weakness[0] == "poison") and (sephiroth.mp >= 15):
            x = random.randint(0, 1)
            if x == 0:
                cloud.hp -= 45
                cloud.hplost += 45
                sephiroth.mp -= 15
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " casts poison causing 45 damage!"
                turn = "player"

            elif x == 1:
                cloud.hp -= (sephiroth.weapon_damage - cloud.armour)
                cloud.hplost += (sephiroth.weapon_damage - cloud.armour)
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " attacks " + cloud.name + " causing " + str(
                    sephiroth.weapon_damage - cloud.armour) + " damage!"
                turn = "player"

        elif sephiroth.mp >= 15:
            x = random.randint(0, 1)
            if x == 0:
                cloud.hp -= (sephiroth.weapon_damage - cloud.armour)
                cloud.hplost += (sephiroth.weapon_damage - cloud.armour)
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " attacks " + cloud.name + " causing " + str(
                    sephiroth.weapon_damage - cloud.armour) + " damage!"
                turn = "player"

            elif x == 1:
                cloud.hp -= (sephiroth.weapon_damage - cloud.armour)
                cloud.hplost += (sephiroth.weapon_damage - cloud.armour)
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " attacks " + cloud.name + " causing " + str(
                    sephiroth.weapon_damage - cloud.armour) + " damage!"
                turn = "player"

        else:
            cloud.hp -= (sephiroth.weapon_damage - cloud.armour)
            cloud.hplost += (sephiroth.weapon_damage - cloud.armour)
            screen_state = "text screen"
            timer = pygame.time.get_ticks()
            message_for_turn = sephiroth.name + " attacks " + cloud.name + " causing " + str(
                sephiroth.weapon_damage - cloud.armour) + " damage!"
            turn = "player"



########## computer AI end #################

    def game_over(self):
        global screen_state
        global timer
        global message_for_turn
        global turn
        global end_announcment

        if end_announcment == 0:
            if cloud.hp <= 0:
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = sephiroth.name + " wins!"
                turn = "game over"
                end_announcment += 1

            elif sephiroth.hp <= 0:
                screen_state = "text screen"
                timer = pygame.time.get_ticks()
                message_for_turn = cloud.name + " wins!"
                turn = "game over"
                end_announcment += 1














class health_bar():
    def __init__(self, x, y, hp, full_hp, mp, full_mp):
        self.x = x
        self.y = y
        self.hp = hp
        self.full_hp = full_hp
        self.mp = mp
        self.full_mp = full_mp

    def draw(self, hp):
        # update new hp value
        self.hp = hp
        # health ratio
        ratio = self.hp/self.full_hp
        # pygame.draw.rect(screen, red, (self.x, self.y, 150, 20)) not needed, replaced with health image
        # pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

        if self.hp >= 0:
            good_health_scaled = pygame.transform.scale(good_health,
                                                        (good_health.get_width() * ratio, good_health.get_height()))
        else:
            good_health_scaled = pygame.transform.scale(good_health,
                                                        (good_health.get_width() * 0, good_health.get_height()))



        screen.blit(bad_health, (self.x, self.y))
        screen.blit(good_health_scaled, (self.x, self.y))

    def draw_mp(self, mp):
        # update new hp value
        self.mp = mp
        # health ratio
        mp_ratio = self.mp / self.full_mp
        # pygame.draw.rect(screen, red, (self.x, self.y, 150, 20)) not needed, replaced with health image
        # pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

        if self.mp >= 0:
            good_mp_scaled = pygame.transform.scale(good_health, ((good_health.get_width() * 0.5) * mp_ratio, good_health.get_height()))
            bad_mp_scaled = pygame.transform.scale(bad_health, (good_health.get_width() * 0.5, good_health.get_height()))
        else:
            good_mp_scaled = pygame.transform.scale(good_health, ((good_health.get_width() * 0.5) * 0, good_health.get_height()))
            bad_mp_scaled = pygame.transform.scale(bad_health, (good_health.get_width() * 0.5, good_health.get_height()))




        screen.blit(bad_mp_scaled, (self.x, self.y))
        screen.blit(good_mp_scaled, (self.x, self.y))



# function to draw text
def  draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# buttons class
class button():
    def __init__(self, x, y, image, text):
        self.image = image
        self.rect = self.image.get_rect() # not sure of the use of this but ill leave it in, it also works other way
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.clicked = False
        self.button_text = text

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        screen.blit(self.image, ((self.rect.x), (self.rect.y)))

        # draw text as well...?
        draw_text(self.button_text, font, white, self.x + 10, self.y + 10)

        # return True or False
        return action


# create cloud instance
test_button = button(500, 200, fifty_button, "")
text_button = button(335, 75, long_button, "")
button_2 = button(75, 475, small_button, "Attack")
button_3 = button(75, 535, small_button, "Fire")
button_4 = button(75, 595, small_button, "Lightning")
button_5 = button(325, 475, small_button, "Scan")
button_6 = button(325, 535, small_button, "Limit break")
reset_button = button(540, 200, small_button, "  click to reset")
return_menu_button = button(540, 265, small_button, " return to menu")
button_start = button(725, 475, small_button, "click to begin")
button_exit = button(725, 540, small_button, "exit")

# create sephiroth instance
button_a = button(725, 475, small_button, "Attack")
button_b = button(725, 535, small_button, "Fire")
button_c = button(725, 595, small_button, "Lightning")
button_d = button(975, 475, small_button, "Scan")
button_e = button(975, 535, small_button, "Limit break")


# create character class instances
cloud = soldier("Cloud", 150, 100, "Buster Sword", 500, "fire", "lightning", "ice", 1, "Braver", 'cloud 250.jpg', 100, 50)
sephiroth = soldier("Sephiroth", 250, 25, "Masamune", 25, "poison", "heal", "poison", 1, "Storm", 'sephiroth 250.jpg', 950, 50)

# create health bars
cloud_health_bar = health_bar(75, 440, cloud.hp, cloud.full_hp, cloud.mp, cloud.full_mp)
sephiroth_health_bar = health_bar(725, 440, sephiroth.hp, sephiroth.full_hp, sephiroth.mp, sephiroth.full_mp)
cloud_mp_bar = health_bar(340, 440, cloud.hp, cloud.full_hp, cloud.mp, cloud.full_mp)
sephiroth_mp_bar = health_bar(990, 440, sephiroth.hp, sephiroth.full_hp, sephiroth.mp, sephiroth.full_mp)


# main game loop
game_running = True
while game_running:

    # create option to quit by pressing x button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # if turn == "computer":
    #     sephiroth.attack(cloud)
    #     turn = "player"

    current_time = pygame.time.get_ticks()
    if (current_time - timer > 2000) and (screen_state != "menu"):
        screen_state = "game"
        if turn == "player":
            highlight = "player"

            if (highlight == "player") and (count % 4 == 0) and (screen_state == "game"):
                draw_text(f"{cloud.name}", font, dark_white, 75, 365)
                count += 1
            else:
                count += 1



        if turn == "computer":
            highlight = "computer"

            if (highlight == "computer") and (count % 4 == 0) and (screen_state == "game"):
                draw_text(f"{sephiroth.name}", font, dark_white, 725, 365)
                count += 1
            else:
                count += 1




    if current_time - timer > 2500 and cloud.game_over() is True:
        turn = "restart"
        screen_state = "game"

    if current_time - timer > 4000 and turn == "computer":
        sephiroth.computer()
        turn = "player"


    # control fps
    clock.tick(fps)

    # get pygame to update screen as it runs
    pygame.display.update()

    # regulate screen state
    if screen_state == "menu":
        draw_menu_screen()

    if screen_state == "game":
        draw_game_background()

    if screen_state == "intro":
        draw_intro_screen()

    if screen_state == "text screen":
        action_screen()


    def print_message(text, font, text_col, x, y):
        global message
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    # countdown timers for HP and MP
    if cloud.hp == cloud.full_hp:
        cloud_current_hp = cloud.full_hp
    if (cloud.hp < cloud.full_hp) and (cloud_current_hp > cloud.hp):
        cloud_current_hp -= 3

    if sephiroth.hp == sephiroth.full_hp:
        sephiroth_current_hp = sephiroth.full_hp
    if (sephiroth.hp < sephiroth.full_hp) and (sephiroth_current_hp > sephiroth.hp):
        sephiroth_current_hp -= 3

    if cloud.mp == cloud.full_mp:
        cloud_current_mp = cloud.full_mp
    if (cloud.mp < cloud.full_mp) and (cloud_current_mp > cloud.mp):
        cloud_current_mp -= 1

    if sephiroth.mp == sephiroth.full_mp:
        sephiroth_current_mp = sephiroth.full_mp
    if (sephiroth.mp < sephiroth.full_mp) and (sephiroth_current_mp > sephiroth.mp):
        sephiroth_current_mp -= 1






    #
    # if cloud.hp < cloud_current_hp:
    #     cloud_current_hp -= 1


pygame.quit()
















