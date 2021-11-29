"""
Compute a grobner basis

For simplicity, assume we are working over Z (or some quotient thereof)
This is reasonable as rationals can have their denominators cleared, 
and things like R are messy so we need not bother
"""
import copy
from polynomial import Polynomial, Monomial, order, variables

# TODO: reduce polys mod G at each step

def is_multiple(a, b):
    """Return true if Monomial a is a multiple of Monomial b."""
    if a.coefficient == 0 or b.coefficient == 0:
        return False
    for (deg1, deg2) in zip(a.degrees, b.degrees):
        if deg1 < deg2:
            return False
    return True

def can_reduce(f, g):
    """Return true if some monomial m in f is reducible by leading monomial of g."""
    for i, m in enumerate(f.monomials):
        if is_multiple(m, g.monomials[0]):
            print(i)
            # print("F", f)
            # print("g", g)
            return True, i
    return False, -1

def reduce(f, g):
    """Reduce f by g."""
    can, i = can_reduce(f, g)
    if not can:
        return
    m = f.monomials[i]

    deg_def = [a - b for (a, b) in zip(m.degrees, g.monomials[0].degrees)]
    h = Polynomial([Monomial(deg_def, coefficient=int(m.coefficient / g.monomials[0].coefficient))])
    return f - h * g

def degree_lcm(a, b):
    degs = [max(deg1, deg2) for (deg1, deg2) in zip(a.degrees, b.degrees)]
    return degs

def is_zero(p):
    for mono in p.monomials:
        if mono.coefficient != 0:
            return False
    return True

def keep_reducing(f, grob_set):
    did_add = False
    # g = copy.deepcopy(grob_set)
    for poly in copy.deepcopy(grob_set):
        h = f
        while can_reduce(h, poly)[0]:
            h = reduce(h, poly)
            if not is_zero(h):
                did_add = True
                grob_set.add(h)
            
    if not did_add and not is_zero(f) and f not in grob_set:
        grob_set.add(f)

def S_polynomial(f_i, f_j):
    """Calculate the S-polynomial for two given members of the current Grobner basis.
    
    f_i, f_j \in G
    g_i the leading term of f_i
    a_ij = lcm(g_i, g_j)
    S_ij = (a_ij / g_i) f_i - (a_ij / g_j) f_j

    This is crafted so leading terms cancel out
    """
    # leading terms
    g_i = f_i.monomials[0]
    g_j = f_j.monomials[0]

    a = degree_lcm(g_i, g_j)
    h_i = Polynomial([Monomial([deg1 - deg2 for (deg1, deg2) in zip(a, g_i.degrees)], coefficient=g_i.coefficient)])
    h_j = Polynomial([Monomial([deg1 - deg2 for (deg1, deg2) in zip(a, g_j.degrees)], coefficient=g_j.coefficient)])
    if is_zero(h_i) or is_zero(h_j):
        return Polynomial([])
    return  h_j * f_j - h_i * f_i


def buchberger(gen_set):
    """Return a Grobner basis for a given generating set.
    
    TODO: This does not adequately handle elements that are equivalent mod G.
    That is, x and -x are both in the outputted basis for a particular example. For large
    bases, this may be problematic, as there could be numerous relations mod G that should 
    be quotiented away.
    
    Perhaps this isn't a problem ... processor go brr"""
    print(gen_set)
    grobner = set(gen_set)
    print(grobner)

    S = dict()

    def all_pairs_considered():
        for f_i in grobner:
            for f_j in grobner:
                if f_i == f_j:
                    continue 
                if (f_i, f_j) not in S.keys():
                    return False
        return True

    while not all_pairs_considered():
        for f_i in copy.deepcopy(grobner):
            for f_j in copy.deepcopy(grobner):
                if f_i == f_j or (f_i, f_j) in S.keys():
                    continue
                S[(f_i, f_j)] = S_polynomial(f_i, f_j)
                keep_reducing(S[(f_i, f_j)], grobner)

    return grobner

# f = Polynomial.from_string("1 x^2 y^0 + 2 x^1 y^2")
# g = Polynomial.from_string("1 x^1 y^1 + 2 x^0 y^3 + -1 x^0 y^0")
# h = Polynomial.from_string("1 x^1 y^1 + 2 x^0 y^3 + -1 x^0 y^0")


# buchberger([f, g, h])

# f = Polynomial.from_string("2 x^3 y^0 + -1 x^2 y^1 + 1 x^0 y^3 + 3 x^0 y^1")
# g1 = Polynomial.from_string("1 x^2 y^0 + 1 x^0 y^2 + -1 x^0 y^0")
# g2 = Polynomial.from_string("1 x^1 y^1 + -2 x^0 y^0")

# # print(f)
# # print(g1)
# # print(g2)
# f1 = reduce(f, g1)
# print("f1", f1)
# fa = reduce(f1, g1)
# print("fa", fa)
# f3 = reduce(fa, g2)
# print(f3)