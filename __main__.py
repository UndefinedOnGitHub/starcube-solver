from cubesolver import CubeSolver
from starcube import StarCube, BaseFace, SideCube, COLOR_MAP


def createRotationOutput(inp, inputPosition):
  color_dict = {
      "top": "w",
      "bottom": "y",
      "left": "b",
      "front": "r",
      "right": "g",
      "back": "p"}
  if inp in ["0", "1"]:
    return BaseFace(
        color_dict[inputPosition],
        color_dict[inputPosition],
        float(inp))
  else:
    print("Bad Input")
    return None


def createColorOutput(inp, inputPosition):
  if "." in inp:
    inps = inp.split(".")
  elif "|" in inp:
    inps = inp.split("|")
  else:
    inps = list(inp)

  if len(inps) != 2:
    print("Too Many Char")
  else:
    cornerColor, centerColor = inps[0:2]
    if cornerColor in COLOR_MAP and centerColor in COLOR_MAP:
      return BaseFace(cornerColor, centerColor)
    else:
      print("Incorrect Input")

  return None


def getColorFromInput(inputPosition, numberInput=False):
  output = None
  while not output:
    inp = input(f"Current Position[{inputPosition}]:\n")
    if numberInput:
      output = createRotationOutput(inp, inputPosition)
    else:
      output = createColorOutput(inp, inputPosition)

  return output


def getCommandLineInput(inputComment, numberInput=False):
  print(inputComment)
  top = getColorFromInput("top", numberInput)
  bottom = getColorFromInput("bottom", numberInput)
  left = getColorFromInput("left", numberInput)
  front = getColorFromInput("front", numberInput)
  right = getColorFromInput("right", numberInput)
  back = getColorFromInput("back", numberInput)
  if numberInput:
    cube = SideCube(
        top=top,
        bottom=bottom,
        left=left,
        front=front,
        right=right,
        back=back
    )
  else:
    cube = StarCube(
        top=top,
        bottom=bottom,
        left=left,
        front=front,
        right=right,
        back=back
    )
  print(cube)
  input("Press Return to run:\n\n")
  return cube


def main():
  cube = getCommandLineInput("Enter Cube Info: corner.center")

  cs = CubeSolver(cube)
  result = cs.solve()
  if result["result"]:
    print("\nRESULT:\n")
    for h in result["solved_cube"].cube_history:
      print(h)

    sidecube = getCommandLineInput(
        "Enter Cube Rotations: aligned=0 | misaligned=1", True)
    sidecs = CubeSolver(sidecube)
    sideresult = sidecs.solve()
    print("\nRESULT:\n")
    for h in sideresult["solved_cube"].cube_history:
      print(h)


if __name__ == "__main__":
  main()
