

from random import randint, random
import pyxel
from game.obstacle import ObstacleList

WINDOW_H = 208
WINDOW_W = 112
mario_H = 16
mario_W = 16
MAP_H = 2048
MAP_W = 112
ENEMY_H = 8
ENEMY_W = 8
INGAME_COUNT = 15


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player:
    def __init__(self, img_id, speed, life=3):

        self.pos = Vec2(48, 176)
        self.vec = 0
        self.img_mario = img_id
        self.speed = speed
        self.life = life
        self.a_pressed = False
        self.d_pressed = False
        self.y_pressed = False
        self.is_invincible = False
        self.inv_start_frame = 0

    def update(self, x, y):
        """
        プレイヤーのベクトルを更新
        """
        self.pos.x = x
        self.pos.y = y


class Enemy_kuri:
    def __init__(self, img_id, speed, x, y):

        self.pos = Vec2(x, y)
        self.vec = 0
        self.img_enemy = img_id
        self.speed = speed
        self.default_y = y

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y


class Enemy_koura:
    def __init__(self, img_id, speed, x, y):

        self.pos = Vec2(x, y)
        self.vec = 0
        self.img_enemy = img_id
        self.x_speed = speed
        self.y_speed = speed
        self.default_x = x
        self.default_y = y

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y


class Map:
    def __init__(self, tilemap_id, default_y, speed=8):

        self.pos = Vec2(0, default_y)
        self.tilemap = tilemap_id
        self.speed = speed
        self.default_y = default_y

    def update(self, x, y):
        """
        マップのベクトルを更新
        """
        self.pos.x = x
        self.pos.y = y


class Collision:
    def __init__(self, obstacle_list):
        self.obstacle_list = obstacle_list

    def update(self, obstacle_list):
        """
        マップの衝突判定を更新
        """
        self.obstacle_list = obstacle_list


