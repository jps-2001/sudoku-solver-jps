# Requires Virtual ENVironment (VENV) to get Python 3.13 to work, with 'requests' library
import requests

"""
TODO: determine algorithm!
- list functions:
    - sets & gets DONE
    - verify
    - translate from string to 3x3 (for visual purposes) DONE?
"""
class Sudoku:
    def __init__(self, puzzle: str, solution: str):
        # Dynamic sudoku sizes
        self.sudokuSize = 3
        self.setSizes()
        self.progress = 0

        self.puzzle = puzzle
        self.squareForm = self.getSquarePuzzle()
        self.solution = solution
        self.squareSolution = self.getSquareSolution()
        self.possibleCells = self.initialiseSolver()
    
    def setSizes(self):
        # Sets line and puzzle element sizes for future reference
        self.lineSize = self.sudokuSize ** 2
        self.puzzleSize = self.sudokuSize ** 4

    def initialiseSolver(self) -> list:
        # Generates a multi-dimensional array for all 81 cells
        # Each cell contains the numbers 1 - 9, used to determine the solution to the puzzle
        allCells_list = []
        # No target list required, so an underscore can be used
        for element in self.puzzle:
            # Unknown elements are filled with all possible digits
            if element == "0":
                possibleDigits = list(range(1, self.lineSize + 1))
            else: 
                # Known elements are isolated
                possibleDigits = [0] * self.lineSize
                # Every other element in the list becomes zero
                intElement = int(element)
                possibleDigits[intElement - 1] = intElement
            allCells_list.append(possibleDigits)
        return allCells_list

    def getRow(self, rowNum: int) -> str:
        startIdx = self.lineSize * rowNum
        # Returns a 9-element array of a specified row
        row = self.puzzle[startIdx : startIdx + self.lineSize]
        return row
    
    def getCol(self, colNum: int) -> str:
        # Returns a 9-element array of a specified column
        col = self.puzzle[colNum : self.puzzleSize : self.lineSize]
        return col
    
    def getSquarePuzzle(self) -> list:
        # Returns a square format, useful for debugging
        # Typically size 9-by-9
        squareForm = []
        for rowIdx in range(0, self.lineSize):
            # Typically returns a 9-element row
            squareForm.append(self.getRow(rowIdx))
        return squareForm
    
    def getSquareSolution(self) -> list:
        # Returns a square format, useful for debugging
        # Typically size 9-by-9
        squareForm = []
        for rowIdx in range(0, self.lineSize):
            startIdx = self.lineSize * rowIdx
            squareForm.append(self.solution[startIdx : startIdx + self.lineSize])
        return squareForm        

    def getSquare(self, squareNum: int) -> str:
        # Typically returns a 9-element string
        # Eventually contains each digit from 1 - 9 (Sudoku rules)
        # Square order starts top left, ends bottom right:
        #  0 | 1 | 2
        # -----------
        #  3 | 4 | 5
        # -----------
        #  6 | 7 | 8

        square = ""
        # Uses integer devision and modulus operations to convert required square into co-ordinates
        # Floor handles y-coord, modulus handles x-coord
        startRowIdx = squareNum // self.sudokuSize
        startColIdx = squareNum % self.sudokuSize
        for offsetIdx in range(self.sudokuSize):
            # Typically, appends 3 rows of 3 elements, forming a 3-by-3 square
            # Each iteration adds a 3-element array, using the determined offsets
            square += self.getRow((self.sudokuSize * startRowIdx) + offsetIdx)[(self.sudokuSize * startColIdx) : (self.sudokuSize * startColIdx) + self.sudokuSize]
        return square

    def iteration(self):
        solved = False
        while solved == False:
            self.solve()
            solved = self.verifySolution()
            self.squareForm = self.getSquarePuzzle()

            self.progress = self.getProgress()
            # Serial monitor text to update progress
            text = f"Elements Found: {self.progress} out of {self.puzzleSize}"
            formatted_text = text.ljust(25)
            print(f"{formatted_text}", end="\r")

        print("Solved!")
        """ Progress: {round(100 * iteration / self.num_of_iterations)}% """  

    def attemptSolve(self) -> bool:
        # Attempts to solve the Sudoku. If no progress is made, the algorithm has failed
        # Returns a boolean result, detailing the result of the algorithm
        
        # Number of allowed iterations before the algorithm is considered a failure
        failCriteria = 10
        staleCounter = 0
        previousIteration = self.puzzle[:]
        solved = False
        while not solved:
            self.solve()
            
            self.squareForm = self.getSquarePuzzle()

            self.progress = self.getProgress()

            # Serial monitor text to update progress
            text = f"Elements Found: {self.progress} out of {self.puzzleSize}"
            formatted_text = text.ljust(25)
            print(f"{formatted_text}", end="\r")

            solved = self.verifySolution()
            if not solved: 
                if self.puzzle == previousIteration: staleCounter += 1
                else: staleCounter = 0
                if staleCounter >= failCriteria: return False
                previousIteration = self.puzzle[:]

        # If code is able to exit loop, solution must've been located!
        return True

    def getProgress(self) -> int:
        # Determines the number of solved elements
        zeroCount = 0
        for element in self.puzzle:
            if element == "0": zeroCount += 1
        return self.puzzleSize - zeroCount

    def solve(self):
        # A single iteration towards the final solution
        for rowIdx in range(self.lineSize):
            # 'x' component to determine square quadrant
            xComponent = rowIdx // self.sudokuSize
            for colIdx in range(self.lineSize):
                # Row is updated per element to account for incremental changes
                currentRow = self.getRow(rowIdx)
                currentCol = self.getCol(colIdx)

                # 'y' component to determine square quadrant
                yComponent = colIdx // self.sudokuSize
                squareIdx = (self.sudokuSize * xComponent) + yComponent
                currentSquare = self.getSquare(squareIdx)
                
                # This combination of rows, columns (and technically square) correlates with a single element in the puzzle!
                # If any non-zero digits are found in these variables, the element at this address CANNOT be said digit(s)
                # Get corresponding co-ords for element
                elementIdx = (self.lineSize * rowIdx) + colIdx

                # USED FOR DEBUGGING ALGORITHM PURPOSES
                if elementIdx == 44:
                    pass

                if elementIdx == 37:
                    pass

                if elementIdx == 39:
                    pass

                if elementIdx == 2:
                    pass

                    # Insert function to test here, replace with 'pass' once finished!
                    #addr = self.getRowAddresses(3)
                    #digits = self.getGroupPossibleDigits(addr)
                    #self.nakedSingleAttemptPlace(digits, addr)

                # Algorithms to update possible digits
                # Special cases to progress the iteration

                # Attempts to place possible digits in row/column/square
                # Analyses possible digits in these groups
                colAddresses = self.getColAddresses(colIdx)
                colDigits = self.getGroupPossibleDigits(colAddresses)
                self.nakedSingleAttemptPlace(colDigits, colAddresses)
                self.nakedPairAttemptPlace(colDigits, colAddresses)

                squareAddresses = self.getSquareAddresses(squareIdx)
                squareDigits = self.getGroupPossibleDigits(squareAddresses)
                self.nakedSingleAttemptPlace(squareDigits, squareAddresses)
                self.nakedPairAttemptPlace(squareDigits, squareAddresses)

                # Special case for square and line interactions
                self.checkSquareLineInteractions(squareDigits, squareAddresses)

                # Brute forces possible digits from current row, column and square
                # Iterates through each digit, typically 1-9, to remove impossible combinations
                for digit in range(1, self.lineSize + 1):
                    # Skips loop iteration if the current digit is already deduced
                    if self.puzzle[elementIdx] == str(digit): continue
                    # use 'find' command - retrieve index, replace digit with zero if necessary!
                    rowFind = currentRow.find(str(digit))
                    colFind = currentCol.find(str(digit))
                    squareFind = currentSquare.find(str(digit))

                    # If any result isn't -1, the answer cannot be this digit!
                    if rowFind != -1 or colFind != -1 or squareFind != -1:
                        # Sets found digit to 0, eliminating the possible digit
                        self.possibleCells[elementIdx][digit - 1] = 0

                # If there is a single possible digit, the solution to this element is found!
                # Puzzle variable is updated, if a solution is found
                possibleDigit = self.checkPossibleDigits(elementIdx)
                if possibleDigit != -1 and self.puzzle[elementIdx] != str(possibleDigit): 
                    self.updatePuzzle(elementIdx, possibleDigit)


            rowAddresses = self.getRowAddresses(rowIdx)
            rowDigits = self.getGroupPossibleDigits(rowAddresses)
            self.nakedSingleAttemptPlace(rowDigits, rowAddresses)
            self.nakedPairAttemptPlace(rowDigits, rowAddresses)

    def getRowAddresses(self, rowIdx: int) -> list:
        # Returns a list of addresses for a given row
        elementList = []
        for xIdx in range(self.lineSize):
            # x Index adjusts column
            # Row index defines y coordinate
            # Size of line defines incremental amount
            elementList.append((self.lineSize * rowIdx) + xIdx)
        return elementList

    def getColAddresses(self, colIdx: int) -> list:
        # Returns a list of addresses for a given column
        elementList = []
        for yIdx in range(self.lineSize):
            # y Index adjusts row
            # Fixed x coordinate
            elementList.append((self.lineSize * yIdx) + colIdx)
        return elementList

    def getSquareAddresses(self, squareIdx: int) -> list:
        # Returns a list of element numbers - corresponding to a given square
        # Uses a modified 'getSquare' algorithm to determine indexes of the specified elements from said square
        elementList = []

        # Starting Co-ords for indexes
        startRowIdx = squareIdx // self.sudokuSize
        startColIdx = squareIdx % self.sudokuSize

        # y Index adjusts row
        for yIdx in range(self.sudokuSize):
            # x Index adjusts column
            for xIdx in range(self.sudokuSize):
                # Retrieves the element number in a square formation
                address = (self.lineSize * ((startRowIdx * self.sudokuSize) + yIdx)) + ((self.sudokuSize * startColIdx) + xIdx)
                elementList.append(address)

        return elementList

    def getGroupPossibleDigits(self, indexes: list) -> list:
        # Returns a 2D array of possible digits from a given group
        # Group is IMPLIED - not explicitly given - addresses are used instead!

        possibleDigitsArray = []
        # Gets data from the provided addresses
        for idx in indexes:
            possibleDigitsArray.append(self.possibleCells[idx])
        return possibleDigitsArray

    def nakedSingleAttemptPlace(self, group: list, addresses: list):
        # Naked single digits are single exposed digits which can be placed

        # Analyses the possible digits in a group of elements
        # Attempts to place a digit, if there's only a single location for it to go!

        # A list of digit occurances, updated if a possible digit is found in the group
        digitInstances = self.getDigitOccurances(group)
        
        for digit in range(1, self.lineSize + 1):
            if digitInstances[digit - 1] == 1:
                for elementIdx in range(self.lineSize):
                #    if digit in group[elementIdx]: self.updatePuzzle(addresses[elementIdx], digit) 
                    if digit in group[elementIdx]: 
                        address = addresses[elementIdx]
                        # Sends a list for compatibility with function
                        self.removeInvalidDigits(address, [digit])

    def getDigitOccurances(self, group: list) -> list:
        # Returns a list of appearances for each digit
        # Digit in question is the INDEX of appearance
        digitInstances = [0] * self.lineSize
        
        # Analyses each element from the group individually
        for element in group:
            for digitCheck in element: 
                # Increments the list at the indicated address, if a possible non-zero digit is found
                if digitCheck != 0: digitInstances[digitCheck - 1] += 1

        # Returns list, similar to a dictionary, with the index being the key
        return digitInstances

    def removeInvalidDigits(self, elementIdx: int, confirmedDigits: list):
            # When a digit is confirmed to be in an element, removes all other possible digits
            for digit in range(1, self.lineSize + 1):
                if digit not in confirmedDigits: self.possibleCells[elementIdx][digit - 1] = 0
                # Used when a valid digit is located
                else: self.possibleCells[elementIdx][digit - 1] = digit

    def nakedPairAttemptPlace(self, possibleDigitsGroup: list, addresses: list):
        # Checks a group to determine if a pair of elements contain the same two possible digits
        # Successful naked pairs constrain the location of said digits to somewhere in either element
        # As such, it is impossible for those digits to be contained elsewhere in the group!

        # A list of digit occurances, updated if a possible digit is found in the group
        digitInstances = self.getDigitOccurances(possibleDigitsGroup)

        # Temporary list to contain the naked pair
        instanceAdr = []

        for digit in range(1, self.lineSize + 1):
            # Locating 1st half of a potential naked pair
            if digitInstances[digit - 1] == 2:        
                for groupIdx in range(self.lineSize):
                    # Locates elements which uniquely share a potential digit
                    # Can lead to multiple naked pairs being loated - works one at a time!
                    if digit in possibleDigitsGroup[groupIdx]: instanceAdr.append(groupIdx) 
                
                # Checks for pairs of instances
                if len(instanceAdr) != 2: continue

                elementA = possibleDigitsGroup[instanceAdr[0]]
                elementB = possibleDigitsGroup[instanceAdr[1]]

                # Identifies instances of digits shared by the elements in question
                # List of occurances in the pair, values: 0, 1 or 2, looking for 2!
                # List length is TYPICALLY 9: for digits 1 - 9
                pairInstances = self.getDigitOccurances([elementA, elementB])
                for pairInstanceIdx in range(self.lineSize):
                    if pairInstances[pairInstanceIdx] == 2 and pairInstanceIdx != digit - 1 and digitInstances[pairInstanceIdx] == 2:
                        # This is a pair!!
                        self.removeInvalidDigits(addresses[instanceAdr[0]], [digit, pairInstanceIdx + 1])
                        self.removeInvalidDigits(addresses[instanceAdr[1]], [digit, pairInstanceIdx + 1])

                # Resets the list to check another pair
                instanceAdr.clear()

    def checkPossibleDigits(self, elementIdx: int) -> int:
        # Used to check if only a single digit is valid in a given element

        # Retrieves the possible digits for a given element
        digitArray = self.possibleCells[elementIdx]
        
        # Integers stored to monitor the number of applicable digits and respective indexes
        zeroCounter = 0
        nonZeroDigit = 0

        # Checks for non-zero digits
        for digitIdx in digitArray:
            if digitIdx == 0: zeroCounter += 1
            else: nonZeroDigit = digitIdx
        # Returns most recent non-zero digit
        # Only returns non-zero digit if the rest are all zeros (hence most recent non-zero digit)
        if zeroCounter == self.lineSize - 1: return nonZeroDigit
        else: return -1


    def checkSquareLineInteractions(self, square: list, addresses: list):
        # Checks square. If a group of digits are only valid on the same line (row or column):
        # Remove instances of digit in question from elsewhere in line (not in current square)
        
        digitAppearanceList = []
        coordinateList = []

        for digit in range(1, self.lineSize + 1):
            # Gets each instance of the possible digit and checks for lines
            for elementIdx in range(self.lineSize):
                # Adds locations of elements, for the digit in question, onto the list
                if digit in square[elementIdx]: 
                    digitAppearanceList.append(addresses[elementIdx])
                    # Stores x and y coordinates for shape analysis
                    coordinateList.append(self.getCoordinates(addresses[elementIdx]))

            # TODO: fix this, currently works incorrectly!!
            if coordinateList == []: 
                continue

            # Checks if potential digits all share the same row
            changeRow = self.getRowShape(coordinateList)
            if changeRow != -1: 
                rowAddresses = self.getRowAddresses(changeRow)
