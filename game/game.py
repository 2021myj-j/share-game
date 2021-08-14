import pyxel

WINDOW_H = 208
WINDOW_W = 112
mario_H = 16
mario_W = 16
MAP_H = 2048
MAP_W = 112


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
        self.pos.x = x
        self.pos.y = y


class Map:
    def __init__(self, tilemap_id, default_y, speed=32):
        self.pos = Vec2(0, default_y)
        self.tilemap = tilemap_id
        self.speed = speed
        self.default_y = default_y

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y


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

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # ====== ctrl Cat ======
        if pyxel.btnp(pyxel.KEY_A):
            self.player.update(self.player.pos.x - self.player.speed, self.player.pos.y)
            if self.player.pos.x < 0:
                self.player.update(0, self.player.pos.y)
        elif pyxel.btnp(pyxel.KEY_D):
            self.player.update(self.player.pos.x + self.player.speed, self.player.pos.y)
            if self.player.pos.x + mario_W > WINDOW_W:
                self.player.update(WINDOW_W - mario_W, self.player.pos.y)

        # ====== crtl Map ======
        if pyxel.frame_count % 5 == 0:
            for map in self.maps:
                if map.pos.y < WINDOW_H:
                    map.update(map.pos.x, map.pos.y + map.speed)
                else:
                    map.update(map.pos.x, map.pos.y - MAP_H * 2 + map.speed)

    def draw(self):
        pyxel.cls(0)

        # ====== draw Map ======

        for map in self.maps:
            pyxel.bltm(map.pos.x, map.pos.y, map.tilemap, 0, 0, MAP_W, MAP_H, 13)
        # ====== draw Cat ======
        if pyxel.btnp(pyxel.KEY_A):
            self.player.vec = 1

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


if __name__ == "__main__":
    App()
