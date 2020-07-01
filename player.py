import pygame

Window_width = 480
Window_height = 640

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("./images/fighter.png")
        self.rect = self.image.get_rect()  # 그림의 현재 위치
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