from __future__ import annotations
from typing import Optional


class Environment:
    def __init__(self) -> None:
        self.ctx = {}

    def clone(self) -> Environment:
        ctx = self.ctx.copy()
        env = Environment()
        env.ctx = ctx
        return env

    def get(self, var: Var) -> Optional[Term]:
        out = self.ctx.get(var, None)
        return out

    def put(self, var: Var, term: Term):
        self.ctx[var] = term

    def __repr__(self) -> str:
        return f"{self.ctx}"


class Term:
    pass


class Nil(Term):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"NIL"

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Nil)

    def __hash__(self) -> int:
        return hash(("NIL",))


class Atom(Term):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name}"

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Atom) and self.name == value.name

    def __hash__(self) -> int:
        return hash(("Atom", self.name))


class Var(Term):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name}"

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Var) and self.name == value.name

    def __hash__(self) -> int:
        return hash(("Var", self.name))


class Cons(Term):
    def __init__(self, fst: Term, snd: Term) -> None:
        self.fst = fst
        self.snd = snd

    def __repr__(self) -> str:
        return f"({repr(self.fst)} . {repr(self.snd)})"

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Cons):
            return self.fst == value.fst and self.snd == value.snd
        return False


class Closure(Term):
    def __init__(self, params: Cons, code: Cons, env: Environment) -> None:
        self.params = params
        self.code = code
        self.env = env

    def __repr__(self) -> str:
        return f"Closure({self.params}, {self.code}, {self.env})"


def solve(t1: Term, t2: Term, env: Environment) -> tuple[bool, Environment]:
    # print("[DEBUG]", t1, t2, type(t1), type(t2))
    if isinstance(t1, Var) and isinstance(t2, Var):
        env.put(t1, t2)
        env.put(t2, t1)
        return True, env
    if isinstance(t1, Var):
        env.put(t1, t2)
        return True, env
    if isinstance(t2, Var):
        env.put(t2, t1)
        return True, env
    if isinstance(t1, Cons) and isinstance(t2, Cons):
        ok1, e1 = solve(t1.fst, t2.fst, env)
        if ok1:
            ok2, e2 = solve(t1.snd, t2.snd, e1)
            return ok1 or ok2, e2
        return ok1, e1
    return False, env


def apply(t: Term, env: Environment):
    if isinstance(t, Var):
        v = env.get(t)
        if v is not None:
            if isinstance(v, Var):
                d = env.get(v)
                if t == d:
                    return t
                return apply(v, env)
            return v
        return t
    if isinstance(t, Cons):
        return Cons(apply(t.fst, env), apply(t.snd, env))
    return t


def call(closure: Closure, arg: Term) -> Term:
    # 克隆环境，不污染原闭包
    new_env = closure.env.clone()
    # 参数 ↔ 实参 匹配
    ok, bind_env = solve(closure.params, arg, new_env)
    if not ok:
        raise Exception("Call Match failed")
    # 用绑定环境展开函数体
    return apply(closure.code, bind_env)