######################################## TODO: DON'T REMOVE DIGIT FROM CONFIRMED ELEMENT!!! ########################################
                for element in rowAddresses: 
                    if element not in digitAppearanceList: 
                        self.removePossibleDigit(element, digit)
            
            # Checks if potential digits all share the same column
            changeCol = self.getColShape(coordinateList)
            if changeCol != -1:
                colAddresses = self.getColAddresses(changeCol)    
                for element in colAddresses: 
                    if element not in digitAppearanceList: self.removePossibleDigit(element, digit)

            # Resets the list for each new digit
            digitAppearanceList.clear()
            coordinateList.clear()

    def removePossibleDigit(self, elementIdx: int, toRemove: int):
        # Removes a single invalid digit from the possible digits list
        for digitIdx in range(self.lineSize):
            if self.possibleCells[elementIdx][digitIdx] == toRemove:
                self.possibleCells[elementIdx][digitIdx] = 0


    def getCoordinates(self, address: int) -> list:
        # Converts an integer element address into a 2D coordinate
         
        # x uses modulus, y uses integer division
        xComponent = address % self.lineSize
       
        yComponent = address // self.lineSize
        # Stored in a list
        return [xComponent, yComponent]

    def getRowShape(self, coords: list) -> int:
        # Coordinates stored in a 2D array, using 0th element to check row
        rowNum = coords[0][1]
        for coordinate in coords:
            # If elements are located on separate rows, -1 is returned
            # This value will never be stored as a coordinate, so will be returned
            if coordinate[1] != rowNum: rowNum = -1

        # DEBUGGING:
        if rowNum != -1:
            pass

        # If row number is unchanged, a row has been located
        return rowNum
        

    def getColShape(self, coords: list) -> int:
        # Columns stored in the 1st element 
        colNum = coords[0][0]
        for coordinate in coords:
            # Checks if all elements share the same column
            if coordinate[0] != colNum: colNum = -1

        # DEBUGGING:
        if colNum != -1:
            pass

        # If row number is unchanged, a column has been located
        return colNum

    def updatePuzzle(self, elementIdx: int, digit: int):
        originalStr = self.puzzle[0 : self.puzzleSize]
        newStr = originalStr[0 : elementIdx] + str(digit) + originalStr[elementIdx + 1 : self.puzzleSize]
        self.puzzle = newStr

    def verifySolution(self) -> bool:
        # Returns boolean comparing current solution to intended one

        # Boolean generated through comparison
        if self.puzzle == self.solution: return True
        else: return False
    
    # Currently outdated or redundant functions
    def getSquareArray(self, squareNum):
        # Currently redundant - better version is 'getSquare'
        square = []
        startRowIdx = squareNum // self.sudokuSize
        startColIdx = squareNum % self.sudokuSize
        for offsetIdx in range(self.sudokuSize):
            square.append(list(self.getRow((self.sudokuSize * startRowIdx) + offsetIdx)[(self.sudokuSize * startColIdx) : (self.sudokuSize * startColIdx) + self.sudokuSize]))
        return square

    def removeInvalidDigitsSingle(self, elementIdx, confirmedDigit):

            # NOTE: redundant once 'removeInvalidDigits' is sorted

            # When a digit is confirmed to be in an element, removes all other possible digits
            for digit in range(1, self.lineSize + 1):
                if digit != confirmedDigit: self.possibleCells[elementIdx][digit - 1] = 0
                # Used when a SINGLE VALID DIGIT is located
                else: self.possibleCells[elementIdx][digit - 1] = digit

