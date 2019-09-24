screenX, screenY = 1024, 1024
validKeys = [65, 68, 37, 39]


class Paddle():
    w, h = 128, 32
    speed = 8
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def move(self, dir):
        if (collisions().get("paddle") != dir):
            i = 0
            while i < self.speed and "paddle" not in collisions():
                i += 1
                self.x += 1 if dir == "right" else -1
    
    def display(self):
        fill(0, 150, 255)
        rect(self.x, self.y, self.w, self.h)


class Ball():
    def __init__(self, x, y):
        self.x, self.y = x, y


class Brick():
    def __init__(self, x, y):
        self.x, self.y = x, y


def collisions():
    colliding = {}
    # paddle screen side collision
    if (paddle.x == 0):
        colliding["player"] = "left"
    if (paddle.x + paddle.w == screenX):
        colliding["player"] = "right"
    return colliding


def convertKey(n):
    return "left" if n == 65 or n == 37 else \
        "right" if n == 68 or n == 39 else None

def setup():
    global paddle, keysPressed
    size(screenX, screenY)
    keysPressed = []
    temp = Paddle(0, 0)
    paddle = Paddle(screenX/2 - temp.w/2, screenY - screenY/30 - temp.h)

def draw():
    background(255)
    if "left" in keysPressed and "right" not in keysPressed:
        paddle.move("left")
    if "right" in keysPressed and "left" not in keysPressed:
        paddle.move("right")
    paddle.display()


def keyPressed():
    if convertKey(keyCode) is not None and convertKey(keyCode) not in keysPressed:
        keysPressed.append(convertKey(keyCode))


def keyReleased():
    if convertKey(keyCode) is not None:
        keysPressed.remove(convertKey(keyCode))
    
