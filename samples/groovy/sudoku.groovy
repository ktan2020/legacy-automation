/**
 * Sudoku solver
 */

// the games to solve
def games = [
    "   1    5  7 48  2 2 9    7 3   29  5       4  68   1 8    1 4 6  28 5  1    4   ",
    "   897     9     1  6 1  9  3     2    574    1     6  8  2 7  5     9     763   ",
    "5   1 9  73 2    5    6  7    5  8  8       3  4  7    1  8    2    1 69  6 7   4",
    " 7  4  63  2  9 4 5     8      7 3  9  8 6  7  8 5      7     2 1 4  7  69  2  3 ",
    "57  9 18  3      4 8    6    24 5               6 95    5    9 3      2  91 3  75",
    " 7  4  63  2  9 4 5     8      7 3  9  8 6  7  8 5      7     2 1 4  7  69  2  3 ",
    "18    4     8       9 345   4 96    52  8  76    53 1   251 7       2     7    92",
    " 6  3     459   28  8   73     9  5 9  8 6  7 8  5     36   9  42   938     2  1 ",
    "  14         786 1    5 9   8     23 13   56 95     7   5 4    3 918         73  ",
    "7 5 2   3  35     4  7    6    3 82           62 9    3    8  9     41  1   7 3 2",
    "  1  74      2  966  3      57  89  93     51  69  27      6  582  7      52  8  ",
    "  73  2  3       18  62     734    5         5    849     67  42       6  9  43  "
]

def solver = new Backtracker()

solver.isSolution = { theGame ->
    def numbersSolved = 0
    for (i in 0..<9) {
        for (j in 0..<9) {
            if (theGame.grid[i][j].value) numbersSolved++
        }
    }
    return numbersSolved == 81
}

solver.possibilities = { theGame ->

    playSingleCandidates(theGame)
   
    if (solver.isSolution(theGame)) {
        return [theGame]
    } else {
        def position = getPositionWithLowestNumberOfCandidates(theGame)
        def candidates = theGame.grid[position[0]][position[1]].candidates
        return candidates.collect{
            def possibleGrid = new Grid(theGame)
            possibleGrid.play(it, position[0], position[1])
            return possibleGrid
        }       
    }
}

Grid playSingleCandidates(Grid game) {
    def player = {
        def counter = 0     
        for (i in 0..<9) {
            for (j in 0..<9) {
                if (game.grid[i][j].candidates.size() == 1) {
                    game.play(game.grid[i][j].candidates[0], i, j)
                    counter++
                }
            }
        }   
        return counter
    }   
    while (true) {
        if (player() == 0) break
    }
}

List getPositionWithLowestNumberOfCandidates(Grid game) {
    def position = [0,0]
    def lowestNumberOfCandidates = 9
    for (i in 0..<9) {
        for (j in 0..<9) {
            def cell = game.grid[i][j]
            if (cell.value == null && cell.candidates.size() < lowestNumberOfCandidates) {
                position = [i,j]
                lowestNumberOfCandidates = cell.candidates.size()
            }
        }
    }
    return position
}

games.each{ game ->
    def grid = new Grid()
    grid.loadGame(game)

    def start = System.currentTimeMillis()
    def solution = solver.solve(grid)

    if (solution)
        println solution.toString()
    else
        println "No solution found"

    println "\nSolved in ${System.currentTimeMillis() - start}ms with ${solver.stages} steps and ${solver.backtracks} backtracks"
}

class Cell implements Cloneable {
    def value
    def candidates = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
   
    Object clone() {
        def newCell = new Cell()
        newCell.value = value
        newCell.candidates = candidates.clone()
        return newCell
    }
}

class Grid {
    def grid = [[], [], [], [], [], [], [], [], []]
   
    Grid() {
        for(i in 0..<9)
            for (j in 0..<9)
                grid[i][j] = new Cell()
    }
   
    Grid(Grid g) {
        for(i in 0..<9)
            for (j in 0..<9)
                grid[i][j] = g.grid[i][j].clone()       
    }
   
    void loadGame(String game) {
        def counter = 0
        for(c in game) {
            if (c ==~ "[1-9]")
                play(c, counter.intdiv(9), counter % 9)
            counter++
        }
    }
   
    void play(number, line, column) {
        def cell = grid[line][column]
        cell.value = number
        cell.candidates = []
        removeCandidateFromLine([number], line)
        removeCandidateFromColumn([number], column)
        removeCandidateFromBlock([number], line, column)
    }
   
    private void removeCandidateFromLine(candidates, line) {
        for (i in 0..<9)
            grid[line][i].candidates = grid[line][i].candidates - candidates
    }
   
    private void removeCandidateFromColumn(candidates, column) {
        for (i in 0..<9)
            grid[i][column].candidates = grid[i][column].candidates - candidates
    }
   
    private void removeCandidateFromBlock(candidates, line, column) {
        for (i in 0..<3)
            for (j in 0..<3) {
                def x = i + 3*(line.intdiv(3))
                def y = j + 3*(column.intdiv(3))
                grid[x][y].candidates = grid[x][y].candidates - candidates
            }
    }
   
    String candidatesToString() {
        def sb = new StringBuffer()
        for(i in 0..<9) {
            sb << (i % 3 == 0 ? "\n+" + ("-" * 27 + "+") * 3 : "") + "\n"
            for (j in 0..<9) {
                if (j % 3 == 0) sb << "|"
                def cell = grid[i][j]
                sb << cell.candidates.join('').center(9)
            }
            sb << "|"
        }
        sb << "\n+" + ("-" * 27 + "+") * 3 + "\n"
        return sb.toString()
    }

    String toString() {
        def sb = new StringBuffer()
        for(i in 0..<9) {
            sb << (i % 3 == 0 ? "\n+---+---+---+\n" : "\n")
            for (j in 0..<9) {
                if (j % 3 == 0) sb << "|"
                def cell = grid[i][j]
                sb << (cell.value ? cell.value : " ")
            }
            sb << "|"
        }
        sb << "\n+---+---+---+\n"
        return sb.toString()
    }
   
    boolean equals(Object obj) {
        this.hashCode() == obj?.hashCode()     
    }
   
    int hashCode() {
        def sb = new StringBuffer()
        for(i in 0..<9)
            for (j in 0..<9)
                sb << (grid[i][j].candidates + grid[i][j].value)
        return sb.toString().hashCode()
    }
}

class Backtracker {
    def possibilities
    def isSolution
    def stages = 0
    def backtracks = 0
 
    def solve(possibility) {
        def steps = []
        doSolveRecurse(steps, possibility)
    }
 
    private doSolveRecurse(List steps, currentPossibility) {
        if (isSolution(currentPossibility)) {
            return currentPossibility
        } else {
            stages++
            def allPossibilities = possibilities(currentPossibility)
            if (allPossibilities.size() > 0) {
                steps << currentPossibility
            } else {
                // we've backtracked all the way to the root, so there's no solution
                if (steps.size() <= 1) return null
                def popped = steps.pop()
                backtracks++
            }
            for(possibility in allPossibilities) {
                def value = doSolveRecurse(steps, possibility)
                if (value != null) return value
            }           
        }
    }   
}