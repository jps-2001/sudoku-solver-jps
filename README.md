# Sudoku Solver - Joseph Styles
A Sudoku solver program which uses constraint programming to imitate human techniques, instead of typical back-tracking.
Author: Joe Styles, 

## About:
- Program takes strings of 81 characters and attempts to solve the given Sudoku
- Provides a custom Class to generate Sudokus of adjustable square sizes (tested for 4x4 and 9x9)
- Uses intuitive human solving techniques to solve Sudoku, including hidden singles and naked pairs
- Testing file to conduct custom performance tests

## Requirements
- Python 3.13 or higher: https://www.python.org/downloads
- 'requests' library: https://pypi.org/project/requests

## Known Issues:
- Inconsistent solving for 'medium' and 'hard' puzzles
- Susceptible to errors if a custom puzzle is provided
- Limited error handling

## Future Iterations:
- Include advanced solving techniques: chains, X-Wing, XY-Wing
- Improved solver performance analysis: time complexity
- Implement error handling for robustness
- Convert into an executable file