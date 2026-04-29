from __future__ import annotations
from typing import Optional, List, TypeVar

T = TypeVar("T")


def all_permutations(arr):
    """
    生成 长度 2 ~ len(arr) 的所有全排列
    顺序：两两、三三、四四...
    """
    result = []
    n = len(arr)

    # 生成长度 2 ~ n 的所有排列
    for length in range(2, n + 1):
        current = []
        backtrack(arr, length, [False] * n, [], current)
        result.extend(current)

    return result


def backtrack(arr, length, used, path, result):
    """
    回溯：生成固定长度的全排列
    【顺序完全符合你的要求】
    """
    if len(path) == length:
        result.append(path.copy())
        return

    for i in range(len(arr)):
        if not used[i]:
            used[i] = True
            path.append(arr[i])
            backtrack(arr, length, used, path, result)
            path.pop()
            used[i] = False


def combinations(arr, k):
    """
    手写纯组合：不重复、不考虑顺序
    满足 A ∧ B = B ∧ A
    完全符合逻辑与的语义！
    """
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path.copy())
            return
        for i in range(start, len(arr)):
            path.append(arr[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def all_combinations(arr):
    """生成 2、3...n 长度的所有组合"""
    res = []
    for k in range(2, len(arr) + 1):
        res += combinations(arr, k)
    return res


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

    def deref(self, i: Var) -> Term:
        t: Term = i
        while isinstance(t, Var):
            v = self.get(t)
            if v is None:
                break
            t = v
        return t

    def __bool__(self) -> bool:
        pred = len(self.ctx) > 0
        return pred

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
    if isinstance(t1, Var) and isinstance(t2, Var):
        # print("[TRACE][VAR]", t1, t2)
        env = env.clone()
        env.put(t1, t2)
        env.put(t2, t1)
        return True, env

    if isinstance(t1, Var):
        # print("[TRACE][VAR]", t1, t2)
        env = env.clone()
        env.put(t1, t2)
        return True, env

    if isinstance(t2, Var):
        # print("[TRACE][VAR]", t1, t2)
        env = env.clone()
        env.put(t2, t1)
        return True, env

    if isinstance(t1, Atom) and isinstance(t2, Atom):
        # print("[TRACE][ATOM]", t1, t2)
        return t1 == t2, env

    if isinstance(t1, Nil) and isinstance(t2, Nil):
        # print("[TRACE][NIL]", t1, t2)
        return t1 == t2, env

    if isinstance(t1, Cons) and isinstance(t2, Cons):
        # print("[TRACE][CONS]", t1, t2)
        ok1, e1 = solve(t1.fst, t2.fst, env)
        if ok1:
            ok2, e2 = solve(t1.snd, t2.snd, e1)
            return ok2, e2
        return ok1, e1
    return False, env


def apply(t: Term, env: Environment) -> Term:
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


class DB:
    def __init__(self, rules: list[Cons]) -> None:
        self.rules = rules
        self.compose()

    def compose(self):
        nil = Nil()
        nil_rules = [rule for rule in self.rules if isinstance(rule.snd, Nil)]
        composed = []

        for combo in all_combinations(nil_rules):
            combo_cons = nil
            for rule in reversed(combo):
                combo_cons = Cons(rule.fst, combo_cons)
            new_rule = Cons(combo_cons, nil)
            composed.append(new_rule)
        # 合并原规则 + 新生成的组合规则
        self.rules = self.rules + composed

    def prove(self, goal: Term, e: Environment):
        # print("[TRACE][PROVE]", goal, e)
        checkpoints = []
        new_e = e.clone()
        for rule in self.rules:
            ok, new_e = solve(goal, rule.fst, new_e)
            if ok:
                sub_goal = apply(rule.snd, new_e)
                checkpoints.append((ok, new_e, sub_goal))
                # print("[TRACE][SUBGOAL]", sub_goal)
                cps = self.prove(sub_goal, new_e)
                checkpoints.extend(cps)
        return checkpoints
