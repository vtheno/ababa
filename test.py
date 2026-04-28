from terms import *


class DB:
    def __init__(self, rules: list[Term]) -> None:
        self.rules = rules

    def prove(self, goal: Term, e: Environment):
        checkpoints = []
        for rule in self.rules:
            if isinstance(goal, Cons) and isinstance(rule, Cons):
                # print(goal, rule)
                ok, new_e = solve(goal, rule.fst, e.clone())
                if ok:
                    checkpoints.append((ok, new_e, apply(rule.snd, new_e)))
                # print(ok, new_e)
        return checkpoints


nil = Nil()
e = Environment()
X = Var("X")
Y = Var("Y")
Z = Var("Z")
W = Var("W")

zero = Atom("0")
nat = Atom("nat")
succ = Atom("succ")


# r = solve(Cons(X, nil), Cons(Cons(zero, nil), nil), e)
# print(r)
def test1():
    db = DB(
        [
            Cons(Cons(nat, zero), nil),
            Cons(Cons(nat, Cons(X, nil)), Cons(X, X)),
        ]
    )
    print("=" * 50)
    r = db.prove(Cons(nat, zero), e)
    print(r)
    print("=" * 50)
    r = db.prove(Cons(nat, Cons(zero, nil)), e)
    print(r)
    print("=" * 50)
    r = db.prove(Cons(nat, Cons(zero, Cons(zero, nil))), e)
    print(r)
    print("=" * 50)
    r = db.prove(Cons(nat, Cons(Cons(zero, nil), nil)), e)
    print(r)
    print("=" * 50)


def test2():
    e = Environment()
    """
    nat(0).
    nat(succ(X)) :- nat(X).
    """
    nat_zero = Cons(Cons(nat, zero), Cons(nat, zero))
    nat_succ = Cons(Cons(nat, Cons(succ, X)), Cons(nat, X))
    db = DB([nat_zero, nat_succ])

    print("=" * 50)
    goal = Cons(nat, Cons(succ, zero))
    r = db.prove(goal, e)
    print(r)
    print("=" * 50)
    goal = Cons(nat, Cons(succ, Cons(succ, zero)))
    r = db.prove(goal, e)
    print(r)


test2()
