"""
Basic equality saturation example.
==================================
"""
from __future__ import annotations

from egg_smol import *

egraph = EGraph()


@egraph.class_
class Num(BaseExpr):
    def __init__(self, value: i64Like) -> None:
        ...

    @classmethod
    def var(cls, name: StringLike) -> Num:
        ...

    def __add__(self, other: Num) -> Num:
        ...

    def __mul__(self, other: Num) -> Num:
        ...


# expr1 = 2 * (x + 3)
expr1 = egraph.define(
    "expr1",
    Num(2) * (Num.var("x") + Num(3)),
)
# expr2 = 6 + 2 * x
expr2 = egraph.define(
    "expr2",
    Num(6) + Num(2) * Num.var("x"),
)

a, b, c = vars_("a b c", Num)
i, j = vars_("i j", i64)
egraph.register(
    rewrite(a + b).to(b + a),
    rewrite(a * (b + c)).to((a * b) + (a * c)),
    rewrite(Num(i) + Num(j)).to(Num(i + j)),
    rewrite(Num(i) * Num(j)).to(Num(i * j)),
)
egraph.run(10)
egraph.check(eq(expr1).to(expr2))
