import pygame

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
        if self.rect.y + self.rect.height < 0:  # 미사일 화면 밖으로 나가면 없애주자
            self.kill()

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite