from main import Sudoku
import requests

class testingSudoku(Sudoku):
    def __init__(self, puzzle, solution):
        super().__init__(puzzle, solution)

if __name__ == "__main__":

    difficultyDictionary = {
        1 : 'easy',
        2 : 'medium',
        3 : 'hard'
    }

#### Testing Area ####
    numIterations = 100
    difficulty = 3


    difficultyString = difficultyDictionary[difficulty] # 'easy', 'medium' or 'hard'

    # Occurs for given number of iterations
    solveCount = 0
    for iteration in range(numIterations):
        
        # Defines test Sudoku environment
        body = {
                "difficulty": difficultyString,   # Options: "easy", "medium", or "hard" (defaults to "easy")
                "solution": True,       # True or False (defaults to True)
                "array": False          # True or False (defaults to False)
            }
        headers =  {"Content-Type":"application/json"}
        response = requests.post("https://youdosudoku.com/api/", json=body, headers=headers)

        # Ensures data is correctly received
        if response.status_code == 200:
            API_data = response.json()
        else:
            print(f"Error: {response.status_code}")

        # New test
        print(f"New Sudoku: {iteration + 1}")
        newSudoku = testingSudoku(API_data["puzzle"], API_data["solution"])
        solved = newSudoku.attemptSolve()

        # Increment solved counter if solution is achieved
        if solved: 
            solveCount += 1
            print("\nPass")
        else: print("\nFail")

    print("Results: ")
    print(f"{solveCount} out of {numIterations} were correctly solved!")

    
"""
    Results: (100 iterations)
     'easy'  :   100% 
    'medium' :   90%
     'hard'  :   59%
"""
