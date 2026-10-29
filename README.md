# Logical Validity Analyzer

## Project Abstract

This project implements a logical evaluation pipeline for classical propositional logic and normal modal logic K. The user inputs the premises and then the conclusion of an argument in symbolic notation. Based on the operators detected, the task is routed to either the classical logic engine, which uses exhaustive truth-table enumeration to determine the argument's logical properties, or the modal logic engine, which uses abstract syntax trees to represent formula structure and tableau search to construct and track the Kripke model. The propositional logic engine determines whether the argument is valid or invalid; if it is invalid, it prints a countermodel to the user; it also determines whether the premises are jointly contradictory and whether the conclusion is contingent or logically necessary. The modal logic engine dynamically searches the tableau tree containing the premises and the negated conclusion, closing branches under contradiction; if it finds an open branch, the argument is invalid, and it prints a Kripke countermodel.

## Key Features

Key features

- Classical propositional logic argument evaluation: Determines whether the argument is valid, that is, whether the premises logically necessitate the conclusion. 

- Truth table enumeration: Prints full truth tables with all possible truth assignments and valuations. 

- Propositional Countermodel Generation: If an argument is invalid, it prints a valuation in which all the premises are true, but the conclusion is false. 

- Logical Property Classification: Determines whether the premises are jointly satisfiable and whether the conclusion is logically necessary, contingent, or contradictory. 

- Normal Modal Logic K Evaluation: Determines whether an argument is valid according to the Kripke semantics of normal modal logic K if a modal argument is detected. 

- Abstract Syntax Tree Parsing: Converts tokenized formulas into recursively structured abstract syntax trees, representing all propositional connectives and modal operators, for modal logic evaluation. 

- Tableau-Based Satisfiability Search: Evaluates modal arguments by constructing a tableau from the premises and negated conclusion and performing depth-first search over alternative tableau branches, closing branches when contradictions are detected.

- Dynamic Kripke Model Construction: Constructs possible worlds, accessibility relations, and world-specific formula constraints during tableau expansion rather than enumerating complete modal models in advance.

- Modal Countermodel Generation: When an open tableau branch is found, extracts and displays the resulting Kripke countermodel demonstrating how the premises can be satisfied while the conclusion is false.

- Symbolic Formula Normalization and Tokenization: Accepts multiple symbolic representations of logical operators and converts them into a standardized token sequence for parsing and evaluation.


## Theoretical Background

## System Architecture

The user is first prompted to input the premises for an argument, separated by commas, and is then prompted to input the conclusion of the argument. The premises and conclusion are then normalized, converting common propositional or modal symbols into a standardized set of logical connective symbols. The normalized premises and conclusion are then tokenized into lists whose elements are atomic propositions, logical connectives, or modal operators.

If modal operators are detected, the premises and conclusion are then routed to the modal logic engine; otherwise, they are routed to the propositional logic engine. If the premises and conclusion are routed to the propositional logic engine, the user is prompted to choose whether to print a full truth table. The token list for each is then converted from infix notation to postfix notation. The atomic variables are placed into a sorted set, and a valuation list is constructed whose elements are dictionaries representing truth-value assignments to the atomic variables. State-tracking variables are then declared for later semantic analysis. For each valuation, the RPN lists of the premises and conclusion are evaluated, and the state-tracking variables are updated. Then, from the state-tracking variables, the argument's logical properties are determined: if the conclusion is true under some valuations and false under others, the conclusion is contingent; if it is true under all valuations, it is a tautology; if it is false under all valuations, it is a contradiction. If there is a valuation under which the premises jointly evaluate to true, then the premises are satisfiable. If there exists a valuation under which the premises are true and the conclusion is false, the argument is invalid; otherwise, it is valid. If the argument is invalid, the counterexample valuation is stored and printed to the user, along with the conclusion and satisfiability classifications. The full truth table is also printed if requested by the user.

If the argument is routed to the modal logic engine, the premises and conclusion are parsed, where the tokens are converted into formula objects and then hierarchically structured into abstract syntax trees. A tableau branch is then constructed with world 0. The premises and negated conclusion are then added to world 0. Each world stores the formulas asserted at that world. New worlds are then generated as needed when modal formulas are expanded. If \(P\) and \(\neg P\) are detected at the same world, the branch is closed. The tableau branches are then searched depth-first. If a branch is fully expanded and remains open, the argument is deemed invalid; otherwise, it is valid. If the argument is invalid, a countermodel is then printed to the user.


