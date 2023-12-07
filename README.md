# Cube Solver

Cube Solver is a tool to solve the star shaped rubix cube (Meffert's Skewb Xtreme)
[Meffert's](https://www.mefferts.com/)

## Installation

```bash
git clone https://github.com/UndefinedOnGitHub/starcube-solver.git
```

## Usage

```bash
cd starcube-solver
python3 .
```

## Usage in code

```python
from starcube import StarCube, BaseFace
from starcube import CubeSolver
top = BaseFace(<cornerColor>, <centerColor>)
bottom = BaseFace(<cornerColor>, <centerColor>)
...

cube = StarCube(
	top=top,
  bottom=bottom,
  left=left,
  front=front,
  right=right,
  back=back
)

cs = CubeSolver(cube)
result = cs.solve()
```

## Pretty

```bash
python3 -m autopep8 --in-place --aggressive --aggressive --indent-size=2 .\<filename>
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
