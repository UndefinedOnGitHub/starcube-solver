import re
import random
from cubesolver import CubeSolver
from starcube import StarCube, BaseFace, SideCube, COLOR_MAP, BaseCubeMove

# Include color if allowed
try:
  from termcolor import colored, cprint
except ImportError:
  def cprint(text, color=None, background=None):
    print(text)

  def colored(text, color):
    return text


class StarCubeRunner():
  """Runner to process user inputs"""
  def __init__(self, args=[]):
    self.args = args

  def colored_cube(self, cube):
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

  def createRotationOutput(self, inp, inputPosition):
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

  def createColorOutput(self, inp, inputPosition):
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

  def getColorFromInput(self, inputPosition, numberInput=False):
    output = None
    while not output:
      inp = input(f"Current Position[{inputPosition}]: ")
      if numberInput:
        output = self.createRotationOutput(inp, inputPosition)
      else:
        output = self.createColorOutput(inp, inputPosition)

    return output

  def getCommandLineInput(self, inputComment, numberInput=False):
    print(inputComment)
    top = self.getColorFromInput("top", numberInput)
    bottom = self.getColorFromInput("bottom", numberInput)
    left = self.getColorFromInput("left", numberInput)
    front = self.getColorFromInput("front", numberInput)
    right = self.getColorFromInput("right", numberInput)
    back = self.getColorFromInput("back", numberInput)
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
    print(self.colored_cube(cube))
    input(colored("Press Return to run", "blue"))
    print("")
    return cube

  def startupStar(self):
    # return "\n".join([
    #   " " * 17 + ".",
    #   " " * 12 + "---./|\\.---",
    #   " " * 12 + "'._/ | \\_.'",
    #   " " * 10 + "_.-'_'.|.'_'-._",
    #   " " * 11 + "'-._.'|'._.-'",
    #   " " * 12 + ".' \\ | / '.",
    #   " " * 12 + "---'\\|/'---",
    #   " " * 17 + "'",
    # ])
    # return """
    #              .
    #         ---./|\\.---
    #         '._/ | \\_.'
    #       _.-'_'.|.'_'-._
    #        '-._.'|'._.-'
    #         .' \\ | / '.
    #         ---'\\|/'---
    #              '
    # """
    coloredQuotes = [
      # colored("'", 'white'),
      colored("'", 'yellow'),
      colored("'", 'blue'),
      colored("'", 'red'),
      colored("'", 'green'),
      colored("'", 'magenta')
    ]
    rc = lambda: coloredQuotes[random.randrange(0, len(coloredQuotes))]
    return "\n".join([
      " " * 17 + ".",
      " " * 12 + "---./|\\.---",
      " " * 12 + f"{rc()}._/ | \\_.{rc()}",
      " " * 10 + f"_.-{rc()}_{rc()}.|.{rc()}_{rc()}-._",
      " " * 11 + f"{rc()}-._.{rc()}|{rc()}._.-{rc()}",
      " " * 12 + f".{rc()} \\ | / {rc()}.",
      " " * 12 + f"---{rc()}\\|/{rc()}---",
      " " * 17 + "'",
    ])

  def run(self):
    print("")
    print(self.startupStar())
    print("\n   WELCOME TO THE STAR CUBE SOLVER\n")
    # print("""
    #              .
    #         ---./|\\.---
    #         '._/ | \\_.'
    #       _.-'_'.|.'_'-._
    #        '-._.'|'._.-'
    #         .' \\ | / '.
    #         ---'\\|/'---
    #              '

    # WELCOME TO THE STAR CUBE SOLVER

    # """)
    print(
        "Color options: ", colored(
            "w", 'white'), colored(
            "y", 'yellow'), colored(
            "b", 'blue'), colored(
            "r", 'red'), colored(
            "g", 'green'), colored(
                "p", 'magenta'))
    cube = self.getCommandLineInput("Enter Cube Info: <corner>.<center>")

    cs = CubeSolver(cube)
    result = cs.solve()

    if result["result"]:
      print("\nSOLUTION:\n")
      for h in result["solved_cube"].cube_history:
        print(self.colored_cube(h))

      print("\n")

      sidecube = self.getCommandLineInput(
          "Enter Cube Rotations: aligned=0 | misaligned=1", True)
      sidecs = CubeSolver(sidecube)
      sideresult = sidecs.solve()

      print("\nRESULT:\n")
      for h in sideresult["solved_cube"].cube_history:
        colored_history = re.sub(r"\~", colored("~", "yellow"), str(h))
        colored_history = re.sub(r"\*", colored("*", "green"), colored_history)
        print(colored_history)
