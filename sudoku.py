"""n x n Sudoku

Intended to be solved via grobner bases.
"""
import grobner
import polynomial
from tabulate import tabulate

class Sudoku:
    def __init__(self, n):
        self.n = n
        self.board = [[0 for _ in range(self.n * self.n)] for _ in range(self.n * self.n)]
        polynomial.variables = [f"x_{{{i},{j}}}" for i in range(1, self.n**2 + 1) for j in range(1, self.n**2 + 1)]
        print(polynomial.variables)

    def pretty_print(self):
        print(tabulate(s.board, tablefmt="grid"))

    def get_index(self, i, j):
        return i * self.n * self.n + j

    
    def board_to_polynomials(self):
        polys = []

        # Ensure each polynomial takes on proper values
        # Include (z - 1)(z - 2)...(z - self.n**2) = 0, z = x_{i,j} for all i,j
        for i in range(self.n**2):
            for j in range(self.n**2):
                p = polynomial.Polynomial([polynomial.Monomial([0 for _ in polynomial.variables], coefficient=1)])
                for k in range(self.n**2):
                    degs = [0 for _ in polynomial.variables]
                    degs[self.get_index(i, j)] = 1
                    linear_term = polynomial.Monomial(degs, coefficient=1)
                    constant_term = polynomial.Monomial([0 for _ in polynomial.variables], coefficient=-(k + 1))
                    q = polynomial.Polynomial([linear_term, constant_term])
                    p = p * q
                polys.append(p)

        # Ensure give clues give proper solution
        # Include (x_{i,j} - a) = 0 if clue is board[i][j] = a
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val == 0: continue
                degs = [0 for _ in polynomial.variables]
                degs[self.get_index(i, j)] = 1
                linear_term = polynomial.Monomial(degs, coefficient=1)
                constant_term = polynomial.Monomial([0 for _ in polynomial.variables], coefficient=-val)
                polys.append(polynomial.Polynomial([linear_term, constant_term]))
        
        # Each subsquare must have unique values
        # Can achieve this through prodcut and sum relations
        # An earlier set of polynomials has guaranteed that values occur in {1, ..., n**2}
        # Using this and the following relations guarantees uniqueness:
        #   \sum x_{i,j} - \sum_1^{n**2} k = 0
        #   \prod x_{i,j} - \prod_1^{n**2} k = 0 
        # We may then do the same for rows/cols
        val_sum = 0
        val_prod = 1
        for i in range(1, self.n**2 + 1):
            val_sum += i
            val_prod *= i
    
        # subsquares
        for i in range(0, self.n**2, self.n):
            for j in range(0, self.n**2, self.n):
                p_sum = polynomial.Polynomial([polynomial.Monomial([0 for _ in polynomial.variables], coefficient=0)])
                p_prod = polynomial.Polynomial([polynomial.Monomial([0 for _ in polynomial.variables], coefficient=1)])
                for x in range(self.n):
                    for y in range(self.n):
                        degs = [0 for _ in polynomial.variables]
                        degs[self.get_index(i + x, j + y)] = 1
                        q = polynomial.Polynomial([polynomial.Monomial(degs, coefficient=1)])

                        p_sum = p_sum + q
                        p_prod = p_prod * q
                zero_degs = [0 for _ in polynomial.variables]
                p_sum = p_sum + polynomial.Polynomial([polynomial.Monomial(zero_degs, coefficient=-val_sum)])   
                p_prod = p_prod + polynomial.Polynomial([polynomial.Monomial(zero_degs, coefficient=-val_prod)])
                polys.append(p_sum)   
                polys.append(p_prod) 

        # rows
        for i in range(self.n**2):
            p_sum = polynomial.Polynomial([polynomial.Monomial([0 for _ in polynomial.variables], coefficient=0)])
            p_prod = polynomial.Polynomial([polynomial.Monomial([0 for _ in polynomial.variables], coefficient=1)])
            for j in range(self.n**2):
                degs = [0 for _ in polynomial.variables]
                degs[self.get_index(i, j)] = 1
                q = polynomial.Polynomial([polynomial.Monomial(degs, coefficient=1)])

                p_sum = p_sum + q
                p_prod = p_prod * q
            zero_degs = [0 for _ in polynomial.variables]
            p_sum = p_sum + polynomial.Polynomial([polynomial.Monomial(zero_degs, coefficient=-val_sum)])   
            p_prod = p_prod + polynomial.Polynomial([polynomial.Monomial(zero_degs, coefficient=-val_prod)])
            polys.append(p_sum)   
            polys.append(p_prod) 

        # columns
        for j in range(self.n**2):
            p_sum = polynomial.Polynomial([polynomial.Monomial([0 for _ in polynomial.variables], coefficient=0)])
            p_prod = polynomial.Polynomial([polynomial.Monomial([0 for _ in polynomial.variables], coefficient=1)])
            for i in range(self.n**2):
                degs = [0 for _ in polynomial.variables]
                degs[self.get_index(i, j)] = 1
                q = polynomial.Polynomial([polynomial.Monomial(degs, coefficient=1)])

                p_sum = p_sum + q
                p_prod = p_prod * q
            zero_degs = [0 for _ in polynomial.variables]
            p_sum = p_sum + polynomial.Polynomial([polynomial.Monomial(zero_degs, coefficient=-val_sum)])   
            p_prod = p_prod + polynomial.Polynomial([polynomial.Monomial(zero_degs, coefficient=-val_prod)])
            polys.append(p_sum)   
            polys.append(p_prod)
        
        return polys

        

    def solve(self):
        return grobner.buchberger(self.board_to_polynomials())

                



s = Sudoku(2)
s.board[1][3] = 1
s.board[2][1] = 1
s.board[2][3] = 2
s.board[3][0] = 3
s.board[3][1] = 2
s.board[2][0] = 4
s.board[2][2] = 3
s.board[3][2] = 1
s.board[3][3] = 4
s.board[0][3] = 3
s.board[0][0] = 1
s.board[1][0] = 2
s.board[1][1] = 3
s.board[0][1] = 4
s.board[0][2] = 2
s.pretty_print()
print(s.solve())
