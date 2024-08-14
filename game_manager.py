import pygame
from player import Player
from wall import Wall
from star import Star
from target import Target
from utils.colided import collided_rect, collided_cricle
import os


class GameManager:
    def __init__(self, screen, level=1):
        self.screen = screen
        self.level = level
        self.player = None
        self.walls = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.stars_count = 0
        self.targets = pygame.sprite.Group()
        self.stars_sound = pygame.mixer.Sound('static/sound/eat_stars.wav')
        self.stars_sound.set_volume(0.3)
        self.targets_sound = pygame.mixer.Sound('static/sound/success.wav')
        self.targets_sound.set_volume(0.3)
        self.load()

    def load_starts(self, starts):
        self.stars.empty()
        for x, y in starts:
            stars = Star(x, y)
            stars.add(self.stars)

    def load_targets(self, targets):
        self.targets.empty()
        for x, y in targets:
            target = Target(x, y)
            target.add(self.targets)

    def load_walls(self, walls):
        self.walls.empty()
        for x, y, width, height in walls:
            wall = Wall(x, y, width, height)
            wall.add(self.walls)

    def load_player(self, center_x, center_y, forward_angle):
        if self.player:
            self.player.kill()
        self.player = Player(center_x, center_y, forward_angle)

    def load(self):
        with open("static/maps/level%d.txt" % self.level, 'r') as fin:

            walls_cnt = int(fin.readline())
            walls = []
            for i in range(walls_cnt):
                x, y, width, height = map(int, fin.readline().split())
                walls.append((x, y, width, height))
            self.load_walls(walls)
            self.stars_count = int(fin.readline())

            stars = []
            for i in range(self.stars_count):
                x, y = map(int, fin.readline().split())
                stars.append((x, y))
            self.load_starts(stars)

            targets_cnt = int(fin.readline())
            targets = []
            for i in range(targets_cnt):
                x, y = map(int, fin.readline().split())
                targets.append((x, y))
            self.load_targets(targets)

            center_x, center_y, forward_angle = map(int, fin.readline().split())
            self.load_player(center_x, center_y, forward_angle)

    def next_level(self):
        self.level += 1
        if not os.path.isfile("static/maps/level%d.txt" % self.level):
            return False
        self.load()
        return True

    def check_collide(self):
        if pygame.sprite.spritecollide(self.player, self.walls, False, collided_rect):
            self.player.crash()
        if pygame.sprite.spritecollide(self.player, self.stars, True, collided_cricle):
            self.stars_sound.play()
            self.stars_count -= 1
        if self.stars_count == 0:
            if pygame.sprite.spritecollide(self.player, self.targets, True, collided_rect):
                self.targets_sound.play()
                return True
        return False

    def update(self):
        self.stars.update()
        self.stars.draw(self.screen)
        self.targets.update()
        self.targets.draw(self.screen)

        self.player.update()
        success = self.check_collide()
        self.screen.blit(self.player.image, self.player.rect)

        self.walls.update()
        self.walls.draw(self.screen)
        return success