### Pipeline Overview


```text
User Input
│
├── Premises
└── Conclusion
        │
        ▼
Normalization
        │
        ▼
Tokenization
        │
        ▼
Modal Operator Detection
        │
        ├── No Modal Operators
        │       │
        │       ▼
        │   Propositional Logic Engine
        │       │
        │       ├── Prompt for Optional Truth Table
        │       │
        │       ▼
        │   Infix → Postfix (RPN) Conversion
        │       │
        │       ▼
        │   Extract Atomic Variables
        │       │
        │       ▼
        │   Generate Truth-Value Valuations
        │       │
        │       ▼
        │   Evaluate Premises and Conclusion
        │   Under Each Valuation
        │       │
        │       ▼
        │   Update Semantic State
        │       │
        │       ├── Premise Satisfiability
        │       ├── Conclusion Classification
        │       │   ├── Tautology
        │       │   ├── Contradiction
        │       │   └── Contingency
        │       │
        │       └── Argument Validity
        │               │
        │               ├── Valid
        │               │
        │               └── Invalid
        │                       │
        │                       ▼
        │                 Counterexample Valuation
        │
        └── Modal Operators Detected
                │
                ▼
            Modal Logic K Engine
                │
                ▼
            Parse Tokens
                │
                ▼
        Abstract Syntax Trees
                │
                ▼
        Construct Initial Tableau Branch
                │
                ▼
            Create World 0
                │
                ▼
    Add Premises + Negated Conclusion
                │
                ▼
        Expand Tableau Formulas
                │
                ├── Propositional Expansion
                │       │
                │       └── May Create New Tableau Branches
                │
                └── Modal Expansion
                        │
                        ├── Create New Worlds
                        └── Add Accessibility Relations
                │
                ▼
        Depth-First Tableau Search
                │
                ├── Contradiction at a World
                │       │
                │       └── Close Branch
                │
                └── Fully Expanded Open Branch
                        │
                        ▼
                    INVALID
                        │
                        ▼
                Kripke Countermodel

        If Every Tableau Branch Closes
                        │
                        ▼
                      VALID
```


## Repository Structure

```text
valcheck/
│
├── src/
│   ├── logic_core.py      # Shared normalization and tokenization utilities
│   ├── main.py            # Main application entry point and logic-engine routing
│   ├── modal_logic.py     # Modal logic K parser, tableau search, and Kripke countermodels
│   ├── prop_logic.py      # Propositional logic evaluation and truth-table reasoning
│   └── utils.py           # Shared helper utilities
│
├── tests/                 # Automated tests for propositional and modal logic
│
├── .gitignore             # Files and directories excluded from Git tracking
└── README.md              # Project documentation
```

## Installation

Clone the repository:

```bash
git clone https://github.com/jnikhilw/logic-validity-checker.git
cd logic-validity-checker
```

Run the program:

```bash
python3 src/main.py
```

## Usage

## Usage

Run the program:

```bash
python3 src/main.py
```

Enter premises separated by commas:

```text
P -> Q, P
```

Enter the conclusion:

```text
Q
```

Supported propositional operators:

```text
~    negation
&    conjunction
|    disjunction
->   implication
<->  biconditional
```

Supported modal operators:

```text
[]   necessity
<>   possibility
```

Example modal input:

```text
Premises:
[](P -> Q), []P

Conclusion:
[]Q
```

The program returns the validity result and, when applicable, a counterexample or Kripke countermodel.


## Propositional Logic Engine

### Infix-to-Postfix Conversion

The propositional logic engine converts the premises and conclusion from infix notation to postfix notation using the shunting-yard algorithm. A previously defined dictionary specifies the binding strength, or precedence, of each classical logical operator. 

The shunting-yard algorithm keeps track of two lists: the RPN output stack and the operator stack. For each token, if the token is an atomic variable, it adds it to the output stack; if it is a logical connective, 

### Variable Extraction and Valuation Generation

### RPN Evaluation

### Validity Checking

### Satisfiability and Conclusion Classification

### Countermodel Generation

## Modal Logic Engine

## Testing

## Limitations and Future Work

## References