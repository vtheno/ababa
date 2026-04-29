from terms import *


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
    nat_zero = Cons(Cons(nat, zero), nil)
    nat_succ = Cons(Cons(nat, Cons(succ, X)), Cons(nat, X))
    db = DB([nat_zero, nat_succ])

    print("=" * 50)
    goal = Cons(nat, Cons(succ, zero))
    r = list(db.prove(goal, e))
    print(r)
    print("=" * 50)
    goal = Cons(nat, Cons(succ, Cons(succ, zero)))
    r = list(db.prove(goal, e))
    print(r)


def test_grandfather():
    print("\n=== grandfather test ===")
    env = Environment()
    X = Var("X")
    Y = Var("Y")
    Z = Var("Z")
    john = Atom("john")
    bob = Atom("bob")
    tom = Atom("tom")
    alice = Atom("alice")
    father = Atom("father")
    grandfather = Atom("grandfather")
    nil = Nil()

    f1 = Cons(Cons(father, Cons(john, Cons(bob, nil))), nil)
    f2 = Cons(Cons(father, Cons(bob, Cons(tom, nil))), nil)
    f3 = Cons(Cons(father, Cons(bob, Cons(alice, nil))), nil)
    body = Cons(
        Cons(father, Cons(X, Cons(Z, nil))),
        Cons(Cons(father, Cons(Z, Cons(Y, nil))), nil),
    )
    g_rule = Cons(Cons(grandfather, Cons(X, Cons(Y, nil))), body)
    db = DB([f1, f2, f3, g_rule])
    for r in db.rules:
        print(r)

    goal = Cons(father, Cons(X, Cons(tom, nil)))
    r = db.prove(goal, env)
    print(r)
    goal = Cons(grandfather, Cons(X, Cons(tom, nil)))
    r = db.prove(goal, env)
    print(r)


test1()
test2()
test_grandfather()
