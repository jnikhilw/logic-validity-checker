
from logic_core import normalize, tokenize, to_rpn
import re
from typing import Dict, List, Tuple

def looks_symbolic(s: str) -> bool:
    s = s.strip()
    if not s:
        return False

    try:
        s = normalize(s)
        toks = tokenize(s)

        if not any(tok.isupper() for tok in toks):
            return False

        to_rpn(toks)
        return True

    except ValueError:
        return False
    

def translate_with_llm(premises, conclusion):
    print("\n[translator stub hit ✅]")
    print("premises raw:", premises)
    print("conclusion raw:", conclusion)    
    raise NotImplementedError("Natural-language translation not enabled yet. Use symbolic input for now.")
    

def validate_symbolic(premises: list[str], conclusion: str) -> tuple[list[str], str]:
    all_text = premises + [conclusion]

    for s in all_text:
        s2 = s.strip()
        if not s2:
            raise ValueError("Translator returned an empty premise/conclusion.")
# NOTE: we only normalize for validation here; main.py does the actual normalization later.
        s2 = normalize(s2)

        try:
            toks = tokenize(s2)

            if not any(tok.isupper() for tok in toks):
                raise ValueError(f"Translator output has no variables: {s!r}")

            to_rpn(toks)  # parse check

        except ValueError as e:
            raise ValueError(
                f"Translator returned non-symbolic / malformed logic: {s!r}\n"
                f"Underlying parser error: {e}"
            ) from e

    return premises, conclusion


def maybe_translate(premises: list[str], conclusion: str) -> tuple[list[str], str]:
    all_text = premises + [conclusion]
    if all(looks_symbolic(x) for x in all_text):
        return premises, conclusion
    premises2, conclusion2 = translate_with_llm(premises, conclusion)
    return validate_symbolic(premises2, conclusion2)