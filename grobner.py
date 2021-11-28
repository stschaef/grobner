"""
Compute a grobner basis

For simplicity, assume we are working over Z (or some quotient thereof)
This is reasonable as rationals can have their denominators cleared, 
and things like R are messy so we need not bother
"""
import copy
from polynomial import Polynomial, Monomial, order, variables

def is_multiple(a, b):
    """Return true if Monomial a is a multiple of Monomial b."""
    if a.coefficient == 0:
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
            return True, i
    return False, -1

def reduce(f, g):
    """Reduce f by g."""
    can, i = can_reduce(f, g)
    if not can:
        return
    m = f.monomials[i]

    deg_def = [a - b for (a, b) in zip(m.degrees, g.monomials[0].degrees)]
    h = Polynomial([Monomial(deg_def, coefficient=m.coefficient / g.monomials[0].coefficient)])
    return f - h * g

def degree_lcm(a, b):
    degs = [max(deg1, deg2) for (deg1, deg2) in zip(a.degrees, b.degrees)]
    return degs

def is_zero(p):
    for mono in p.monomials:
        if mono.coefficient != 0:
            return False
    return True

def keep_reducing(f, grob, orig_grob):
    did_add = False
    for poly in orig_grob:
        if can_reduce(f, poly)[0]:
            h = reduce(f, poly)
            if not is_zero(h):
                did_add = True
                grob.append(h)
                keep_reducing(h, grob, orig_grob)
    if not did_add and not is_zero(f):
        grob.append(f)


def buchberger(gen_set):
    grobner = gen_set
    pairs = [(i, j) for i in range(len(grobner)) for j in range(i)]
    n = len(grobner)
    S = {}
    for i, pair in enumerate(pairs):
        f_0 = grobner[pair[0]]
        f_1 = grobner[pair[1]]
        g_0 = f_0.monomials[0]
        g_1 = f_1.monomials[0]
        a = degree_lcm(g_0, g_1)
        h_0 = Polynomial([Monomial([deg1 - deg2 for (deg1, deg2) in zip(a, g_0.degrees)], coefficient=g_1.coefficient)])
        h_1 = Polynomial([Monomial([deg1 - deg2 for (deg1, deg2) in zip(a, g_1.degrees)], coefficient=g_0.coefficient)])
        print(h_0)
        print(h_1)
        S[pair] =  h_1 * f_1 - h_0 * f_0
        print(S)

        keep_reducing(S[pair], grobner, copy.deepcopy(grobner))
        print(grobner)
        pairs.extend([(i, j) for i in range(n, len(grobner)) for j in range(i)])
        n = len(grobner)
        pairs.remove(pair)
    # print(pairs

f = Polynomial.from_string("1 x^2 y^0 + 2 x^1 y^2")
g = Polynomial.from_string("1 x^1 y^1 + 2 x^0 y^3 + -1 x^0 y^0")

buchberger([f, g])

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