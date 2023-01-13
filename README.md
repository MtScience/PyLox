# PyLox

## Overview

This is my Python 3.10 reimplementation of jlox as described in the awesome book [“Crafting Interpreters”](https://craftinginterpreters.com/) by Robert Nystrom. Made it to better understand the principles behind language implementation, since I'm not particularly comfortable with Java, which Robert used.

## Running

The program is run with the command (on openSUSE Linux)

    python3.10 pylox.py <script>

to run a Lox script or with

    python3.10 pylox.py

to run the interactive interpreter. The program requires no external dependencies.

## Differences from Robert's jlox

PyLox is mostly a direct translation of Java code in the book to Python (made idiomatic where possible), so it doesn't have any major differences when it comes to behaviour. However, there are some differences:

- Added support for a `^` operator, denoting exponentiation—I thought it was too minimalistic for a modern scripting language, albeit not intended for real-world use, to not have exponentiation built-in;
- Modified the REPL so that now it automatically prints the result of expression statements (trying to complete the challenge after chapter 8; drew inspiration from [ronsh909](https://github.com/ronsh909)'s version);
- Implementation detail: replaced the recursive method lookup with copy-down inheritance (clox-inspired) for performance—it reduces the number of condition checks and recursive method calls.

## Current state of the project

PyLox is considered complete (chapter 13 of the book completed). Currently it's code is being simplified and optimized. Also, there is a plan to add a number of native functions and (possibly) modify the REPL to make it more comfortable to use.

All variables, class attributes and functions are type-hinted, except where doing so vould lead to a circular import.
