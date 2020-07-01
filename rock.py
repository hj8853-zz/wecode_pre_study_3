import random
import pygame

Window_width = 480
Window_height = 640

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
        # rock이라는 class가 호출 될 때마다 랜덤으로 이미지 불러옴
        self.image = pygame.image.load(random.choice(rock_images))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def out_out_screen(self):
        if self.rect.y > Window_height:
            return True