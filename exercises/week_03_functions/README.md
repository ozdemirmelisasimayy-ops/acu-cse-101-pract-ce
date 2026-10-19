# Week 03: Functions

**Think Python:** Chapter 3

Learn to define a function with `def`, pass arguments to its parameters, and
send a result back with `return`. Indent the statements inside each function.

- [`practice.py`](practice.py): guided workshop on a welcome message, doubling a number, and adding two numbers.
- [`challenge.py`](challenge.py): three independent graded challenges.

Both files start without solutions. Replace each `pass` with your own code.
No user input, imports, loops, or conditions are needed.

## Three graded challenges

| Function | What to return | Example |
|---|---|---|
| `greet(name)` | A personal greeting | `greet("Ada")` → `"Hello, Ada!"` |
| `square(number)` | The number multiplied by itself | `square(4)` → `16` |
| `minutes_to_seconds(minutes)` | Minutes converted to seconds | `minutes_to_seconds(2)` → `120` |

Use the parameters so your functions work with different arguments, including
zero for calculations, negative numbers for squares, and fractional minutes.
The challenge functions must **return** results. Printing an answer does not
return it to the caller.

## Checking your work

Use **Run Tests** in **Course Tasks**, then select Week 03. This checks the graded
challenges. You can also run:

```bash
python3 -m pytest exercises/week_03_functions/test_challenge.py
```

Check the workshop separately:

```bash
python3 -m pytest exercises/week_03_functions/test_practice.py
```

Tests will fail until you complete the functions. They call each function with
different arguments and check the returned values, or the workshop welcome output.

## Submitting

After the challenge tests pass, use **Submit** in **Course Tasks** and select Week 03.
