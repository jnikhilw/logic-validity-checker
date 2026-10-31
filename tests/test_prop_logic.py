from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from logic_core import normalize, tokenize
from prop_logic import prop_check

def run_prop_check(premises, conclusion):
    """
    Helper function that normalizes and tokenizes an argument
    before passing it to prop_check().
    """
    premise_tokens = [
        tokenize(normalize(p))
        for p in premises
    ]

    conclusion_tokens = tokenize(normalize(conclusion))

    return prop_check(
        premises,
        conclusion,
        premise_tokens,
        conclusion_tokens
    )


def test_modus_ponens_valid():
    """
    P -> Q
    P
    ∴ Q

    Expected: Valid
    """
    result = run_prop_check(
        ["P -> Q", "P"],
        "Q"
    )

    assert result["premises_satisfiable"] is True
    assert result["counterexample_found"] is False


def test_affirming_consequent_invalid():
    """
    P -> Q
    Q
    ∴ P

    Expected: Invalid
    """
    result = run_prop_check(
        ["P -> Q", "Q"],
        "P"
    )

    assert result["premises_satisfiable"] is True
    assert result["counterexample_found"] is True

    # Counterexample should make all premises true
    # while making P false.
    assert result["counterexample"]["P"] is False
    assert result["counterexample"]["Q"] is True
    assert all(result["counterexample_premise_values"])
    assert result["counterexample_conclusion_value"] is False


def test_contradictory_premises_vacuously_valid():
    """
    P
    ~P
    ∴ Q

    Expected: Valid because the premises are jointly unsatisfiable.
    """
    result = run_prop_check(
        ["P", "~P"],
        "Q"
    )

    assert result["premises_satisfiable"] is False
    assert result["counterexample_found"] is False


def test_tautology_classification():
    """
    P | ~P

    Expected conclusion classification: TAUTOLOGY
    """
    result = run_prop_check(
        [],
        "P | ~P"
    )

    assert result["conclusion_kind"] == "TAUTOLOGY"


def test_contradiction_classification():
    """
    P & ~P

    Expected conclusion classification: CONTRADICTION
    """
    result = run_prop_check(
        [],
        "P & ~P"
    )

    assert result["conclusion_kind"] == "CONTRADICTION"


def test_contingent_classification():
    """
    P -> Q

    Expected conclusion classification: CONTINGENT
    """
    result = run_prop_check(
        [],
        "P -> Q"
    )

    assert result["conclusion_kind"] == "CONTINGENT"


def test_variable_extraction_is_sorted():
    result = run_prop_check(
        ["Q -> P", "R"],
        "P"
    )

    assert result["variables"] == ["P", "Q", "R"]


def test_truth_table_size():
    """
    Three variables should generate 2^3 = 8 valuations.
    """
    result = run_prop_check(
        ["P & Q"],
        "R"
    )

    assert len(result["valuations"]) == 8


def test_truth_table_not_stored_by_default():
    result = run_prop_check(
        ["P"],
        "P"
    )

    assert result["truth_table"] is None


def test_truth_table_stored_when_requested():
    premises = ["P -> Q", "P"]
    conclusion = "Q"

    premise_tokens = [
        tokenize(normalize(p))
        for p in premises
    ]
    conclusion_tokens = tokenize(normalize(conclusion))

    result = prop_check(
        premises,
        conclusion,
        premise_tokens,
        conclusion_tokens,
        include_truth_table=True
    )

    # P and Q give 2^2 = 4 rows.
    assert len(result["truth_table"]) == 4