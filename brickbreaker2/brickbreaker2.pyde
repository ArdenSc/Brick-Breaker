screenX, screenY = 1024, 1024
speed = 8


class Paddle():
    w = 128
    h = 32

    def __init__(self, x, y):
        self.x = x
        self.y = y

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
    angle = 45
    color = {"r": 255, "g": 0, "b": 0}

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        i = 0
        while i < speed*2:
            i += 1
            self.x += 0.5*cos(radians(self.angle - 90))
            self.y += 0.5*sin(radians(self.angle - 90))
            checkCollisions()
            if "ball" in colliding:
                self.x -= 0.5*cos(radians(self.angle - 90))
                self.y -= 0.5*sin(radians(self.angle - 90))
                for collision in colliding["ball"]:
                    self.angle = 2*collision-self.angle
                    if (self.angle < 0):
                        self.angle += 360
                    if (self.angle >= 360):
                        self.angle -= 360


    def display(self):
        fill(self.color["r"], self.color["g"], self.color["b"])
        circle(self.x, self.y, self.r*2)


class Brick():
    w = 64
    h = 32

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
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
            colliding["paddle"] = []
        colliding["paddle"].append("left")
    elif (paddle.x + paddle.w == screenX):
        if "paddle" not in colliding:
            colliding["paddle"] = []
        colliding["paddle"].append("right")
    # ball screen side collision
    if (ball.x - ball.r <= 0 or ball.x + ball.r >= screenX):
        if "ball" not in colliding:
            colliding["ball"] = []
        colliding["ball"].append(0)
    if (ball.y - ball.r <= 0):
        if "ball" not in colliding:
            colliding["ball"] = []
        colliding["ball"].append(90)
    # ball paddle colllision
    temp = circleRectCollision(ball.x, ball.y, ball.r, 
                               paddle.x, paddle.y, paddle.w, paddle.h)
    if temp is not None:
        if "ball" not in colliding:
            colliding["ball"] = []
        if (temp["x"] != "middle" and temp["y"] != "middle"):
            if "paddle" not in colliding:
                colliding["paddle"] = []
            colliding["paddle"].append(temp["x"])
            colliding["ball"].append(45 if ((temp["x"] == "left" and temp["y"] == "top") or 
                                            (temp["x"] == "right" and temp["y"] == "bottom")) else 135)
        elif (temp["x"] == "middle"):
            colliding["ball"].append(90)
        elif (temp["y"] == "middle"):
            if "paddle" not in colliding:
                colliding["paddle"] = []
            colliding["paddle"].append(temp["x"])
            colliding["ball"].append(0)
        else:
            print("Ball is inside an object, terminating")
            exit()
    # ball brick collision
    i = 0
    while (i < len(bricks)):
        temp = circleRectCollision(ball.x, ball.y, ball.r, 
                                   bricks[i].x, bricks[i].y, bricks[i].w, bricks[i].h)
        if temp is not None:
            if "ball" not in colliding:
                colliding["ball"] = []
            if (temp["x"] != "middle" and temp["y"] != "middle"):
                colliding["ball"].append(45 if ((temp["x"] == "left" and temp["y"] == "top") or 
                                            (temp["x"] == "right" and temp["y"] == "bottom")) else 135)
            elif (temp["x"] == "middle"):
                colliding["ball"].append(90)
            elif (temp["y"] == "middle"):
                colliding["ball"].append(0)
            else:
                print("Ball is inside an object, terminating")
                exit()
            del bricks[i]
        i += 1


def convertKey(n):
    return "left" if n == 65 or n == 37 else \
        "right" if n == 68 or n == 39 else None


def reset():
    global paddle, bricks, totalBricks, ball, keysPressed, impact, gamestate
    keysPressed = []
    bricks = []
    gamestate = 0
    for x in range(8):
        for y in range(12):
            if (random(1) >= 0.5):
                bricks.append(Brick(screenX/2 + x*64, 32 + y*32, 
                                    {"r": random(51)*5, "g": random(51)*5, "b": random(51)*5}))
                bricks.append(Brick(screenX/2 - screenX/16 - x*64, 32 + y*32, 
                                    {"r": random(51)*5, "g": random(51)*5, "b": random(51)*5}))
    totalBricks = len(bricks)
    temp = Paddle(0, 0)
    paddle = Paddle(screenX/2 - temp.w/2, screenY - screenY/30 - temp.h)
    temp = Ball(0, 0)
    ball = Ball(paddle.x + paddle.w/2, paddle.y - temp.r - 10)


def setup():
    global impact
    size(screenX, screenY)
    frameRate(60)
    impact = createFont("Impact", 48)
    reset()


def draw():
    # Initialization
    background(200)
    # Movement
    if gamestate == 1:
        if "left" in keysPressed and "right" not in keysPressed:
            paddle.move("left")
        if "right" in keysPressed and "left" not in keysPressed:
            paddle.move("right")
        ball.move()
        if (len(bricks) == 0 or ball.y >= screenY + ball.r):
            reset()
    # Display
    guiDisplay()
    paddle.display()
    ball.display()
    for brick in bricks:
        brick.display()


def keyPressed():
    global gamestate
    if convertKey(keyCode) is not None and convertKey(keyCode) not in keysPressed:
        keysPressed.append(convertKey(keyCode))
        gamestate = 1


def keyReleased():
    if convertKey(keyCode) is not None and convertKey(keyCode) in keysPressed:
        keysPressed.remove(convertKey(keyCode))
