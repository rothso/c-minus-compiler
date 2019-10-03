C- Compiler
===========================
> A recursive descent parser for C- built for COP 4620.

## Structure

### Lexer
The lexer scans the input file and outputs a list of tokens. The head of the input is continually
matched to regex groups that capture the various types of tokens recognized by the parser. Block
and line comments are stripped before processing.

The lexer was [originally written in ReasonML](https://github.com/rothso/c-minus-lexer).

### Parser
The grammar was fixed by hand and implemented using a recursive descent parser. The program
tokenizes the input file and feeds the list of tokens into the parser. The parser peeks at the
head of the list when deciding which rule to follow, and pops the head when accepting (consuming)
a token. The parser throws an error if the expected popped token is not the expected token.

### Semantic Analyzer
The semantic analyzer consumes an abstract syntax tree (AST) generated by the parser. The
analyzer visits each node on the tree and performs the relevant semantic checks on that node.
Scope is handled with a dictionary of defined functions, a dictionary of variables in  the
current scope, and a list of all open scopes. The analyzer throws an error if the semantic rule
is violated.

### Intermediate Code Generator

The intermediate code generator that outputs quadruples for C- according to the operators used in
class. The code generator consumes an abstract syntax tree (AST) generated by the parser and
validated by the semantic analyzer. The code generator visits each node and generates a set of
quadruples for that node, recursively calling children nodes to build the list. The results of
intermediate expressions are assigned to temporary variables. Branch destinations are first
computed as relative jumps and then converted to absolute jumps upon a second pass of the
resulting quadruples list. The resulting list is printed with line numbers. If the input program
 is an invalid C- program, nothing will be printed.

## Source files

Source files are located in the compiler/ directory. It contains the following files:

```
lexer.py             Contains the tokenizer logic, which splits the input file into tokens
parser.py            Contains the handwritten recursive descent parser and commented grammar
semantics.py         Contains the semantic analyzer, which operates on an abstract syntax tree
astnodes.py          Contains the classes for the nodes of the abstract syntax tree
codegen.py           Contains the code generator, which operates on an abstract syntax tree
main.py              Calls the parser, lexer, analyzer, and code generator and displays the list
```

## Running

Requires Python 3.6 or higher.

```shell
$ git clone https://github.com/rothso/c-minus.git
$ cd c-minus
$ python3 main.py input.txt
```

**Input:** The program requires an [input file](input.txt) to be passed as the first argument. <br>
**Output:** A list of quadruples if the input file is a semantically-valid C- program, and
 nothing if it is not.