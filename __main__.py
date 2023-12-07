import re
from cubesolver import CubeSolver
from starcube import StarCube, BaseFace, SideCube, COLOR_MAP, BaseCubeMove

USED_CORNERS = COLOR_MAP
USED_CENTERS = COLOR_MAP

try:
  from termcolor import colored, cprint
  import foo
except ImportError:
  def cprint(text, color=None, background=None):
    print(text)

  def colored(text, color):
    return text


def colored_cube(cube):
  if isinstance(cube, BaseCubeMove):
    move = f"{cube.move}\n\n"
    string_cube = str(cube.cube)
  else:
    move = ""
    string_cube = str(cube)

  string_cube = re.sub(r"w", colored("w", "white"), string_cube)
  string_cube = re.sub(r"y", colored("y", "yellow"), string_cube)
  string_cube = re.sub(r"b", colored("b", "blue"), string_cube)
  string_cube = re.sub(r"r", colored("r", "red"), string_cube)
  string_cube = re.sub(r"g", colored("g", "green"), string_cube)
  string_cube = re.sub(r"p", colored("p", "magenta"), string_cube)
  return f"{move}{string_cube}"


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
    cprint("Bad Input", "red")
    return None


def createColorOutput(inp, inputPosition):
  if "." in inp:
    inps = inp.split(".")
  elif "|" in inp:
    inps = inp.split("|")
  else:
    inps = list(inp)

  if len(inps) != 2:
    cprint("Too Many Char", "red")
  else:
    cornerColor, centerColor = inps[0:2]
    if cornerColor in COLOR_MAP and centerColor in COLOR_MAP:
      return BaseFace(cornerColor, centerColor)
    else:
      cprint("Incorrect Input", "red")

  return None


def getColorFromInput(inputPosition, numberInput=False):
  output = None
  while not output:
    inp = input(f"Current Position[{inputPosition}]: ")
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
  print("\nPreview:\n")
  print(colored_cube(cube))
  input(colored("Press Return to run", "blue"))
  print("")
  return cube


def main():
  print("""
               .
          ---./|\\.---
          '._/ | \\_.'
        _.-'_'.|.'_'-._
         '-._.'|'._.-'
          .' \\ | / '.
          ---'\\|/'---
               '

  WELCOME TO THE STAR CUBE SOLVER

  """)
  print(
      "Color options: ", colored(
          "w", 'white'), colored(
          "y", 'yellow'), colored(
          "b", 'blue'), colored(
          "r", 'red'), colored(
          "g", 'green'), colored(
              "p", 'magenta'))
  cube = getCommandLineInput("Enter Cube Info: <corner>.<center>")

  cs = CubeSolver(cube)
  result = cs.solve()
  if result["result"]:
    print("\nSOLUTION:\n")
    for h in result["solved_cube"].cube_history:
      print(colored_cube(h))

    print("\n")
    sidecube = getCommandLineInput(
        "Enter Cube Rotations: aligned=0 | misaligned=1", True)
    sidecs = CubeSolver(sidecube)
    sideresult = sidecs.solve()
    print("\nRESULT:\n")
    for h in sideresult["solved_cube"].cube_history:
      colored_history = re.sub(r"\~", colored("~", "yellow"), str(h))
      colored_history = re.sub(r"\*", colored("*", "green"), colored_history)
      print(colored_history)


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt as e:
    cprint("\n\nExiting Solver\n", "yellow")
