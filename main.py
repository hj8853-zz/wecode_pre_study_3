import random, pygame
from time import sleep
from pygame.locals import *

Window_width = 480
Window_height = 640

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 250, 250)
RED = (250, 50, 50)

FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("./images/fighter.png")
        self.rect = self.image.get_rect() # 그림의 현재 위치
        self.rect.x = int(Window_width / 2)
        self.rect.y = Window_height - self.rect.height
        self.dx = 0
        self.dy = 0

    # 업데이트
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 화면 밖으로 플레이어 캐릭터가 나가지 않도록
        if self.rect.x < 0 or self.rect.x + self.rect.width > Window_width:
            self.rect.x -= self.dx

        if self.rect.y < 0 or self.rect.y + self.rect.height > Window_height:
            self.rect.y -= self.dy

    # 그려주는 부분
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    
    # 충돌일어났을 경우
    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


class Missile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, speed):
        super(Missile, self).__init__()
        self.image = pygame.image.load("./images/missile.png")
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed = speed
        self.sound = pygame.mixer.Sound("./sounds/missile.wav")


    # 소리 들리도록
    def launch(self):
        self.sound.play()

    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0: # 미사일 화면 밖으로 나가면 없애주자
            self.kill()
        

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


    
class Rock(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, speed):
        super(Rock, self).__init__()
        rock_images = (
            "./images/rock01.png", "./images/rock02.png", "./images/rock03.png", "./images/rock04.png", "./images/rock05.png",
            "./images/rock06.png", "./images/rock07.png", "./images/rock08.png", "./images/rock09.png", "./images/rock10.png",
            "./images/rock11.png", "./images/rock12.png", "./images/rock13.png", "./images/rock14.png", "./images/rock15.png",
            "./images/rock16.png", "./images/rock17.png", "./images/rock18.png", "./images/rock19.png", "./images/rock20.png",
            "./images/rock21.png", "./images/rock22.png", "./images/rock23.png", "./images/rock24.png", "./images/rock25.png",
            "./images/rock26.png", "./images/rock27.png", "./images/rock28.png", "./images/rock29.png", "./images/rock30.png",
        )
        self.image = pygame.image.load(random.choice(rock_images)) # rock이라는 class가 호출 될 때마다 랜덤으로 이미지 불러옴
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed = speed

        
    def update(self):
        self.rect.y += self.speed


    def out_out_screen(self):
        if self.rect.y > Window_height:
            return True


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

    explosion_sounds = ("./sounds/explosion01.wav", "./sounds/explosion02.wav", "./sounds/explosion03.wav", "./sounds/explosion04.wav")
    explosion_sound = pygame.mixer.Sound(random.choice(explosion_sounds))
    explosion_sound.play()


def game_loop():
    default_font = pygame.font.Font("./fonts/NanumGothic.ttf", 28)
    background_image = pygame.image.load("./images/background.png")
    gameover_sound = pygame.mixer.Sound("./sounds/gameover.wav")
    pygame.mixer.music.load("./sounds/music.wav")
    pygame.mixer.music.play(-1) # 무한반복
    fps_clock = pygame.time.Clock()

    player = Player()
    missiles = pygame.sprite.Group()
    rocks = pygame.sprite.Group()

    occur_prob = 40
    shot_count = 0
    count_missed = 0

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.dx -= 5
                elif event.key == pygame.K_RIGHT:
                    player.dx += 5
                elif event.key == pygame.K_UP:
                    player.dy -= 5
                elif event.key == pygame.K_DOWN:
                    player.dy += 5
                elif event.key == pygame.K_SPACE:
                    missile = Missile(player.rect.centerx, player.rect.y, 10)
                    missile.launch()
                    missiles.add(missile)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.dy = 0

        screen.blit(background_image, background_image.get_rect())

        occur_of_rocks = 1 + int(shot_count / 300)
        min_rock_speed = 1 + int(shot_count / 200)
        max_rock_speed = 1 + int(shot_count / 100)

        if random.randint(1, occur_prob) == 1:
            for i in range(occur_of_rocks):
                speed = random.randint(min_rock_speed, max_rock_speed)
                rock = Rock(random.randint(0, Window_width - 30), 0, speed)
                rocks.add(rock)

        draw_text("파괴한 운석: {}".format(shot_count), default_font, screen, 100, 20, YELLOW)
        draw_text("놓친 운석: {}".format(count_missed), default_font, screen, 400, 20, RED)

        for missile in missiles:
            rock = missile.collide(rocks) # 미사일과 운석이 충돌한 경우
            if rock:
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y)
                shot_count += 1

        for rock in rocks:
            if rock.out_out_screen(): #운석이 화면 밖으로 나간 경우
                rock.kill()
                count_missed += 1

        rocks.update()
        rocks.draw(screen)
        missiles.update()
        missiles.draw(screen)
        player.update()
        player.draw(screen)
        pygame.display.flip()

        # 게임 종료 조건
        if player.collide(rocks)  or count_missed >= 3:
            pygame.mixer_music.stop()
            occur_explosion(screen, player.rect.x, player.rect.y)
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