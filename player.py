import pygame
import config
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, forward_angle):
        super().__init__()
        self.width = 100
        self.height = 50
        self.forward_angle = forward_angle
        self.image = pygame.Surface([self.width, self.height])
        self.image_source = pygame.image.load("static/images/car.png").convert()
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        self.image.set_colorkey("black")

        self.rect = self.image.get_rect()
        self.rect.center = (center_x / 2, center_y / 2)

        self.last_time = pygame.time.get_ticks()  # 当前时间，ms
        self.delta_time = 0  # 两帧 之间的间隔

        self.move_v_limit = 220
        self.move_v = 0
        self.move_f = 0.95
        self.move_a = 600
        self.rotate_v = 0
        self.rotate_v_limit = 140

        self.crash_sound = pygame.mixer.Sound("static/sound/crash.mp3")
        self.crash_sound.set_volume(0.1)
        self.move_sound = pygame.mixer.Sound("static/sound/move.mp3")
        self.move_sound.set_volume(0.1)

        self.move_voice_channel = pygame.mixer.Channel(7)

    def update_delta_time(self):
        current_time = pygame.time.get_ticks()
        self.delta_time = (current_time - self.last_time) / 1000
        self.last_time = current_time

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move_v += self.move_a * self.delta_time
            self.move_v = min(self.move_v_limit, self.move_v)

            if not self.move_voice_channel.get_busy():
                self.move_voice_channel.play(self.move_sound)
        elif keys[pygame.K_s]:
            self.move_v -= self.move_a * self.delta_time
            self.move_v = max(-self.move_v_limit, self.move_v)

            if not self.move_voice_channel.get_busy():
                self.move_voice_channel.play(self.move_sound)
        else:
            self.move_v = int(self.move_v * self.move_f)
            if self.move_voice_channel.get_busy():
                self.move_voice_channel.stop()
        sign = 1
        if self.move_v < 0:
            sign = -1

        if keys[pygame.K_a]:
            self.rotate_v = -self.rotate_v_limit * sign
        elif keys[pygame.K_d]:
            self.rotate_v = self.rotate_v_limit * sign
        else:
            self.rotate_v = 0

    def rotate(self, direction=1):
        self.forward_angle += self.rotate_v * self.delta_time * direction
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        self.image.set_colorkey("black")
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, direction=1):
        if direction == 1 and abs(self.move_v) > 50:
            self.rotate(direction)  # 原地打方向盘，车身不动
        vx = self.move_v * math.cos(math.pi * self.forward_angle / 180) * direction
        vy = self.move_v * math.sin(math.pi * self.forward_angle / 180) * direction
        self.rect.x += vx * self.delta_time
        self.rect.y += vy * self.delta_time
        if direction == -1 and abs(self.move_v) > 50:
            self.rotate(direction)  # 原地打方向盘，车身不动

    def crash(self):
        self.crash_sound.play()
        self.move(-1)
        if self.move_v >= 0:
            self.move_v = min(-self.move_v, -100)
        else :
            self.move_v = max(self.move_v, 100)
        self.rotate_v *= -1

    def update(self, direction=1):
        self.update_delta_time()
        self.input()
        self.move(direction)
