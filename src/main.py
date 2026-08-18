from logic_core import normalize, tokenize, has_modal_ops
from nl_translate import maybe_translate
from prop_logic import prop_validity
from modal_logic import modal_validity



def validity():
    # str -> list[str] 
    premises = [p.strip() for p in input("Enter premises: ").split(",")]
    # str
    conclusion = input("Enter conclusion: ").strip()
    
    # --- Data Preparation ---
        
    # NL -> Symbolic: Translates natural language to logic symbols if necessary.
    premises, conclusion = maybe_translate(premises, conclusion)
    
    # list[str] -> normalized list[str] -> tokenized list[list[str]]
    # premise_tokens: list[list[str]]
    premise_tokens = [tokenize(normalize(p)) for p in premises]
    
    # str -> normalized str -> tokenized list[str] 
    # conclusion_tokens: [str]
    conclusion_tokens = tokenize(normalize(conclusion))

    # list[list[str]] + list[str] -> list[str]
    all_tokens = [tok for toks in premise_tokens for tok in toks] + conclusion_tokens
    
    # --- Engine Selection & Execution ---
    
        # --- Modal Logic Engine ---
     
    # Routes to modal logic engine if modal operators are present in the tokens.
    if has_modal_ops(all_tokens):
        print("(Modal operators detected: routing to modal tableau engine.)")
        modal_validity(premises, conclusion, premise_tokens, conclusion_tokens, include_truth_table=False)
        return
       
        # --- Prop Logic Engine ---
            
    # (list[str], str, list[list[str]], list[str]) -> None
    # Evaluates and prints truth table and logical properties.
    prop_validity(premises, conclusion, premise_tokens, conclusion_tokens)

if __name__ == "__main__":
    # Start the interactive CLI
    validity()
