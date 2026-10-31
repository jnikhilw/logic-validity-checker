from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from logic_core import normalize, tokenize
from modal_logic import modal_validity


def run_modal_check(premises, conclusion):
    """
    Helper function that normalizes and tokenizes an argument
    before passing it to modal_validity().
    """
    premise_tokens = [
        tokenize(normalize(p))
        for p in premises
    ]

    conclusion_tokens = tokenize(normalize(conclusion))

    modal_validity(
        premises,
        conclusion,
        premise_tokens,
        conclusion_tokens
    )


def test_modal_distribution_valid(capsys):
    """
    □(P → Q), □P ⊨ □Q

    Expected: Valid in K
    """
    run_modal_check(
        ["[](P -> Q)", "[]P"],
        "[]Q"
    )

    output = capsys.readouterr().out

    assert "VALID in K" in output


def test_necessity_does_not_imply_actuality(capsys):
    """
    □P ⊨ P

    Expected: Invalid in K
    """
    run_modal_check(
        ["[]P"],
        "P"
    )

    output = capsys.readouterr().out

    assert "INVALID in K" in output
    assert "Countermodel:" in output


def test_necessity_does_not_imply_iterated_necessity(capsys):
    """
    □P ⊨ □□P

    Expected: Invalid in K
    """
    run_modal_check(
        ["[]P"],
        "[][]P"
    )

    output = capsys.readouterr().out

    assert "INVALID in K" in output
    assert "Countermodel:" in output


def test_possible_conjunction_implies_possible_conjunct(capsys):
    """
    ◇(P ∧ Q) ⊨ ◇P

    Expected: Valid in K
    """
    run_modal_check(
        ["<>(P & Q)"],
        "<>P"
    )

    output = capsys.readouterr().out

    assert "VALID in K" in output