# Connecting to YouDoSudoku API - generates random Sudoku!
if __name__ == "__main__":

    customEnabled = True
    if customEnabled:
        # CUSTOMISABLE query to generate harder Sudokus
        body = {
            "difficulty": "hard",   # Options: "easy", "medium", or "hard" (defaults to "easy")
            "solution": True,       # True or False (defaults to True)
            "array": False          # True or False (defaults to False)
        }
        headers =  {"Content-Type":"application/json"}
        response = requests.post("https://youdosudoku.com/api/", json=body, headers=headers)
    else:     
        # BASIC query to send to website to generate Sudoku 
        # This uses default variables: 'easy', 'True' and 'False'   
        response = requests.get("https://youdosudoku.com/api/")

    # Ensures data is correctly received
    if response.status_code == 200:
        API_data = response.json()
    else:
        print(f"Error: {response.status_code}")

    # Optional debugging tools
    debugging = False
    if not debugging:
        # Generated puzzle and accompanying solution
        puzzle = API_data["puzzle"]
        solution = API_data["solution"]
    else:
        # Example values for debugging
        
        # Original unchanged puzzle
        puzzle = "104080020090000000600900000070500600000008090000430081000000500849700030503800000"
        
        # 37 digits solved:
    #    puzzle = "104680020090100800680900000078500640400208095000430081000300508849700030503800070"
        
        # Interesting puzzle useful for debugging:
       # puzzle = '000265300000804590000901600000749816746158923981326745000493168004587239893612457'

        solution = "134685927295147863687923154378519642461278395952436781726394518849751236513862479"

    newSudoku = Sudoku(puzzle, solution)
    #newSudoku.iteration()
    solved = newSudoku.attemptSolve()
    if solved: print("\nPassed!")
    else: print("\nFailed!")