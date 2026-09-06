# Logical Validity Analyzer

## Project Abstract

This project implements a logical evaluation pipeline for classical propositional logic and normal modal logic K. The user inputs the premises and then the conclusion of an argument in symbolic notation. Based on the operators detected, the task is routed to either the classical logic engine, which uses exhaustive truth-table enumeration to determine the argument's logical properties, or the modal logic engine, which uses abstract syntax trees to represent formula structure and tableau search to construct and track the Kripke model. The propositional logic engine determines whether the argument is valid or invalid; if it is invalid, it prints a countermodel to the user; it also determines whether the premises are jointly contradictory and whether the conclusion is contingent or logically necessary. The modal logic engine dynamically searches the tableau tree containing the premises and the negated conclusion, closing branches under contradiction; if it finds an open branch, the argument is invalid, and it prints a Kripke countermodel.

This project implements a logical evaluation pipeline...

## Key Features

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