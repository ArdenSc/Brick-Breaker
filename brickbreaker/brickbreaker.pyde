screenX, screenY = 1024, 1024
speed = 8


class Paddle():
    w, h = 128, 32

    def __init__(self, x, y):
        self.x, self.y = x, y

    def move(self, dir):
        i = 0
        while i < speed:
            i += 1
            self.x += 1 if dir == "right" else -1
            checkCollisions()
            if "paddle" in colliding and "x" in colliding["paddle"]:
                if (colliding["paddle"]["x"] == dir):
                    self.x -= 1 if dir == "right" else -1

    def display(self):
        fill(0, 150, 255)
        rect(self.x, self.y, self.w, self.h)


class Ball():
    r = 20
    dir = {"x": 1, "y": -1}
    color = {"r": 255, "g": 0, "b": 0}

    def __init__(self, x, y):
        self.x, self.y = x, y

    def move(self):
        i = 0
        while i < speed:
            i += 1
            self.x += self.dir["x"]
            self.y += self.dir["y"]
            checkCollisions()
            if "ball" in colliding:
                self.x -= self.dir["x"]
                self.y -= self.dir["y"]
                if "x" in colliding["ball"]:
                    for collision in colliding["ball"]["x"]:
                        self.dir["x"] = 1 if collision == "left" else \
                            -1 if collision == "right" else self.dir["x"]
                if "y" in colliding["ball"]:
                    for collision in colliding["ball"]["y"]:
                        self.dir["y"] = 1 if collision == "top" else \
                            -1 if collision == "bottom" else self.dir["y"]

    def display(self):
        fill(self.color["r"], self.color["g"], self.color["b"])
        circle(self.x, self.y, self.r*2)


class Brick():
    w, h = 64, 32

    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color

    def display(self):
        fill(self.color["r"], self.color["g"], self.color["b"])
        rect(self.x, self.y, self.w, self.h)


def guiDisplay():
    textFont(impact)
    textAlign(CENTER, CENTER)
    fill(255)
    text(str(int(float(totalBricks - len(bricks)) / totalBricks * 100)) + "%", screenX/2, screenY/2)


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
    if (sqrt(distance["x"]**2 + distance["y"]**2) <= cr):
        return edge["side"]
    return None


def checkCollisions():
    global colliding
    colliding = {}
    # paddle screen side collision
    if (paddle.x <= 0):
        if "paddle" not in colliding:
            colliding["paddle"] = {}
        colliding["paddle"]["x"] = "left"
    elif (paddle.x + paddle.w == screenX):
        if "paddle" not in colliding:
            colliding["paddle"] = {}
        colliding["paddle"]["x"] = "right"
    # ball screen side collision
    if (ball.x - ball.r == 0):
        if "ball" not in colliding:
            colliding["ball"] = {}
        if "x" not in colliding:
            colliding["ball"]["x"] = []
        colliding["ball"]["x"].append("left")
    elif (ball.x + ball.r == screenX):
        if "ball" not in colliding:
            colliding["ball"] = {}
        if "x" not in colliding:
            colliding["ball"]["x"] = []
        colliding["ball"]["x"].append("right")
    if (ball.y - ball.r == 0):
        if "ball" not in colliding:
            colliding["ball"] = {}
        if "x" not in colliding:
            colliding["ball"]["y"] = []
        colliding["ball"]["y"].append("top")
    # ball paddle collision
    temp = circleRectCollision(ball.x, ball.y, ball.r, paddle.x, paddle.y, paddle.w, paddle.h)
    if temp is not None:
        if (temp["x"] != "middle"):
            if "paddle" not in colliding:
                colliding["paddle"] = {}
            if "ball" not in colliding:
                colliding["ball"] = {}
            if "x" not in colliding["ball"]:
                colliding["ball"]["x"] = []
            colliding["paddle"]["x"] = temp["x"]
            colliding["ball"]["x"].append("left" if temp["x"] == "right" else "right")
        if (temp["y"] != "middle"):
            if "paddle" not in colliding:
                colliding["paddle"] = {}
            if "ball" not in colliding:
                colliding["ball"] = {}
            if "y" not in colliding["ball"]:
                colliding["ball"]["y"] = []
            colliding["paddle"]["y"] = temp["y"]
            colliding["ball"]["y"].append("bottom" if temp["y"] == "top" else "top")
    # ball brick collision
    i = 0
    while (i < len(bricks)):
        temp = circleRectCollision(ball.x, ball.y, ball.r, bricks[i].x, bricks[i].y, bricks[i].w, bricks[i].h)
        if temp is not None:
            if (temp["x"] != "middle"):
                if "ball" not in colliding:
                    colliding["ball"] = {}
                if "x" not in colliding["ball"]:
                    colliding["ball"]["x"] = []
                colliding["ball"]["x"].append("left" if temp["x"] == "right" else "right")
            if (temp["y"] != "middle"):
                if "ball" not in colliding:
                    colliding["ball"] = {}
                if "y" not in colliding["ball"]:
                    colliding["ball"]["y"] = []
                colliding["ball"]["y"].append("bottom" if temp["y"] == "top" else "top")
            ball.color = bricks[i].color
            del bricks[i]
        i += 1


def convertKey(n):
    return "left" if n == 65 or n == 37 else \
        "right" if n == 68 or n == 39 else None


def setup():
    global paddle, bricks, totalBricks, ball, keysPressed, impact
    size(screenX, screenY)
    frameRate(60)
    keysPressed = []
    bricks = []
    impact = createFont("Impact", 48)
    for x in range(8):
        for y in range(12):
            if (random(1) >= 0.5):
                bricks.append(Brick(screenX/2 + x*64, 32 + y*32, {"r": random(51)*5, "g": random(51)*5, "b": random(51)*5}))
                bricks.append(Brick(screenX/2 - screenX/16 - x*64, 32 + y*32, {"r": random(51)*5, "g": random(51)*5, "b": random(51)*5}))
    totalBricks = len(bricks)
    temp = Paddle(0, 0)
    paddle = Paddle(screenX/2 - temp.w/2, screenY - screenY/30 - temp.h)
    temp = Ball(0, 0)
    ball = Ball(paddle.x + paddle.w/2, paddle.y - temp.r)


def draw():
    # Initialization
    background(200)
    # Movement
    ball.move()
    if "left" in keysPressed and "right" not in keysPressed:
        paddle.move("left")
    if "right" in keysPressed and "left" not in keysPressed:
        paddle.move("right")
    # Display
    guiDisplay()
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
