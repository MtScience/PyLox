# PyLox

## Overview

This is my Python 3.10 reimplementation of jlox as described in the awesome book [“Crafting Interpreters”](https://craftinginterpreters.com/) by Robert Nystrom. Made it to better understand the principles behind language implementation.

## Running

The program is run with the command (on openSUSE Linux)

    python3.10 pylox.py <script>

to run a Lox script or with

    python3.10 pylox.py

to run the interactive interpreter. The program requires no external dependencies.

## Differences from Robert's jlox

PyLox is mostly a direct translation of Java code in the book to Python (made idiomatic where possible), so it doesn't have any major differences. The only thing that I added is support for `^` operator, denoting exponentiation—I thought it was too minimalistic for a modern scripting language, albeit not intended for real-world use, to not have exponentiation built-in.

## Current state of the project

Currently PyLox is a work in progress, supporting only expression evaluation (chapter 7 of the book completed).
