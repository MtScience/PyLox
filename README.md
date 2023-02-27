# PyLox

## Overview

This is my Python 3.10 reimplementation of jlox as described in the awesome book [“Crafting Interpreters”](https://craftinginterpreters.com/) by Robert Nystrom. Made it to better understand the principles behind language implementation, since I'm not particularly comfortable with Java, which Robert used.

## Running

The program is run with the command (on openSUSE Linux)

```console
python3.10 pylox.py <script>
```

to run a Lox script or with

```console
python3.10 pylox.py
```

to run the interactive interpreter. The program requires no external dependencies (however, `pytest` is required to run the test suite).

## Differences from Robert's jlox

PyLox is mostly a direct translation of Java code in the book to Python (made idiomatic where possible), so it doesn't have any major differences when it comes to behaviour. However, there are some differences:

- Added support for a `^` operator, denoting exponentiation—I thought it was too minimalistic for a modern scripting language, albeit not intended for real-world use, to not have exponentiation built-in;
- For the same reason added support for a `%` operator, denoting modulo division;
- Modified the REPL so that now it automatically prints the result of expression statements (trying to complete the challenge after chapter 8; drew inspiration from [ronsh909](https://github.com/ronsh909)'s version);
- Extended the “standard library” by adding some new functions. The full list:
  * `clock` – returns the current time as a float,
  * `type` – returns the type of a value as a string,
  * `getline` – asks for user input and returns it as a string,
  * `tostring` – returns the string representation of a value,
  * `tonumber` – returns the numeric value of a string or raises an error if the string does not represent a number,
  * `exp` – exponentiation,
  * `log` – natural logarithm,
  * `rad` – converts degrees to radians,
  * `sin` – sine,
  * `cos` – cosine,
  * `tan` – tangent,
  * `asin` – inverse of `sin`,
  * `acos` – inverse of `cos`,
  * `atan` – inverse of `tan`,
  * `sign` – sign function (returns 0 if the argument is 0, 1 if it is positive or -1 otherwise),
  * `ceil` – ceiling function (rounds up to the nearest integer),
  * `floor` – floor function (rounds down to the nearest integer),
  * `round` – rounding,
  * `abs` – absolute value.
- Implementation detail: replaced the recursive method lookup with copy-down inheritance (clox-inspired) for performance—it reduces the number of condition checks and recursive method calls.
- Slightly changed the output format when printing classes and instances: their names are enclosed in angle brackets (e.g. `<class MyClass>` and `<MyClass instance>`) (inspired by Python's output format).

## Test suite

The test suite is taken directly from Robert's [suite](https://github.com/munificent/craftinginterpreters/tree/master/test) with appropriate additions and modifications (which mainly consist of removal of some parts related to clox, which differs in behaviour, and tests for WIP implementation, such as parsing tests). The suite is written using `pytest`.

Additional tests for the REPL are planned.

## Current state of the project

PyLox is considered complete (chapter 13 of the book completed). There is a plan to modify the REPL to make it more comfortable to use and add a special `require` function to load libraries (and extract the mathematical functions into a library).

All variables, class attributes and functions are type-hinted, except where doing so would lead to circular imports.
