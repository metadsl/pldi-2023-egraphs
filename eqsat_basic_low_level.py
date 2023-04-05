"""
Basic equality saturation example using the low-level API.
=========================================================
"""
from egg_smol.bindings import *

egraph = EGraph()
egraph.declare_sort("Math")
egraph.declare_constructor(Variant("Num", ["i64"]), "Math")
egraph.declare_constructor(Variant("Var", ["String"]), "Math")
egraph.declare_constructor(Variant("Add", ["Math", "Math"]), "Math")
egraph.declare_constructor(Variant("Mul", ["Math", "Math"]), "Math")

egraph.define(
    "expr1",
    Call(
        "Mul", [Call("Num", [Lit(Int(2))]), Call("Add", [Call("Var", [Lit(String("x"))]), Call("Num", [Lit(Int(3))])])]
    ),
)
egraph.define(
    "expr2",
    Call(
        "Add", [Call("Num", [Lit(Int(6))]), Call("Mul", [Call("Num", [Lit(Int(2))]), Call("Var", [Lit(String("x"))])])]
    ),
)
egraph.add_rewrite(Rewrite(Call("Add", [Var("a"), Var("b")]), Call("Add", [Var("b"), Var("a")])))

lhs = Call("Mul", [Var("a"), Call("Add", [Var("b"), Var("c")])])
rhs = Call("Add", [Call("Mul", [Var("a"), Var("b")]), Call("Mul", [Var("a"), Var("c")])])
egraph.add_rewrite(Rewrite(lhs, rhs))


lhs = Call("Add", [Call("Num", [Var("a")]), Call("Num", [Var("b")])])
rhs = Call("Num", [Call("+", [Var("a"), Var("b")])])
egraph.add_rewrite(Rewrite(lhs, rhs))

lhs = Call("Mul", [Call("Num", [Var("a")]), Call("Num", [Var("b")])])
rhs = Call("Num", [Call("*", [Var("a"), Var("b")])])
egraph.add_rewrite(Rewrite(lhs, rhs))

egraph.run_rules(10)
egraph.check_fact(Eq([Var("expr1"), Var("expr2")]))
