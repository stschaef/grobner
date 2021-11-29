import copy

def lexicographic_helper(a, b):
    assert(len(a) == len(b))
    if len(a) == 0:
        return 0
    if a[0] == b[0]:
        return lexicographic_helper(a[1:], b[1:])
    if a[0] < b[0]:
        return -1
    if a[0] > b[0]:
        return 1

def lexicographic_order(a, b):
    return lexicographic_helper(a.degrees, b.degrees)

order = lexicographic_order
variables = ["x", "y"]
        
class Monomial:
        """A coefficient and degree list.
        
        len(degrees) == len(variables)
        """
        def __init__(self, degrees, coefficient=1):
            self.degrees = degrees
            self.coefficient = coefficient
        
        def __mul__(self, other):
            degs = [a + b for (a, b) in zip(self.degrees, other.degrees)]
            c = self.coefficient * other.coefficient
            return Monomial(degs, coefficient=c)

        def __repr__(self):
            return "<degrees: " + str(repr(self.degrees)) + ", coeff: " + str(repr(self.coefficient)) + ">"
        
        def __str__(self):
            s = f"{self.coefficient} " 
            for i, x in enumerate(variables):
                s += f"{str(x)}^{self.degrees[i]} "
            return s
        
        def __lt__(self, other):
            return order(self, other) == -1

        def __gt__(self, other):
           return order(self, other) == 1

        def __eq__(self, other):
            return order(self, other) == 0

        def __le__(self, other):
            return order(self, other) < 1

        def __ne__(self, other):
            return order(self, other) != 0

        def __ge__(self, other):
            return order(self, other) > -1

        
class Polynomial:
    """A sum of monomials. 
    
    Attributes:
    monomials: a list of Monomial objects.
    """

    def __init__(self, monomials):
        self.monomials = sorted(monomials, reverse=True)
        self.simplify()

    def from_string(s):
        """Read in a monomial from a string. Do this assuming that the string is in the following format:
        
        [coeff] [string]^[int] ... [string]^int, delimited by +
        """
        monomial_strings = s.split("+")
        mons = []
        # print(monomial_strings)
        for m_s in monomial_strings:
            mono_data = m_s.split()
            coeff = int(mono_data[0])
            degs = []
            for substr in mono_data[1:]:
                degs.append(int(substr.split("^")[1]))
            mons.append(Monomial(degs, coefficient=coeff))
        return Polynomial(mons)

    def __str__(self):
        s = ""
        first = True
        for i, f in enumerate(self.monomials):
            if f.coefficient != 0:
                if not first:
                    s += "+ " 
                else:
                    first = False
                s += str(f)
            
        return s.strip() if s != "" else str(0)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def combine_like_terms(self):
        if len(self.monomials) == 1: 
            return 
        i, j = 0, 0
        c = 0
        mons = []
        while j < len(self.monomials):
            # here == means monomial order, not algebraic equality
            while self.monomials[i] == self.monomials[j]:
                c += self.monomials[j].coefficient
                j += 1
                if j == len(self.monomials):
                    mons.append(Monomial(self.monomials[i].degrees, coefficient=c))
                    c = 0
                    self.monomials = mons
                    return
            mons.append(Monomial(self.monomials[i].degrees, coefficient=c))
            c = 0
            i = j
        self.monomials = mons

    def get_rid_of_zeros(self):
        for mon in self.monomials:
            if mon.coefficient == 0:
                self.monomials.remove(mon)

    def simplify(self):
        self.combine_like_terms()
        self.get_rid_of_zeros()
            
    def __mul__(self, other):
        """Multiply two polynomials."""
        s_mons = copy.deepcopy(self.monomials)
        g_mons = copy.deepcopy(other.monomials)

        mons = []
        for f in s_mons:
            for g in g_mons:
                mons.append(f * g)
        return Polynomial(mons)

    def __add__(self, other):
        mons = copy.deepcopy(self.monomials)
        mons.extend(other.monomials)
        return Polynomial(mons)
    
    def __sub__(self, other):
        return copy.deepcopy(self + Polynomial([Monomial([0 for _ in variables], -1)]) * other)

    def __eq__(self, other):
        if len(other.monomials) != len(self.monomials):
            return False
        for f, g in zip(self.monomials, other.monomials):
            if f != g:
                return False
        return True

# f = Polynomial.from_string("1 x^0 y^0 + 2 x^1 y^1")
# g = Polynomial.from_string("1 x^0 y^0 + 2 x^1 y^2")
