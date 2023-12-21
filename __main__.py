from runner import StarCubeRunner, cprint
import sys

if __name__ == "__main__":
  try:
    StarCubeRunner(sys.argv).run()
  except KeyboardInterrupt as e:
    cprint("\n\nExiting Solver\n", "yellow")
