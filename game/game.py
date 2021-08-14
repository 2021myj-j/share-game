import pyxel
from obstacle import ObstacleList

WINDOW_H = 208
WINDOW_W = 112
mario_H = 16
mario_W = 16
MAP_H = 2048
MAP_W = 112
INGAME_COUNT = 5


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cat:
    def __init__(self, img_id, speed):
        self.pos = Vec2(48, 176)
        self.vec = 0
        self.img_mario = img_id
        self.speed = speed

    def update(self, x, y):
        """
        プレイヤーのベクトルを更新
        """
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
    def __init__(self):
        self.PLAYER_IMG_ID = 1
        self.TILEMAP_ID = 0

        pyxel.init(WINDOW_W, WINDOW_H, caption="Cat Game")
        pyxel.load("assets2.pyxres")

        # make instance
        self.player = Cat(self.PLAYER_IMG_ID, mario_W)
        self.maps = [
            Map(self.TILEMAP_ID, -MAP_H + WINDOW_H),
            Map(self.TILEMAP_ID, -MAP_H * 2 + WINDOW_H)
        ]
        self.collisions = [Collision([]), Collision([])]
        self.obstacle_lists = ObstacleList.obstacle_lists

        pyxel.run(self.update, self.draw)

    def update(self):
        """
        プレイヤーとマップを動かす
        """
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # ====== ctrl Cat ======
        if pyxel.btnp(pyxel.KEY_A):
            self.player.vec = 1
            self.player.update(self.player.pos.x -
                               self.player.speed, self.player.pos.y)
            if self.player.pos.x < 0:
                self.player.update(0, self.player.pos.y)
        elif pyxel.btnp(pyxel.KEY_D):
            self.player.vec = 0
            self.player.update(self.player.pos.x + self.player.speed, self.player.pos.y)
            if self.player.pos.x + mario_W > WINDOW_W:
                self.player.update(WINDOW_W - mario_W, self.player.pos.y)

        # ====== crtl Map ======
        if pyxel.frame_count % INGAME_COUNT == 0:
            for map in self.maps:
                if map.pos.y < WINDOW_H:
                    map.update(map.pos.x, map.pos.y + map.speed)
                else:
                    map.update(map.pos.x, map.pos.y - MAP_H * 2 + map.speed)

        # ====== ctrl Obstacle ======

        if pyxel.frame_count % INGAME_COUNT == 0:
            index = int(pyxel.frame_count /
                        INGAME_COUNT) % len(self.obstacle_lists)
            self.collisions[0].update(
                self.obstacle_lists[index])
            self.collisions[1].update(
                self.obstacle_lists[index - 1])

    def draw(self):
        pyxel.cls(0)

        # ====== draw Map ======
        for map in self.maps:
            pyxel.bltm(map.pos.x, map.pos.y, map.tilemap, 0, 0, MAP_W, MAP_H, 13)
        # ====== draw Cat ======
        if pyxel.btnp(pyxel.KEY_A):
            self.player.vec = 1

        # ====== draw Cat ======
        elif pyxel.btnp(pyxel.KEY_D):
            self.player.vec = 0

        else:
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


if __name__ == "__main__":
    App()