class App:
    def __init__(self, debug_mode=False):
        self.PLAYER_IMG_ID = 1
        self.TILEMAP_ID = 0
        self.count_amari = False
        self.start_count = 1800
        self.debug_mode = debug_mode


        # make instance
        if self.debug_mode:
            self.player = Player(self.PLAYER_IMG_ID, mario_W, 9999999)
        else:
            self.player = Player(self.PLAYER_IMG_ID, mario_W)
        self.Enemies = [
        Enemy_kuri(self.PLAYER_IMG_ID, 0.8, randint(0, 70), randint(-150, -50)),
        Enemy_kuri(self.PLAYER_IMG_ID, 0.9, randint(10, 80), randint(-350, -100)),
        Enemy_kuri(self.PLAYER_IMG_ID, 1, randint(20, 90), randint(-600, -300)),
        Enemy_kuri(self.PLAYER_IMG_ID, 1.1, randint(30, 100), randint(-700, -500))
        ]

        self.enemy2 = Enemy_koura(self.PLAYER_IMG_ID, 1.2, randint(0, 100), randint(-1000, -500))
        self.maps = [
        Map(self.TILEMAP_ID, -MAP_H + WINDOW_H),
        Map(self.TILEMAP_ID, -MAP_H * 2 + WINDOW_H)
        ]


        self.collisions = [Collision([]), Collision([])]
        self.obstacle_lists = ObstacleList.obstacle_lists

        pyxel.init(WINDOW_W, WINDOW_H, caption="Share Game")
        pyxel.load("assets2.pyxres")
        
        self.start_flag = 1
        self.playing_flag = 0
        self.game_over_flag = 0

        
        pyxel.run(self.update, self.draw)




    def update(self):
        if self.start_flag == 1:

            if pyxel.btnp(pyxel.KEY_Y):
                self.player.y_pressed = True

            if self.player.y_pressed:
                self.count_amari = True
                self.player.y_pressed = False

            if self.count_amari == True:
                if pyxel.frame_count % INGAME_COUNT == 0:
                    self.start_count = pyxel.frame_count
                    self.count_amari = False

            if pyxel.frame_count - self.start_count >= 90:
                    self.start_count = pyxel.frame_count
                    self.start_flag = 0
                    self.playing_flag = 1



        """
        プレイヤーとマップを動かす
        """
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.playing_flag == 1:
            # ====== ctrl Player ======
            if pyxel.btnp(pyxel.KEY_A):
                self.player.a_pressed = True
            if pyxel.btnp(pyxel.KEY_D):
                self.player.d_pressed = True

            if self.player.a_pressed:
                self.player.vec = 1
                self.player.update(
                    self.player.pos.x - self.player.speed,
                    self.player.pos.y
                )   # yapf: disable
                if self.player.pos.x < 0:
                    self.player.update(0, self.player.pos.y)
                self.player.a_pressed = False
            elif self.player.d_pressed:
                self.player.vec = 0
                self.player.update(self.player.pos.x +
                                self.player.speed, self.player.pos.y)
                if self.player.pos.x + mario_W > WINDOW_W:
                    self.player.update(WINDOW_W - mario_W, self.player.pos.y)
                self.player.d_pressed = False

            # ====== ctrl Enemy ======

            for enemy in self.Enemies:
                enemy.update(enemy.pos.x, enemy.pos.y + enemy.speed)
                if enemy.pos.y >= WINDOW_H - ENEMY_H:
                    enemy.pos.y = enemy.default_y - 256

            self.enemy2.update(
                self.enemy2.pos.x + self.enemy2.x_speed,
                self.enemy2.pos.y + self.enemy2.y_speed
            )

            if self.enemy2.pos.x >= WINDOW_W - ENEMY_W or self.enemy2.pos.x <= 0:
                self.enemy2.x_speed = -self.enemy2.x_speed

            if self.enemy2.pos.y >= WINDOW_H:
                self.enemy2.pos.y = self.enemy2.default_y - 200

            # ====== ctrl Enemy ======

            for enemy in self.Enemies:
                enemy.update(enemy.pos.x, enemy.pos.y + enemy.speed)
                if enemy.pos.y >= WINDOW_H - ENEMY_H:
                    enemy.pos.y = enemy.default_y - randint(100, 300)

            self.enemy2.update(
                self.enemy2.pos.x + self.enemy2.x_speed,
                self.enemy2.pos.y + self.enemy2.y_speed
            )

            if self.enemy2.pos.x >= WINDOW_W - ENEMY_W or self.enemy2.pos.x <= 0:
                self.enemy2.x_speed = -self.enemy2.x_speed

            if self.enemy2.pos.y >= WINDOW_H:
                self.enemy2.pos.y = self.enemy2.default_y - randint(200, 500)

            # ====== Enemy Collision ======
            enemy_count = len(self.Enemies)
            for i in range(enemy_count):
                # 当たり判定(クリボーとマリオ)
                if ((self.player.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                    and (self.Enemies[i].pos.x + ENEMY_W < self.player.pos.x + mario_W)
                    and (self.player.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                    and (self.Enemies[i].pos.y + ENEMY_H < self.player.pos.y + mario_H) 
                    or (self.player.pos.x < self.Enemies[i].pos.x)
                    and (self.Enemies[i].pos.x < self.player.pos.x + mario_W)
                    and (self.player.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                    and (self.Enemies[i].pos.y + ENEMY_H < self.player.pos.y + mario_H)
                    or (self.player.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                    and (self.Enemies[i].pos.x + ENEMY_W < self.player.pos.x + mario_W)
                    and (self.player.pos.y < self.Enemies[i].pos.y)
                    and (self.Enemies[i].pos.y < self.player.pos.y + mario_H)
                    or (self.player.pos.x < self.Enemies[i].pos.x)
                    and (self.Enemies[i].pos.x < self.player.pos.x + mario_W)
                    and (self.player.pos.y < self.Enemies[i].pos.y)
                    and (self.Enemies[i].pos.y < self.player.pos.y + mario_H)):

                    self.damage()

            # 当たり判定(こうらとマリオ)
            if ((self.player.pos.x < self.enemy2.pos.x + ENEMY_W)
                and (self.enemy2.pos.x + ENEMY_W < self.player.pos.x + mario_W)
                and (self.player.pos.y < self.enemy2.pos.y + ENEMY_H)
                and (self.enemy2.pos.y + ENEMY_H < self.player.pos.y + mario_H) 
                or (self.player.pos.x < self.enemy2.pos.x)
                and (self.enemy2.pos.x < self.player.pos.x + mario_W)
                and (self.player.pos.y < self.enemy2.pos.y + ENEMY_H)
                and (self.enemy2.pos.y + ENEMY_H < self.player.pos.y + mario_H)
                or (self.player.pos.x < self.enemy2.pos.x + ENEMY_W)
                and (self.enemy2.pos.x + ENEMY_W < self.player.pos.x + mario_W)
                and (self.player.pos.y < self.enemy2.pos.y)
                and (self.enemy2.pos.y < self.player.pos.y + mario_H)
                or (self.player.pos.x < self.enemy2.pos.x)
                and (self.enemy2.pos.x < self.player.pos.x + mario_W)
                and (self.player.pos.y < self.enemy2.pos.y)
                and (self.enemy2.pos.y < self.player.pos.y + mario_H)):

                    self.damage()


            # ====== crtl Map ======
            if pyxel.frame_count % INGAME_COUNT == 0:
                for map in self.maps:
                    if map.pos.y < WINDOW_H:
                        map.update(map.pos.x, map.pos.y + map.speed)
                    else:
                        map.update(map.pos.x, map.pos.y - MAP_H * 2 + map.speed)

            # ====== ctrl Obstacle ======
            if pyxel.frame_count % INGAME_COUNT == 0:
                index = int((pyxel.frame_count - self.start_count) /
                            INGAME_COUNT) % len(self.obstacle_lists)

                for i, collision in enumerate(self.collisions):
                    collision.update(self.obstacle_lists[index - i])
                    for i, obstacle in enumerate(collision.obstacle_list):
                        if obstacle:
                            if (i - 1) * 8 <= self.player.pos.x <= i * 8:
                                self.damage()

    def damage(self):
        if not self.player.is_invincible:
            self.player.is_invincible = True
            self.player.inv_start_frame = pyxel.frame_count
            self.player.life -= 1
        else:
            if pyxel.frame_count - self.player.inv_start_frame > 60:
                self.player.is_invincible = False

    def draw(self):
        pyxel.cls(0)
        if self.playing_flag == 1:
            # ====== draw Map ======
            for map in self.maps:
                pyxel.bltm(map.pos.x, map.pos.y, map.tilemap, 0, 0, MAP_W, MAP_H, 13)

            # ====== draw Player ======
            if self.player.vec == 1:
                pyxel.blt(
                    self.player.pos.x, self.player.pos.y,
                    self.player.img_mario, 0, 24, -mario_W, mario_H, 0)
            else:
                pyxel.blt(
                    self.player.pos.x, self.player.pos.y,
                    self.player.img_mario, 0, 24, mario_W, mario_H, 0)


            # ====== draw Collision ======
            # デバッグ用に当たり判定可視化
            for i, obstacle in enumerate(self.collisions[0].obstacle_list):
                if obstacle:
                    pyxel.rect(i * 8, WINDOW_H - 32, 8, 8, 8)
            for i, obstacle in enumerate(self.collisions[1].obstacle_list):
                if obstacle:
                    pyxel.rect(i * 8, WINDOW_H - 24, 8, 8, 8)

            # ====== draw Enemy ======

            for enemy in self.Enemies:

                pyxel.blt(
                    enemy.pos.x, enemy.pos.y, enemy.img_enemy, 16, 24, ENEMY_W, ENEMY_H, 7
                )

            pyxel.blt(
                self.enemy2.pos.x, self.enemy2.pos.y, self.enemy2.img_enemy, 24, 32, ENEMY_W,
                ENEMY_H, 7
            )

            pyxel.rect(8, 8, 60, 16, 0)

            pyxel.text(13, 14, "LIFE: " + str(self.player.life), 7)

            if self.player.life < 1:
                self.game_over()

        if self.start_flag == 1:
            pyxel.cls(0)
            pyxel.text(35, 50, "Share Game!", pyxel.frame_count % 16)
            pyxel.text(35, 80, "Game Start", 8)
            
            if 0 < pyxel.frame_count - self.start_count < 90:
                if 0 < pyxel.frame_count - self.start_count < 30:
                    pyxel.text(55, 120, "3", 8)
                if 30 < pyxel.frame_count - self.start_count < 60:
                    pyxel.text(55, 120, "2", 8)
                if 60 < pyxel.frame_count - self.start_count < 90:
                    pyxel.text(55, 120, "1", 8)

    def game_over(self):
        pyxel.cls(0)
        pyxel.text(37, 100, "GAME OVER", 8)
        self.playing_flag == 0
        self.game_over_flag == 1


if __name__ == "__main__":

    App(debug_mode=True)