# Susu Group Tracker

A lightweight Python application designed to manage a rotating savings group (susu). It tracks weekly contributions, enforces exact currency handling without rounding errors, manages partial payments, prevents week closure on outstanding debts, and rotates pot payouts sequentially based on member join order.

## Features
* **Exact Financial Precision**: Built using Python's `decimal.Decimal` to prevent floating-point rounding errors.
* **Interactive CLI**: Simple command-line menu for real-time tracking and management.
* **Validation & Security**: Strict rules blocking duplicate IDs, unknown members, negative inputs, overpayments, and late membership joins.
* **Automated Unit Tests**: Built-in test suite covering 6 critical functional workflows.

## Prerequisites
* Python 3.8+

## How to Run the Program
Start the interactive command-line interface:
```bash
python3 main.py
