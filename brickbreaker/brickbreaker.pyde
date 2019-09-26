screenX, screenY = 1024, 1024


class Paddle():
    w, h = 128, 32
    
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def move(self, dir):
        i = 0
        while i < speed:
            i += 1
            self.x += 1 if dir == "right" else -1
            if "paddle" in colliding:
                if (colliding["paddle"] == dir):
                    self.x -= 1 if dir == "right" else -1
                    break
    
    def display(self):
        fill(0, 150, 255)
        rect(self.x, self.y, self.w, self.h)


class Ball():
    r = 20
    dir = {"x": 1, "y": -1}
    
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def move(self):
        i = 0
        while i < speed:
            i += 1
            self.x += self.dir["x"]
            self.y += self.dir["y"]
            print(self.x, self.y)
            if "ball" in colliding:
                self.x -= self.dir["x"]
                self.y -= self.dir["y"]
                self.dir["x"] = 1 if colliding["ball"] == "left" else \
                    -1 if colliding["ball"] == "right" else self.dir["x"]
                self.dir["y"] = 1 if colliding["ball"] == "bottom" else \
                    -1 if colliding["ball"] == "top" else self.dir["y"]
                break


    def display(self):
        fill(255, 0, 0)
        circle(self.x, self.y, self.r*2)


class Brick():
    w, h = 64, 32
    
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def display(self):
        fill(130, 70, 70)
        rect(self.x, self.y, self.w, self.h)


def circleRectCollision(cx, cy, cr, rx, ry, rw, rh):
    edge = {"value": {"x": cx, "y": cy},
            "side": {"x": "middle", "y": "middle"}}
    if (cx < rx):
        edge["value"]["x"] = rx
        edge["side"]["x"] = "left"
    elif (cx > rx+rw):
        edge["value"]["x"] = rx+rw
        edge["side"]["x"] = "right"
    if (cy < ry):
        edge["value"]["y"] = ry
        edge["side"]["y"] = "top"
    elif (cy > ry+rh):
        edge["value"]["y"] = ry+rh
        edge["side"]["y"] = "bottom"
    distance = {"x": cx-edge["value"]["x"], "y": cy-edge["value"]["y"]}
    if (sqrt(distance["x"]**2 + distance["y"]**2)):
        return edge["side"]
    return None


def checkCollisions():
    global colliding
    colliding = {}
    # paddle screen side collision
    if (paddle.x <= 0):
        colliding["paddle"] = "left"
    elif (paddle.x + paddle.w == screenX):
        colliding["paddle"] = "right"
    # ball screen Side collision
    if (ball.x - ball.r <= 0):
        colliding["ball"] = "left"
    elif (ball.x + ball.r >= screenX):
        colliding["ball"] = "right"


def convertKey(n):
    return "left" if n == 65 or n == 37 else \
        "right" if n == 68 or n == 39 else None

def setup():
    global paddle, bricks, ball, keysPressed
    size(screenX, screenY)
    keysPressed = []
    bricks = []
    temp = Paddle(0, 0)
    paddle = Paddle(screenX/2 - temp.w/2, screenY - screenY/30 - temp.h)
    temp = Ball(0, 0)
    ball = Ball(paddle.x + paddle.w/2, paddle.y - temp.r)

def draw():
    global speed
    # Initialization
    background(255)
    speed = int(frameRate/8)
    # Movement
    checkCollisions()
    ball.move()
    if "left" in keysPressed and "right" not in keysPressed:
        paddle.move("left")
    if "right" in keysPressed and "left" not in keysPressed:
        paddle.move("right")
    # Display
    paddle.display()
    ball.display()
    for brick in bricks:
        brick.display()


def keyPressed():
    if convertKey(keyCode) is not None and convertKey(keyCode) not in keysPressed:
        keysPressed.append(convertKey(keyCode))


def keyReleased():
    if convertKey(keyCode) is not None:
        keysPressed.remove(convertKey(keyCode))
    
