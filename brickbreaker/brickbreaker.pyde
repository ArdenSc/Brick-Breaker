screenX, screenY = 1024, 1024


class Paddle():
    w, h = 128, 32

    def __init__(self, x, y):
        self.x, self.y = x, y

    def move(self, dir):
        i = 0
        while i < speed:
            i += 1
            checkCollisions()
            self.x += 1 if dir == "right" else -1
            if "paddle" in colliding and "x" in colliding["paddle"]:
                if (colliding["paddle"]["x"] == dir):
                    self.x -= 1 if dir == "right" else -1
                    break

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
            checkCollisions()
            self.x += self.dir["x"]
            self.y += self.dir["y"]
            if "ball" in colliding:
                self.x -= self.dir["x"]
                self.y -= self.dir["y"]
                if "x" in colliding["ball"]:
                    self.dir["x"] = 1 if colliding["ball"]["x"] == "left" else \
                        -1 if colliding["ball"]["x"] == "right" else self.dir["x"]
                if "y" in colliding["ball"]:
                    self.dir["y"] = 1 if colliding["ball"]["y"] == "top" else \
                        -1 if colliding["ball"]["y"] == "bottom" else self.dir["y"]
                self.x += self.dir["x"]
                self.y += self.dir["y"]

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
        colliding["ball"]["x"] = "left"
    elif (ball.x + ball.r == screenX):
        if "ball" not in colliding:
            colliding["ball"] = {}
        colliding["ball"]["x"] = "right"
    if (ball.y - ball.r == 0):
        if "ball" not in colliding:
            colliding["ball"] = {}
        colliding["ball"]["y"] = "top"
    # ball paddle collision
    temp = circleRectCollision(ball.x, ball.y, ball.r, paddle.x, paddle.y, paddle.w, paddle.h)
    if temp is not None:
        if (temp["y"] != "middle"):
            if "paddle" not in colliding:
                colliding["paddle"] = {}
            if "ball" not in colliding:
                colliding["ball"] = {}
            colliding["paddle"]["y"] = temp["y"]
            colliding["ball"]["y"] = "bottom" if temp["y"] == "top" else "top"
        else:
            if "paddle" not in colliding:
                colliding["paddle"] = {}
            if "ball" not in colliding:
                colliding["ball"] = {}
            colliding["paddle"]["x"] = temp["x"]
            colliding["ball"]["x"] = "left" if temp["x"] == "right" else "right"
    # ball brick collision
    i = 0
    while (i < len(bricks)):
        temp = circleRectCollision(ball.x, ball.y, ball.r, bricks[i].x, bricks[i].y, bricks[i].w, bricks[i].h)
        if temp is not None:
            if (temp["y"] != "middle"):
                if "ball" not in colliding:
                    colliding["ball"] = {}
                colliding["ball"]["y"] = "bottom" if temp["y"] == "top" else "top"
            else:
                if "ball" not in colliding:
                    colliding["ball"] = {}
                colliding["ball"]["x"] = "left" if temp["x"] == "right" else "right"
            ball.color = bricks[i].color
            del bricks[i]
        i += 1


def convertKey(n):
    return "left" if n == 65 or n == 37 else \
        "right" if n == 68 or n == 39 else None


def setup():
    global paddle, bricks, ball, keysPressed
    size(screenX, screenY)
    keysPressed = []
    bricks = []
    for x in range(16):
        for y in range(5):
            bricks.append(Brick(x*64, 64 + y*32, {"r": random(255), "g": random(255), "b": random(255)}))
    print(len(bricks))
    temp = Paddle(0, 0)
    paddle = Paddle(screenX/2 - temp.w/2, screenY - screenY/30 - temp.h)
    temp = Ball(0, 0)
    ball = Ball(paddle.x + paddle.w/2, paddle.y - temp.r)


def draw():
    global speed
    # Initialization
    background(200)
    speed = int(frameRate/8)
    # Movement
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
