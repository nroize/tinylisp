# tinylisp

A tiny Lisp interpreter in about 200 lines of plain Python, written for the
**"Build Your Own Programming Language in Python"** workshop I ran at
[Hack the North 2025](https://hackthenorth.com/) (September 12, 2025).

The goal of the workshop is to show that a working programming language isn't
magic: it is a tokenizer, a parser, and an evaluator, and you can write all
three in one sitting.

## What's in the repo

| File | What it is |
| --- | --- |
| [`tinylisp.py`](tinylisp.py) | The **starter file** for the workshop. The tokenizer, parser, environments, procedures, built-ins and REPL are done. `lisp_eval` is left empty for you to write. |
| [`tinylisp_completed.py`](tinylisp_completed.py) | The **finished interpreter**, with `lisp_eval` filled in. Use it to check your work or to see where you're headed. |

Apart from `lisp_eval` and the REPL loop, the two files are identical.

## Running it

You need Python 3, and nothing else.

```bash
python3 tinylisp_completed.py
```

This starts a REPL. Each line you type is run in the same environment, so
definitions stick around between lines. The REPL doesn't echo results, so use
`print` to see values:

```lisp
> (define x 10)
> (print "x is" x)
x is 10
> (define (square n) (* n n))
> (print (square 7))
49
```

Press `Ctrl+C` to quit.

## The language

### Values

- **Integers**: `42`, `-7`, `+3`
- **Strings**: `"hello world"` (no escape sequences)
- **Booleans**: `true`, `false`
- **Symbols**: any other token, like `x`, `square` or `<=`
- **Comments**: from `;` to the end of the line

Division always returns a float, so `(/ 7 2)` is `3.5`.

### Special forms

```lisp
(define name expr)              ; bind a variable
(define (fname a b) body ...)   ; define a function (body can have several expressions; the last one is returned)
(if test then else)             ; conditional; both branches are required
```

### Built-ins

| Name | Description |
| --- | --- |
| `+` `-` `*` `/` | Arithmetic (exactly two arguments each) |
| `=` `<` `>` `<=` `>=` | Comparisons (exactly two arguments each) |
| `print` | Prints its arguments separated by spaces and returns the last one |

### Example: recursion

```lisp
(define (fact n)
  (if (<= n 1)
      1
      (* n (fact (- n 1)))))
```

The REPL reads one line at a time, so type multi-line programs on a single
line, or pass them to `run` from Python:

```python
from tinylisp_completed import run

result, env = run("""
(define (fact n)
  (if (<= n 1) 1 (* n (fact (- n 1)))))
(fact 10)
""")
print(result)  # 3628800
```

## How it works

The interpreter has the classic three stages:

1. **Tokenizer** (`tokenize`): turns source text into tokens: `(`, `)`,
   strings, and everything else as raw words. Whitespace and `;` comments are
   skipped.
2. **Parser** (`parse`): turns tokens into nested Python lists. Numbers become
   `int`, `true`/`false` become `bool`, strings stay `str`, and every other
   word becomes a `Symbol`.
3. **Evaluator** (`lisp_eval`): walks that tree:
   - a `Symbol` is looked up in the environment;
   - any other atom (number, string, boolean) evaluates to itself;
   - `define` and `if` are handled as special forms;
   - anything else is a function call: evaluate the head and the arguments,
     then call either a user-defined `Procedure` or a Python built-in.

Scoping is handled by `Env`, a dictionary with a pointer to its outer
environment. Each function call creates a new `Env` whose parent is the
environment the function was *defined* in, which gives you lexical scope and
closures for free.

## Workshop exercise

Open `tinylisp.py` and implement `lisp_eval(x, env)`. The docstring tells you
what shapes of input the parser produces. A good order to tackle it in:

1. Symbols and literal atoms
2. Function calls (built-ins first, then `Procedure`s)
3. `if`
4. `define`, both the variable form and the function form

Run `python3 tinylisp.py` and try the examples above as you go.

### Ideas to keep going

- Add `begin` to run several expressions in sequence
- Add `lambda` for anonymous functions
- Make `+` and `*` take any number of arguments
- Add list operations: `list`, `car`, `cdr`, `cons`
- Add floating-point literals like `3.14`
- Make the REPL print the result of each expression
