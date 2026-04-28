from terms import Atom, Closure, Environment, Nil, Var, Cons, apply, call, solve


def test1():
    env = Environment()
    nil = Nil()
    X = Var("X")
    Y = Var("Y")
    Z = Var("Z")
    f = Cons(X, Cons(Y, Z))
    g = Cons(Cons(Atom("a"), nil), Cons(Y, Cons(Atom("c"), nil)))
    r, env = solve(X, nil, env)
    print(r, env)
    r, env = solve(f, g, env)
    print(r, env)
    r = apply(f, env)
    print(r, env)


def test2():
    # 变量
    x = Var("x")
    y = Var("y")

    # 参数：(x . y)
    params = Cons(x, y)

    # 函数体：(x . y)
    body = Cons(y, x)

    # 空环境闭包
    env = Environment()
    f = Closure(params, body, env)

    # 调用：f (1 . (2 . nil))
    a1 = Atom("1")
    a2 = Atom("2")
    nil = Atom("nil")
    arg = Cons(a1, Cons(a2, nil))

    # 执行
    print("[Call]", call(f, arg))


def tests():
    test1()
    test2()


if __name__ == "__main__":
    tests()
