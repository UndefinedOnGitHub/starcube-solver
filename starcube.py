COLOR_MAP = ["w", "y", "b", "r", "g", "p"]

###
# BaseFace
###


class BaseFace():
  def __init__(self, cornerColor, centerColor, rotation=0):
    self.cornerColor = cornerColor
    self.centerColor = centerColor
    self.rotation = rotation

  def __str__(self):
    rotation = "*" if self.rotation == 0 else "~"
    return f"{self.cornerColor}({self.centerColor}){rotation}"

  def copy(self):
    return BaseFace(self.cornerColor, self.centerColor, self.rotation)

  def switchCenterColor(self, otherFace):
    currentColor = self.centerColor
    otherColor = otherFace.centerColor
    otherFace.centerColor = currentColor
    self.centerColor = otherColor
    return None

  def value(self):
    return 0 if self.centerColor == self.cornerColor else 1

  def rotate(self, direction=True):
    if direction:
      self.rotation = (self.rotation + 0.5) % 2
    else:
      self.rotation = (self.rotation - 0.5) % 2

  def __radd__(self, memo):
    if isinstance(memo, BaseFace):
      return self.value() + memo.value()
    elif isinstance(memo, int):
      return self.value() + memo
    else:
      return self.value()

  def __add__(self, memo):
    if isinstance(memo, BaseFace):
      return self.value() + memo.value()
    elif isinstance(memo, int):
      return self.value() + memo
    else:
      return self.value()

###
# BaseCubeMove
###


class BaseCubeMove():
  def __init__(self, cube, move="init"):
    self.cube = cube
    self.move = move

  def __str__(self):
    return f"{self.move}\n{self.cube}"

###
# BaseCube
###


class BaseCube():
  def __init__(self, top, bottom, left, front, right, back):
    self.faces = [
        top.copy(),
        bottom.copy(),
        left.copy(),
        front.copy(),
        right.copy(),
        back.copy()]
    self._cube_history = [BaseCubeMove(self)]

  def __str__(self):
    spacing = f"      "
    outstr_list = [
        f"{spacing}{self.top}",
        " ".join(map(lambda x: str(x), self.faces[2:])),
        f"{spacing}{self.bottom}",
        ""
    ]
    return "\n".join(outstr_list)

  @property
  def cube_history(self):
    return self._cube_history

  @cube_history.setter
  def cube_history(self, value):
    self._cube_history = value

  def copy(self, faces=None):
    if faces is None:
      faces = self.faces
    return BaseCube(*faces)

  def sum(self):
    return sum(self.faces)

  @property
  def top(self):
    return self.faces[0]

  @property
  def bottom(self):
    return self.faces[1]

  @property
  def left(self):
    return self.faces[2]

  @property
  def front(self):
    return self.faces[3]

  @property
  def right(self):
    return self.faces[4]

  @property
  def back(self):
    return self.faces[5]

  # MOVES
  def rotate_right(self):
    body = self.faces[2:]
    first = body.pop()
    body.insert(0, first)
    c = self.copy([self.top, self.bottom] + body)
    return c

  def rotate_left(self):
    body = self.faces[2:]
    first = body.pop(0)
    body.append(first)

    c = self.copy([self.top, self.bottom] + body)
    return c

  def rotate_up(self):
    return self.rotate_back()

  def rotate_back(self):
    top, bottom, left, front, right, back = self.faces
    new_list = [
        front, back, left, bottom, right, top
    ]

    c = self.copy(new_list)
    return c

  def rotate_down(self):
    return self.rotate_front()

  def rotate_front(self):
    top, bottom, left, front, right, back = self.faces
    new_list = [
        back, front, left, top, right, bottom
    ]

    c = self.copy(new_list)
    return c

  def body_rotate(self, cube):
    return [
        cube,
        cube.move("rotate_right"),
        cube.move("rotate_right").move("rotate_right"),
        cube.move("rotate_left"),
        cube.move("rotate_up"),
        cube.move("rotate_down")
    ]

  def _move(self, movement):
    if movement == "rotate_down":
      nextCube = self.rotate_down()
    elif movement == "rotate_up":
      nextCube = self.rotate_up()
    elif movement == "rotate_left":
      nextCube = self.rotate_left()
    elif movement == "rotate_right":
      nextCube = self.rotate_right()
    elif movement == "corner_rotate_top_right":
      nextCube = self.corner_rotate_top_right()
    elif movement == "corner_rotate_top_left":
      nextCube = self.corner_rotate_top_left()
    elif movement == "center_rotate_out":
      nextCube = self.center_rotate_out()
    else:
      raise Exception(f"Unknown Movement - {movement}")

    nextCube.cube_history = list(
        self.cube_history) + [BaseCubeMove(nextCube, movement)]
    return nextCube

  def move(self, movement):
    return self._move(movement)

  def possible_rotations(self):
    return self.body_rotate(self) + self.body_rotate(self.move("rotate_up")
                                                     ) + self.body_rotate(self.move("rotate_down"))

  @property
  def possible_moves(self):
    return [
        "corner_rotate_top_right",
        "corner_rotate_top_left",
        "center_rotate_out"]

  # Make Cube Change Move
  def corner_rotate_top_right(self):
    c = self.copy()

    c.front.switchCenterColor(c.right)
    c.bottom.switchCenterColor(c.back)
    list(map(lambda x: x.rotate(), [c.front, c.right, c.bottom, c.back]))
    return c

  def corner_rotate_top_left(self):
    c = self.copy()

    c.left.switchCenterColor(c.front)
    c.bottom.switchCenterColor(c.back)
    list(map(lambda x: x.rotate(), [c.front, c.left, c.bottom, c.back]))
    return c

  def center_rotate_out(self):
    c = self.copy()

    c.bottom.switchCenterColor(c.front)
    c.left.switchCenterColor(c.right)
    list(map(lambda x: x.rotate(), [c.front, c.left, c.bottom, c.right]))
    return c

###
# SideCube
###


class StarCube(BaseCube):
  def __init__(self, top, bottom, left, front, right, back):
    super(StarCube, self).__init__(top, bottom, left, front, right, back)

###
# SideCube
###


class SideCube(BaseCube):
  def __init__(self, top, bottom, left, front, right, back):
    super(SideCube, self).__init__(top, bottom, left, front, right, back)

  def sum(self):
    result = sum(map(lambda x: x.rotation, self.faces))
    return result

  def copy(self, faces=None):
    if faces is None:
      faces = self.faces
    return SideCube(*faces)

  def move(self, movement):
    mv = self
    if movement in self.possible_moves:
      mv = self._move(movement)
    return mv._move(movement)


def getCubeFacesFromSides(top=0, bottom=0, left=0, front=0, right=0, back=0):
  f_top = BaseFace("w", "w", float(top))
  f_bottom = BaseFace("y", "y", float(bottom))
  f_left = BaseFace("b", "b", float(left))
  f_front = BaseFace("r", "r", float(front))
  f_right = BaseFace("g", "g", float(right))
  f_back = BaseFace("p", "p", float(back))
  return [f_top, f_bottom, f_left, f_front, f_right, f_back]
