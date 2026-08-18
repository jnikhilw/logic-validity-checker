from logic_core import eval_rpn


def tf(x: bool) -> str:
    return "1" if x else "0"


def print_truth_table(variables, premises, premise_rpns, conclusion, conclusion_rpn, valuations):
    # Column headers
    headers = list(variables) + [f"P{i+1}" for i in range(len(premises))] + ["C"]

    # Column widths (simple + readable)
    col_w = max(3, max(len(h) for h in headers))  # at least 3 chars wide

    # Print header row
    print("\nTRUTH TABLE")
    print(" | ".join(f"{h:^{col_w}}" for h in headers))

    # Print separator line
    print("-" * ((col_w + 3) * len(headers) - 3))

    # Print each row
    for valuation in valuations:
        var_cells = [tf(valuation[v]) for v in variables]

        premise_cells = [tf(eval_rpn(rpn, valuation)) for rpn in premise_rpns]
        conclusion_cell = tf(eval_rpn(conclusion_rpn, valuation))

        row = var_cells + premise_cells + [conclusion_cell]
        print(" | ".join(f"{cell:^{col_w}}" for cell in row))

    # Legend
    print("\nLegend: 1 = True, 0 = False")
    print("P1..Pn are the premises in the order you entered them; C is the conclusion.")