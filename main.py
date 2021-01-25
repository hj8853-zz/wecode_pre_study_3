import random, pygame, player, missile, rock
from time import sleep
from pygame.locals import *

Window_width = 480 
Window_height = 640 

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 250, 250)
RED = (250, 50, 50)
BRIGHT_RED = (250, 100, 100)
GREEN = (50, 250, 50)
BRIGHT_GREEN = (100, 250, 100)

FPS = 60

def draw_text(text, font, surface, x, y, main_color):
    text_object = font.render(text, True, main_color)
    text_rect = text_object.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_object, text_rect)


def occur_explosion(surface, x, y):
    explosion_image = pygame.image.load("./images/explosion.png")
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    explosion_sounds = ("./sounds/explosion01.wav", "./sounds/explosion02.wav",
                        "./sounds/explosion03.wav", "./sounds/explosion04.wav")
    explosion_sound = pygame.mixer.Sound(random.choice(explosion_sounds))
    explosion_sound.play()

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pause = False


def paused():
    draw_x = int(Window_width / 2)
    draw_y = int(Window_height / 4)
    font_60 = pygame.font.Font("./fonts/Nanumgothic.ttf", 60)
    

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        background_image = pygame.image.load("./images/background.png")
        screen.blit(background_image, background_image.get_rect())
        button("Continue", Window_width - 450, draw_y + 300, 100, 50, GREEN, BRIGHT_GREEN, unpause)
        button("Quit", Window_width - 130, draw_y + 300, 100, 50, RED, BRIGHT_RED, quitgame)
        draw_text("Paused", font_60, screen, draw_x, draw_y / 2, WHITE)

        pygame.display.update()
        clocks = pygame.time.Clock()
        clocks.tick(FPS)


def game_loop():
    global pause

    default_font = pygame.font.Font("./fonts/NanumGothic.ttf", 28)
    background_image = pygame.image.load("./images/background.png")
    gameover_sound = pygame.mixer.Sound("./sounds/gameover.wav")
    pygame.mixer.music.load("./sounds/music.wav")
    pygame.mixer.music.play(-1)  # 무한반복
    fps_clock = pygame.time.Clock()

    players = player.Player()
    missile_group = pygame.sprite.Group()
    rock_group = pygame.sprite.Group()

    occur_prob = 40
    shot_count = 0
    count_missed = 0

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    players.dx -= 5
                elif event.key == pygame.K_RIGHT:
                    players.dx += 5
                elif event.key == pygame.K_UP:
                    players.dy -= 5
                elif event.key == pygame.K_DOWN:
                    players.dy += 5
                elif event.key == pygame.K_SPACE:
                    missiles = missile.Missile(players.rect.centerx, players.rect.y, 10)
                    missiles.launch()
                    missile_group.add(missiles)
                elif event.key == pygame.K_p:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    players.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    players.dy = 0

        screen.blit(background_image, background_image.get_rect())

        occur_of_rocks = 1 + int(shot_count / 300)
        min_rock_speed = 1 + int(shot_count / 200)
        max_rock_speed = 1 + int(shot_count / 100)

        if random.randint(1, occur_prob) == 1:
            for i in range(occur_of_rocks):
                speed = random.randint(min_rock_speed, max_rock_speed)
                rocks = rock.Rock(random.randint(0, Window_width - 30), 0, speed)
                rock_group.add(rocks)

        draw_text("파괴한 운석: {}".format(shot_count),
                  default_font, screen, 100, 20, YELLOW)
        draw_text("놓친 운석: {}".format(count_missed),
                  default_font, screen, 400, 20, RED)

        for missiles in missile_group:
            rocks = missiles.collide(rock_group)  # 미사일과 운석이 충돌한 경우
            if rocks:
                missiles.kill()
                rocks.kill()
                occur_explosion(screen, rocks.rect.x, rocks.rect.y)
                shot_count += 1

        for rocks in rock_group:
            if rocks.out_out_screen():  # 운석이 화면 밖으로 나간 경우
                rocks.kill()
                count_missed += 1

        rock_group.update()
        rock_group.draw(screen)
        missile_group.update()
        missile_group.draw(screen)
        players.update()
        players.draw(screen)
        pygame.display.flip()

        # 게임 종료 조건
        if players.collide(rock_group) or count_missed >= 3:
            pygame.mixer_music.stop()
            occur_explosion(screen, players.rect.x, players.rect.y)
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done = True

        fps_clock.tick(FPS)

    return "game_menu"


def game_menu():
    start_image = pygame.image.load("./images/background.png")
    screen.blit(start_image, [0, 0])
    draw_x = int(Window_width / 2)
    draw_y = int(Window_height / 4)
    font_60 = pygame.font.Font("./fonts/Nanumgothic.ttf", 60)
    font_40 = pygame.font.Font("./fonts/Nanumgothic.ttf", 40)

    draw_text("운석을 파괴해라!", font_60, screen, draw_x, draw_y, YELLOW)
    draw_text("엔터키를 누르면", font_40, screen, draw_x, draw_y + 200, WHITE)
    draw_text("게임이 시작됩니다.", font_40, screen, draw_x, draw_y + 250, WHITE)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "play"
        if event.type == QUIT:
            return "quit"
    return "game_menu"


def main():
    global screen
    
    pygame.init()
    screen = pygame.display.set_mode((Window_width, Window_height))
    pygame.display.set_caption("We Shooting")

    action = "game_menu"
    while action != "quit":
        if action == "game_menu":
            action = game_menu()
        elif action == "play":
            action = game_loop()

    pygame.quit()


if __name__ == "__main__":
    main()
