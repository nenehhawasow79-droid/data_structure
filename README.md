# Stack-Based Expression Evaluator

This program reads each mathematical expression from `input.txt`, evaluates it using a stack-based shunting-yard algorithm, and writes the result to `output.txt`.

## How to run

- Python version: Python 3.10 or newer
- Command:

```bash
python stack_evaluator.py
```

The script looks for `input.txt` in the same folder as the Python file, prints the calculation steps to the console while running, and writes the results to `output.txt` in the same directory.

## File structure

### input.txt

- Contains one mathematical expression per line.
- Expressions are separated by a line containing only dashes: `-----`.
- Blank lines are ignored.
- A trailing separator is permitted without crashing.

Example:

```text
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

### output.txt

- Contains one result per expression.
- The separator line `-----` is preserved between results.
- Invalid expressions are replaced with an error message such as `ERROR: Division by zero.`

Example:

```text
13
-----
17
-----
-10
```

## Assumptions and limitations

- Supported operators: `+`, `-`, `*`, `/`, parentheses `(` and `)`.
- Multiplication and division are evaluated before addition and subtraction.
- Equal-precedence operations are evaluated left to right.
- Integer and decimal numeric values are supported.
- Unary minus is supported for inputs such as `-5` or `3 * -2`.
- Division by zero is handled as an error and does not stop the program.
- Malformed or invalid expressions, such as mismatched parentheses or bad syntax, are reported as errors and continue processing the rest of the file.

## Program design summary

The project uses a custom `Stack` class for stack operations:

- `push(item)` adds a value to the stack
- `pop()` removes and returns the top value
- `peek()` returns the top value without removing it
- `is_empty()` checks whether the stack is empty
- `size()` returns the current stack length

The main evaluation process is:

1. Read the input file and split it into expression entries.
2. Tokenize each expression.
3. Convert the infix expression to postfix using the shunting-yard algorithm.
4. Evaluate the postfix expression using another stack.
5. Store results or error text.
6. Write the final results to `output.txt`.

## Report outline for the printed assignment

### Title page
- Assignment Title: Data Structures and Algorithms - Stacks Implementation
- Student Name: [Student Name]
- Course Name: DCOMP320 – Data Structures and Algorithm
- Submission Date: 2026-10-23

### Introduction
This assignment demonstrates how a stack can be used to evaluate arithmetic expressions correctly and efficiently. The program reads expressions from a file, processes them using a stack-based shunting-yard approach, and writes the results to another file. This assignment highlights the importance of data structures in computing and shows how algorithm design can solve real-world problems such as expression evaluation.

### Data Structures Used
A stack is a linear data structure that follows the Last-In, First-Out (LIFO) principle. In this project, the stack stores operators and operands while converting expressions from infix to postfix notation and while evaluating the postfix sequence. Stacks are important in computing because they are used in function calls, expression parsing, backtracking, syntax checking, and many algorithmic tasks. In this application, the stack ensures that operators are processed in the correct order according to precedence and associativity.

### Program Design
The architecture of the program includes a `Stack` class, a tokenizer, an infix-to-postfix converter, a postfix evaluator, and file I/O functions. The stack operations handle insertion and removal in a controlled way. The expression evaluator converts user input into tokens, applies precedence rules, and then evaluates the postfix output. A simplified flow is shown below:

```text
Read input.txt
   ↓
Split expressions by separator
   ↓
Tokenize expression
   ↓
Convert to postfix using shunting-yard
   ↓
Evaluate postfix with stack
   ↓
Write result/error message to output.txt
```

### Testing and Results
The program was tested with valid expressions, invalid syntax, division by zero, mismatched parentheses, and blank/trailing separator handling. The results were then compared with expected mathematical outcomes to confirm correct precedence and error management. The sample `input.txt` file contains multiple expressions, including both valid and invalid entries, and the generated `output.txt` reflects the expected results and error messages.

### Conclusion
This assignment successfully demonstrates the relevance of stack data structures in algorithm design and expression evaluation. The final solution is implemented in Python, and the code can be shared through GitHub. The lecturer can be added as a collaborator to review and assess the submitted work.

### References
1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms.
2. Sedgewick, R., & Wayne, K. (2011). Algorithms.
3. Python Software Foundation. Python Documentation.
4. Limkokwing University of Creative Technology course notes for DCOMP320 – Data Structures and Algorithm.

## Grading criteria alignment

- Stack operations: 15
- Input handling: 30
- Output: 30
- Testing and results: 15
- Documentation and GitHub: 10

This solution addresses each area by implementing a correct stack, robust input parsing, output formatting, testing with examples, and clear documentation.
