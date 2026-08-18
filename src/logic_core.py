
# Notation normalization: map commonly used logical symbols
# into our canonical operators: ~  &  |  ->  <->
# Note: "^" is treated as AND (not XOR). Lowercase "v" is treated as OR.
ALIASES = {
    "¬": "~",
    "!": "~",
    "∧": "&",
    "·": "&",
    "^": "&",
    "∨": "|",
    "v": "|",
    "→": "->",
    "=>": "->",
    "↔": "<->",
    "<=>": "<->",

    # modal aliases
    "□": "[]",
    "◇": "<>",
}


# Time: O(a * n), where n is formula length and a is the number of aliases (a=15).
# Space: O(n) to store intermediate and final normalized strings.
# str -> str
# Accepts a string with various logical symbols and normalizes it
# into canonical operators (~, &, |, ->, <->).
def normalize(formula: str) -> str:
    formula = formula.replace("<=>", "<->").replace("=>", "->")
    for k, v in ALIASES.items():
        formula = formula.replace(k, v)
    return formula


# Time: O(n), where n is the length of the formula string.
# Space: O(n) to store the resulting tokens.
# str -> list[str]
# Accepts a formula string and returns a list of tokens (variables, operators, parentheses).
def tokenize(formula: str) -> list[str]:
    tokens = [] # stores identified tokens 
    i = 0 # current character index 

   # Linear scan: iterate through formula string character by character
    while i < len(formula):
        ch = formula[i]

        # 1: skip whitespace
        if ch.isspace():
            i += 1
            continue

        # 2: multi-character operators first
        
        # modal unary operators
        # necessity operator 
        if formula.startswith("[]", i):
            tokens.append("[]")
            i += 2
            continue    
        # possibility operator 
        if formula.startswith("<>", i):
            tokens.append("<>")
            i += 2
            continue
        
        # propositional multi-ch binary operators
        # biconditional operator 
        if formula.startswith("<->", i):
            tokens.append("<->")
            i += 3
            continue
        # conditional operator 
        if formula.startswith("->", i):
            tokens.append("->")
            i += 2
            continue


        # 3: grouping (parentheses)
        if ch in ("(", ")"):
            tokens.append(ch)
            i += 1
            continue

        # 4: single-char operators
        # negation (~), conjunction (&), disjunction (|)
        if ch in ("~", "&", "|"):
            tokens.append(ch)
            i += 1
            continue

        # 5: variables (uppercase letters)
        if ch.isupper():
            tokens.append(ch)
            i += 1
            continue

        # 5.5: disambiguate lowercase 'v' as the disjunction operator ('|')
        if ch == "v":
            
            if formula.strip() == "v":
                raise ValueError("Bare 'v' is not a formula")
            
            prev = formula[i-1] if i > 0 else " "
            nxt  = formula[i+1] if i + 1 < len(formula) else " "
            
            
            # Contextual check: ensures 'v' is situated between valid logical components
            left_ok  = prev.isspace() or prev in "()" or prev.isupper()
            right_ok = nxt.isspace() or nxt in "()[]" or nxt.isupper() or nxt in {"~", "<"}
        
            if left_ok and right_ok:
                tokens.append("|")
                i += 1
                continue
            
            
        raise ValueError(f"Unexpected character '{ch}' in: {formula}")
      

    return tokens


# Time: O(n), where n is the total number of tokens across premises and conclusion.
# Space: O(1), as the membership test utilizes a constant-sized lookup set.
# list[str] -> bool
# Scans the token stream for modal operators ([] or <>) to determine 
# the appropriate logic engine (Classical vs. Modal) for further evaluation.
def has_modal_ops(all_tokens: list[str]):
    return any(tok in {"[]", "<>"} for tok in all_tokens)


# Time: O(n * 2^n), where n is the number of propositional variables. 
# Space: O(n * 2^n) to store the complete set of valuations.
# list[str] -> list[dict[str, bool]]
# Accepts a list of variables and returns a list of valuations (dicts mapping var -> bool).
def truthtable(variables: list[str]) -> list[dict[str, bool]]:
    n = len(variables)
    rows = []
    for i in range(2**n):
        bits = bin(i)[2:].zfill(n)
        valuation = {}
        for var, bit in zip(variables, bits):
            valuation[var] = (bit == "1")
        rows.append(valuation)
    return rows


# Defines the binding strength for classical and modal operators.
# Higher values indicate tighter binding.
PRECEDENCE = {
    "[]": 5,
    "<>": 5,
    "~": 4,
    "&": 3,
    "|": 2,
    "->": 1,
    "<->": 0,
}

RIGHT_ASSOC = {"~", "[]", "<>", "->"}
OPERATORS = set(PRECEDENCE.keys())


# Time: O(n), where n is the number of tokens.
# Space: O(n) for the operator stack and output list.
# list[str] -> list[str]
# Shunting-Yard algorithm to convert infix tokens to 
# Reverse Polish Notation (RPN/Postfix) for truth-functional evaluation.
def to_rpn(tokens: list[str]) -> list[str]:
    output = [] # RPN output 
    opstack = [] # operator stack

    for tok in tokens:
        # 1: variable
        if tok.isupper():
            output.append(tok)
            continue

        # 2: operator
        if tok in OPERATORS:
            while opstack and opstack[-1] in OPERATORS:
                top = opstack[-1]

                if tok in RIGHT_ASSOC:
                    # 3: right-assoc pop rule
                    if PRECEDENCE[top] > PRECEDENCE[tok]:
                        output.append(opstack.pop())
                    else:
                        break
                else:
                    # 4: left-assoc pop rule
                    if PRECEDENCE[top] >= PRECEDENCE[tok]:
                        output.append(opstack.pop())
                    else:
                        break

            # 5: push current operator
            opstack.append(tok)
            continue

        # 6: left paren
        if tok == "(":
            opstack.append(tok)
            continue

        # 7: right paren
        if tok == ")":
            while opstack and opstack[-1] != "(":
                output.append(opstack.pop())
            if not opstack:
                raise ValueError("Mismatched parentheses")
            opstack.pop()
            continue

        raise ValueError(f"Unknown token: {tok}")

    # 8: drain remaining operators from stack to output
    while opstack:
        top = opstack.pop()
        if top in ("(", ")"):
            raise ValueError("Mismatched parentheses")
        output.append(top)

    return output


# Time: O(m), where m is the number of tokens in the postfix expression.
# Space: O(m) for the evaluation stack.
# (list[str], dict[str, bool]) -> bool
# Evaluates a postfix (RPN) expression under a single valuation.
# This evaluation step is invoked iteratively to populate truth table rows.
def eval_rpn(rpn: list[str], valuation: dict[str, bool]) -> bool:
    stack = []

    for tok in rpn:
        if tok.isupper():
            stack.append(valuation[tok])
            continue

        if tok == "~":
            a = stack.pop()
            stack.append(not a)
            continue

        # binary ops: pop right operand first, then left operand
        b = stack.pop()
        a = stack.pop()

        if tok == "&":
            stack.append(a and b)
        elif tok == "|":
            stack.append(a or b)
        elif tok == "->":
            stack.append((not a) or b)   # implication
        elif tok == "<->":
            stack.append(a == b)         # biconditional
        else:
            raise ValueError(f"Unknown operator in RPN: {tok}")

    if len(stack) != 1:
        raise ValueError(f"Bad RPN expression, leftover stack: {stack}")

    return stack[0]
