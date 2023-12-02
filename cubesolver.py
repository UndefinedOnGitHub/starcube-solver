class CubeSolver():
  def __init__(self, cube, depth=3):
    self.cube = cube
    self.depth = depth
    self.attempt_counter = 0

  def solve(self, cubes=None, counter=0):
    if not cubes:
      cubes = [self.cube]

    attempted_cubes = []
    solution = False
    result = None

    if counter > self.depth:
      print(f"Ending")
      return {"result": True, "value": ["Bad Result"]}

    for cube in cubes:
      for c in cube.possible_rotations():
        move_cubes = []
        # Do the movement action
        for move in c.possible_moves:
          move_cubes.append(c.move(move))
        minCube = min(move_cubes, key=lambda x: x.sum())
        solveCheck = minCube.sum() == 0
        # Grab the cube with current location
        attempted_cubes = attempted_cubes + move_cubes
        # Log the attempt
        self.attempt_counter += 1
        # Check if cube is solved
        if solveCheck:
          # Log Path
          map(lambda x: print(x), minCube.cube_history)
          result = minCube
          solution = True
          break
      # Should break outer loop if solution found
      if solution:
        break

    if solution:
      return {
          "result": True,
          "value": result.cube_history,
          "solved_cube": result}
    else:
      counter += 1
      print(f"{counter=}")
      return self.solve(attempted_cubes, counter)
