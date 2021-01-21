from csp_solver import *
if __name__ == '__main__':
    n_of_queens = 12
    n_of_sudoku = 3
    k = 30
    # no inference strategy battery test
    # x: test number; y: test counter
    file = open('./result.txt', 'w+')
    sudoku_data = []
    queen_data = []
    for i in range(k):
        backtrack(s := create_n_sudoku(n_of_sudoku), no_inference)
        backtrack(q := create_n_queen(n_of_queens), no_inference)
        sudoku_data.append(s.explorations)
        queen_data.append(q.explorations)
    file.write(f"Sudoku, no inference: {sum(sudoku_data) / len(sudoku_data)}")
    file.write(f"\n{sudoku_data}")
    file.write(f"\nQueens, no inference: {sum(queen_data) / len(queen_data)}")
    file.write(f"\n{queen_data}")

    sudoku_data.clear()
    queen_data.clear()
    for i in range(k):
        backtrack(s := create_n_sudoku(n_of_sudoku), forward_checking)
        backtrack(q := create_n_queen(n_of_queens), forward_checking)
        sudoku_data.append(s.explorations)
        queen_data.append(q.explorations)
    file.write(f"Sudoku, forward checking: {sum(sudoku_data) / len(sudoku_data)}")
    file.write(f"{sudoku_data}")
    file.write(f"Queens, fc: {sum(queen_data) / len(queen_data)}")
    file.write(f"{queen_data}")

    sudoku_data.clear()
    queen_data.clear()
    for i in range(k):
        backtrack(s := create_n_sudoku(n_of_sudoku), maintain_arc_consistncy)
        backtrack(q := create_n_queen(n_of_queens), maintain_arc_consistncy)
        sudoku_data.append(s.explorations)
        queen_data.append(q.explorations)
    file.write(f"\n\nSudoku, mac: {sum(sudoku_data) / len(sudoku_data)}")
    file.write(f"\n{sudoku_data}")
    file.write(f"\nQueens, mac: {sum(queen_data) / len(queen_data)}")
    file.write(f"\n{queen_data}")
    file.close()
