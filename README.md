# Logical Validity Analyzer

## Project Abstract

This project implements a logical evaluation pipeline for classical propositional logic and normal modal logic K. The user inputs the premises and then the conclusion of an argument in symbolic notation. Based on the operators detected, the task is routed to either the classical logic engine, which uses exhaustive truth-table enumeration to determine the argument's logical properties, or the modal logic engine, which uses abstract syntax trees to represent formula structure and tableau search to construct and track the Kripke model. The propositional logic engine determines whether the argument is valid or invalid; if it is invalid, it prints a countermodel to the user; it also determines whether the premises are jointly contradictory and whether the conclusion is contingent or logically necessary. The modal logic engine dynamically searches the tableau tree containing the premises and the negated conclusion, closing branches under contradiction; if it finds an open branch, the argument is invalid, and it prints a Kripke countermodel.

## Key Features

Key features

- **Classical propositional logic argument evaluation: Determines whether the argument is valid, that is, whether the premises logically necessitate the conclusion. 

- **Truth table enumeration: Prints full truth tables with all possible truth assignments and valuations. 

- **Propositional Countermodel Generation: If an argument is invalid, it prints a valuation in which all the premises are true, but the conclusion is false. 

- **Logical Property Classification: Determines whether the premises are jointly satisfiable and whether the conclusion is logically necessary, contingent, or contradictory. 

- **Normal Modal Logic K Evaluation: Determines whether an argument is valid according to the Kripke semantics of normal modal logic K if a modal argument is detected. 

- **Abstract Syntax Tree Parsing: Converts tokenized formulas into recursively structured abstract syntax trees, representing all propositional connectives and modal operators, for modal logic evaluation. 

- **Tableau-Based Satisfiability Search: Evaluates modal arguments by constructing a tableau from the premises and negated conclusion and performing depth-first search over alternative tableau branches, closing branches when contradictions are detected.

- **Dynamic Kripke Model Construction: Constructs possible worlds, accessibility relations, and world-specific formula constraints during tableau expansion rather than enumerating complete modal models in advance.

- **Modal Countermodel Generation: When an open tableau branch is found, extracts and displays the resulting Kripke countermodel demonstrating how the premises can be satisfied while the conclusion is false.

- **Symbolic Formula Normalization and Tokenization: Accepts multiple symbolic representations of logical operators and converts them into a standardized token sequence for parsing and evaluation.


## Theoretical Background

## System Architecture

## Repository Structure

## Installation

## Usage

## Propositional Logic Engine

## Modal Logic Engine

## Testing

## Limitations and Future Work

## References