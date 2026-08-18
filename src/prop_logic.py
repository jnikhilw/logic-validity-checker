from logic_core import to_rpn, eval_rpn, truthtable
from utils import print_truth_table

def prop_check(premises, conclusion, premise_tokens, conclusion_tokens, include_truth_table=False):
    
    # --- Data analysis ---
    
    # list[list[str]] (infix) -> list[list[str]] (postfix)
    # Converts each tokenized premise into Reverse Polish Notation.
    premise_rpns = [to_rpn(toks) for toks in premise_tokens]
    conclusion_rpn = to_rpn(conclusion_tokens)
      
    variables = set()
    # Extracts the set of unique atomic variables from all premises and the conclusion.
    # Time: O(N), where N is the total number of tokens 
    for toks in premise_tokens:
        for tok in toks:
            if tok.isupper():
                variables.add(tok)
    for tok in conclusion_tokens:
        if tok.isupper():
            variables.add(tok)
            
    # list[str] -> sorted list[str]
    # Alphabetizes atomic variables for deterministic column ordering.    
    variables = sorted(variables)
    # valuations = list[str] -> list[dict[str, bool]]
    valuations = truthtable(variables)

    # State tracking for semantic analysis (Satisfiability and Validity) 
    premises_satisfiable = False
    counterexample_found = False
    counterexample = None
    counterexample_premise_values = None
    counterexample_conclusion_value = None   
    # Accumulators for Conclusion classification (Tautology/Contingency/Contradiction) 
    conclusion_true_somewhere = False
    conclusion_false_somewhere = False
    
    truth_table_rows = [] if include_truth_table else None 
       
    # Time: O(L * 2^n)
    # Perform a truth table analysis to check for argument validity 
    # and classify the conclusion (tautology, contingency, or contradiction).   
    for valuation in valuations:
        premise_values = [eval_rpn(rpn, valuation) for rpn in premise_rpns]
        premises_all_true = all(premise_values)

        conclusion_value = eval_rpn(conclusion_rpn, valuation)

        if conclusion_value:
            conclusion_true_somewhere = True
        else:
            conclusion_false_somewhere = True

        if premises_all_true:
            # The premises are satisfiable or consistent if there exists at least one valuation 
            # (truth table row) where all premises jointly evaluate to True.            
            premises_satisfiable = True
            
            # A valuation is a counterexample iff the premises are jointly true 
            # but the conclusion is false. 
            if (not conclusion_value) and (not counterexample_found):
                counterexample_found = True
                counterexample = dict(valuation)
                counterexample_premise_values = premise_values
                counterexample_conclusion_value = conclusion_value
                
        if include_truth_table:
            truth_table_rows.append({
                "valuation": dict(valuation),
                "premises": premise_values,
                "conclusion": conclusion_value,
            })   

    # A conclusion is contingent if there exists a valuation where it is false 
    # and another where it is true. 
    if conclusion_true_somewhere and conclusion_false_somewhere:
        conclusion_kind = "CONTINGENT"
                        
    # A conclusion is a tautology if it is true under ALL valuations.     
    elif conclusion_true_somewhere:
        conclusion_kind = "TAUTOLOGY"
    # A conclusion is a contradiction if it is false under ALL valuations.
    else:
        conclusion_kind = "CONTRADICTION"
               
                    
    # --- Returns logical properties  ---
    
    return {
        "premise_rpns": premise_rpns,
        "conclusion_rpn": conclusion_rpn,
        "variables": variables,
        "valuations": valuations,
    
        "premises_satisfiable": premises_satisfiable,
        "conclusion_kind": conclusion_kind,
    
        "counterexample_found": counterexample_found,
        "counterexample": counterexample,
        "counterexample_premise_values": counterexample_premise_values,
        "counterexample_conclusion_value": counterexample_conclusion_value,
    
        "truth_table": truth_table_rows,
        }
    

def prop_validity(premises, conclusion, premise_tokens, conclusion_tokens):
    show = input("Show full truth table? (y/n): ").strip().lower()
    include_tt = show in ("y", "yes")

    result = prop_check(
        premises, conclusion,
        premise_tokens, conclusion_tokens,
        include_truth_table=include_tt
    )

    # If you want your nice existing table printer:
    if include_tt:
        # You can keep using your existing printer exactly like before
        # (it already knows how to display)
        # If it needs valuations, you can regenerate them from variables OR
        # modify print_truth_table to accept truth_table rows later.
        valuations = truthtable(result["variables"])
        print_truth_table(
            result["variables"],
            premises, result["premise_rpns"],
            conclusion, result["conclusion_rpn"],
            valuations
        )

    # Prints / UX
    if result["premises_satisfiable"]:
        print("Premises are satisfiable.")
    else:
        print("Premises are CONTRADICTORY (unsatisfiable).")

    print(f"Conclusion classification: {result['conclusion_kind']}")

    if result["counterexample_found"]:
        print("INVALID (counterexample found)")
        print("Valuation:", result["counterexample"])
        print("Premises at that valuation:")
        for p, val in zip(premises, result["counterexample_premise_values"]):
            print(f"  {p:<20} = {val}")
        print(f"Conclusion at that valuation:\n  {conclusion:<20} = {result['counterexample_conclusion_value']}")
    else:
        if not result["premises_satisfiable"]:
            print("Argument is VACUOUSLY VALID (no valuation makes all premises true).")
        else:
            print("Your argument is NON-VACUOUSLY valid")