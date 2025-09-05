# Build Your Own Programming Language in Python
# Sept. 12th, 2025 @ Hack the North

# ---------- Symbols ----------
class Symbol(str):
    pass


# ---------- Tokenizer ----------
def tokenize(code):
    tokens = []
    i, n = 0, len(code)
    while i < n:
        c = code[i]
        if c in " \t\r\n":
            i += 1; continue
        if c == ';':
            while i < n and code[i] != '\n': i += 1
            continue
        if c == '(':
            tokens.append('('); i += 1; continue
        if c == ')':
            tokens.append(')'); i += 1; continue
        if c == '"':
            i += 1; start = i
            while i < n and code[i] != '"': i += 1
            if i >= n: raise Exception("Lex error: unterminated string")
            tokens.append(('STR', code[start:i])); i += 1
            continue
        start = i
        while i < n and code[i] not in " \t\r\n()\";":
            i += 1
        tokens.append(code[start:i])
    return tokens


# ---------- Parser ----------
def parse(tokens):
    def read_expr(pos):
        if pos >= len(tokens): raise Exception("Parse error: unexpected end")
        tok = tokens[pos]
        if tok == '(':
            pos += 1; items = []
            while pos < len(tokens) and tokens[pos] != ')':
                node, pos = read_expr(pos); items.append(node)
            if pos >= len(tokens): raise Exception("Parse error: missing ')'")
            return items, pos + 1
        if isinstance(tok, tuple) and tok[0] == 'STR':
            return tok[1], pos + 1
        return atom(tok), pos + 1

    def atom(tok):
        if tok == 'true': return True
        if tok == 'false': return False
        if tok.isdigit() or (len(tok) > 1 and tok[0] in '+-' and tok[1:].isdigit()):
            return int(tok)
        return Symbol(tok)

    forms, pos = [], 0
    while pos < len(tokens):
        node, pos = read_expr(pos); forms.append(node)
    return forms


# ---------- Environment & Procedure ----------
class Env:
    def __init__(self, outer=None):
        self.data, self.outer = {}, outer
    def get(self, k):
        if k in self.data: return self.data[k]
        if self.outer is not None: return self.outer.get(k)
        raise NameError(f"unbound symbol: {k}")
    def set(self, k, v):
        self.data[k] = v

class Procedure:
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    def __call__(self, args, eval_fn):
        if len(args) != len(self.params):
            raise TypeError("arity mismatch")
        local = Env(self.env)
        for name, val in zip(self.params, args):
            local.set(name, val)
        result = None
        for expr in self.body:
            result = eval_fn(expr, local)
        return result


# ---------- Built-ins ----------
def _binop2(name, f):
    def op(*args):
        if len(args) != 2: raise TypeError(f"'{name}' needs 2 args")
        return f(args[0], args[1])
    return op

def builtin_print(*args):
    s = " ".join(str(a) for a in args)
    print(s)
    return args[-1] if args else None

def standard_env():
    e = Env()
    
    # arithmetic
    e.set(Symbol('+'), _binop2('+', lambda a,b: a + b))
    e.set(Symbol('-'), _binop2('-', lambda a,b: a - b))
    e.set(Symbol('*'), _binop2('*', lambda a,b: a * b))
    e.set(Symbol('/'), _binop2('/', lambda a,b: float(a) / float(b)))

    # comparisons
    e.set(Symbol('='),  _binop2('=',  lambda a,b: a == b))
    e.set(Symbol('<'),  _binop2('<',  lambda a,b: a < b))
    e.set(Symbol('>'),  _binop2('>',  lambda a,b: a > b))
    e.set(Symbol('<='), _binop2('<=', lambda a,b: a <= b))
    e.set(Symbol('>='), _binop2('>=', lambda a,b: a >= b))

    # print
    e.set(Symbol('print'), builtin_print)
    
    # booleans
    e.set(Symbol('true'), True)
    e.set(Symbol('false'), False)
    return e


# ---------- Evaluator ----------
def lisp_eval(x, env):
    """
    Evaluate an expression x in environment env.
    Inputs come from the parser:
      - numbers -> int, strings -> str, booleans -> bool
      - symbols -> Symbol (e.g. 'define', 'begin', 'if')
      - lists -> Python list [head, arg1, arg2, ...]
    """


# ---------- Runner ----------
def run(source, base_env=None):
    tokens = tokenize(source)
    forms  = parse(tokens)
    env    = base_env or standard_env()
    last = None
    for form in forms:
        last = lisp_eval(form, env)
    return last, env


if __name__ == "__main__":
    test_env = standard_env()
    while True:
        program = input('> ')
        run(program, test_env)