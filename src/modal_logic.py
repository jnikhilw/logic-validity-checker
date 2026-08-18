from dataclasses import dataclass, field
from typing import Dict, Set, List, Tuple, Optional



    # --- AST NODES ---
    
@dataclass(frozen=True)
class F:
    pass

# Variable  
@dataclass(frozen=True)
class Var(F):
    name: str


# Negation operator 
@dataclass(frozen=True)
class Not(F):
    a: F

    
# Conjunction operator 
@dataclass(frozen=True)
class And(F):
    a: F
    b: F

    
# Disjunction operator 
@dataclass(frozen=True)
class Or(F):
    a: F
    b: F

# Conditional operator 
@dataclass(frozen=True)
class Imp(F):
    a: F
    b: F

# Biconditional operator 
@dataclass(frozen=True)
class Iff(F):
    a: F
    b: F
    
# Necessity operator 
@dataclass(frozen=True)
class Box(F):   # []
    a: F

# Possibility operator 
@dataclass(frozen=True)
class Dia(F):   # <>
    a: F


    # --- PARSER (tokens -> AST) ---

# precedence: bigger = binds tighter
PREC = {
    "<->": 1,
    "->":  2,
    "|":   3,
    "&":   4,
}

RIGHT_ASSOC = {"->", "<->"} 

UNARY = {"~", "[]", "<>"}

# Time: O(n), where n is the number of tokens 
# Space: O(n) 
# list[str] -> F
def parse(tokens: List[str]):
    i = 0  # cursor into tokens

    def peek() -> Optional[str]:
        return tokens[i] if i < len(tokens) else None
    
    def eat(expected: Optional[str] = None) -> str:
        nonlocal i
        tok = peek()
        if tok is None:
            raise ValueError("Unexpected end of input")
        if expected is not None and tok != expected:
            raise ValueError(f"Expected {expected!r}, got {tok!r}")
        i += 1
        return tok

    def parse_prefix() -> F:
        tok = peek()
        if tok is None:
            raise ValueError("Unexpected end of input")

        # unary operators
        if tok in UNARY:
            eat()
            sub = parse_prefix()
            if tok == "~":
                return Not(sub)
            if tok == "[]":
                return Box(sub)
            if tok == "<>":
                return Dia(sub)
            raise ValueError(f"Unknown unary operator: {tok}")

        # parenthesized
        if tok == "(":
            eat("(")
            inside = parse_expr(0)
            eat(")")
            return inside

        # variable
        if tok.isupper():
            eat()
            return Var(tok)

        raise ValueError(f"Unexpected token in prefix position: {tok!r}")

    def parse_expr(min_prec: int) -> F:
        left = parse_prefix()

        while True:
            op = peek()
            if op not in PREC:
                break

            prec = PREC[op]
            if prec < min_prec:
                break

            eat(op)

            # right-assoc means we recurse with same prec
            # left-assoc means we recurse with prec+1
            next_min = prec if op in RIGHT_ASSOC else prec + 1
            right = parse_expr(next_min)

            if op == "&":
                left = And(left, right)
            elif op == "|":
                left = Or(left, right)
            elif op == "->":
                left = Imp(left, right)
            elif op == "<->":
                left = Iff(left, right)
            else:
                raise ValueError(f"Unknown binary operator: {op}")

        return left

    ast = parse_expr(0)

    if i != len(tokens):
        raise ValueError(f"Unconsumed tokens at end: {tokens[i:]}")

    return ast


        # --- Helpers ---

# F -> F
# Returns ¬f or ¬(¬A) = A.
def negate(f: F) -> F:
    """Return ¬f, or ¬(¬A) = A."""
    if isinstance(f, Not):
        return f.a
    return Not(f)

# F -> bool
# Returns True if f is a variable or the negation of a variable
def is_literal(f: F):
    return isinstance(f, Var) or (isinstance(f, Not) and isinstance(f.a, Var))

# (Set[F], F) -> bool
# True iff f is a literal and its negation is already present in existing.
def is_literal_contradiction(existing: Set[F], f: F) -> bool:
    if not is_literal(f):
        return False
    return negate(f) in existing


        # --- TableauBranch ---
        
World = int

@dataclass
class Branch:
    # formulas true at each world
    labels: Dict[World, Set[F]] = field(default_factory=dict)
    
     # accessibility relation: R[w] = set of successors v with wRv
    R: Dict[World, Set[World]] = field(default_factory=dict)
    
    # explicit contradictions found per-world
    closed: bool = False
    closed_reason: str = ""
    
    # worklist of pending expansions: (world, formula)
    todo: List[Tuple[World, F]] = field(default_factory=list)
    next_world_id: int = 0

    def new_world(self) -> World:
        w = self.next_world_id
        self.next_world_id += 1
        self.labels.setdefault(w, set())
        self.R.setdefault(w, set())
        return w

    def has_formula(self, w: World, f: F) -> bool:
        return f in self.labels.get(w, set())

    def add_formula(self, w: World, f: F) -> bool:
        """
        Add f at world w if new.
        If adding creates a literal contradiction (P and ¬P), close branch.
        Returns True iff we actually added something.
        """
        if self.closed:
            return False

        world_set = self.labels.setdefault(w, set())

        # method-style closure check
        if is_literal_contradiction(world_set, f):
            self.closed = True
            # nicer reason
            lit = f if isinstance(f, Var) else f.a  # Var inside literal
            name = lit.name if isinstance(lit, Var) else "?"
            self.closed_reason = f"World {w}: {name} and ~{name}"
            return False

        if f in world_set:
            return False

        world_set.add(f)
        self.todo.append((w, f))
        return True
    
            # --- Helpers ---
            
def ensure_world(b: Branch, w: World) -> None:
    b.labels.setdefault(w, set())
    b.R.setdefault(w, set())
    
def successors(b: Branch, w: World) -> Set[World]:
    ensure_world(b, w)
    return b.R[w]
    
def add_R(b: Branch, w: World, v: World) -> None:
    ensure_world(b, w)
    ensure_world(b, v)
    b.R[w].add(v)
    
def clone_branch(b: Branch) -> Branch:
    nb = Branch()
    nb.labels = {w: set(fs) for w, fs in b.labels.items()}
    nb.R = {w: set(vs) for w, vs in b.R.items()}
    nb.closed = b.closed
    nb.closed_reason = b.closed_reason
    nb.todo = list(b.todo)
    nb.next_world_id = b.next_world_id
    return nb


        
def modal_validity(premises, conclusion, premise_tokens, conclusion_tokens):
    premise_asts = [parse(toks) for toks in premise_tokens]
    conclusion_ast = parse(conclusion_tokens)
    print("Premise ASTs:", premise_asts)
    print("Conclusion AST:", conclusion_ast)