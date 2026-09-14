"""
Python Cheat Sheet — Desktop Reference Tool
============================================
A floating, searchable, always-handy Python reference card.

Features
--------
- Instant search across name / description / code / leetcode notes
- Category dropdown filter
- Two-pane layout: browsable list (left) + detail viewer (right)
- One-click code copy
- Add your own custom snippets (saved to disk between sessions)
- Pin-to-top toggle + draggable frameless-style title bar
- Covers Python basics AND every function from
  https://docs.python.org/3/library/functions.html
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ══════════════════════════════════════════════════════════════════════════
# DATA — core language cheat sheet
# ══════════════════════════════════════════════════════════════════════════
CHEAT_DATA = [
    # ── BASICS ──────────────────────────────────────────────────────────
    {"category": "Basics", "name": "print()",
     "description": "The most common way to show output. Prints any number of "
                     "values to the console, converting each to a string first.",
     "syntax": 'print("Hello World")\nprint("Age:", 25)',
     "leetcode": ""},
    {"category": "Basics", "name": "input()",
     "description": "Pauses the program, shows a prompt, and waits for the user "
                     "to type something. Always returns a string.",
     "syntax": 'name = input("What\'s your name? ")\nprint(f"Hi {name}!")',
     "leetcode": ""},
    {"category": "Basics", "name": "Comments",
     "description": "A # starts a comment — everything after it on that line "
                     "is ignored by Python. Use comments to explain *why*, not *what*.",
     "syntax": '# This is a comment\nprint("This is code")  # inline comment too',
     "leetcode": ""},
    {"category": "Basics", "name": "Variables",
     "description": "A variable gives a name to a piece of data, like a labelled "
                     "box. Python is dynamically typed, so a variable's type can change.",
     "syntax": 'my_name = "Angela"\nmy_age = 12\nmy_age = "twelve"  # allowed!',
     "leetcode": ""},
    {"category": "Basics", "name": "The += Operator",
     "description": "Shorthand for 'take the current value and add to it'. "
                     "Also works as -=, *=, /=, //=, **=, %=.",
     "syntax": 'my_age = 12\nmy_age += 4   # my_age is now 16\nmy_age -= 1   # now 15',
     "leetcode": ""},

    # ── DATA TYPES ──────────────────────────────────────────────────────
    {"category": "Data Types", "name": "Integers",
     "description": "Whole numbers with no decimal point, positive or negative, "
                     "of unlimited size in Python.",
     "syntax": 'my_number = 354\nbig = 10**20  # ints never overflow',
     "leetcode": ""},
    {"category": "Data Types", "name": "Floating Point Numbers",
     "description": "Numbers with a decimal point. Any division that isn't "
                     "exact returns a float, and float math can have tiny rounding errors.",
     "syntax": 'my_float = 3.14159\nprint(0.1 + 0.2)  # 0.30000000000000004',
     "leetcode": ""},
    {"category": "Data Types", "name": "Strings",
     "description": "An immutable sequence of characters, written with single, "
                     "double, or triple quotes.",
     "syntax": 'my_string = "Hello"\nmulti = """line1\nline2"""',
     "leetcode": ""},
    {"category": "Data Types", "name": "String Concatenation",
     "description": "Joining strings together with +. Only works string-to-string; "
                     "convert numbers with str() first.",
     "syntax": '"Hello" + " " + "Angela"\n# "Hello Angela"',
     "leetcode": ""},
    {"category": "Data Types", "name": "Escaping a String",
     "description": "Use a backslash to include a character (like a quote) that "
                     "would otherwise end the string early.",
     "syntax": 'speech = "She said: \\"Hi\\""\nprint(speech)\n# She said: "Hi"',
     "leetcode": ""},
    {"category": "Data Types", "name": "F-Strings",
     "description": "The modern way to embed variables/expressions inside a "
                     "string. Prefix with f and wrap the code in {}.",
     "syntax": 'days = 365\nprint(f"There are {days} days, "\n      f"or {days*24} hours")',
     "leetcode": ""},
    {"category": "Data Types", "name": "Converting Data Types",
     "description": "Convert between types with int(), float(), or str(). "
                     "Fails with a ValueError if the value can't be converted.",
     "syntax": 'n = 354\nfloat(n)     # 354.0\nstr(n)       # "354"\nint("42")    # 42',
     "leetcode": ""},
    {"category": "Data Types", "name": "Checking Data Types",
     "description": "Use type() to see a variable's exact type, or isinstance() "
                     "to check it (or a subclass of it) more flexibly.",
     "syntax": 'n = 3.14159\ntype(n)              # <class \'float\'>\nisinstance(n, float) # True',
     "leetcode": ""},

    # ── MATHS ───────────────────────────────────────────────────────────
    {"category": "Maths", "name": "Arithmetic Operators",
     "description": "Core mathematical operators. / always returns a float; "
                     "// performs floor (integer) division.",
     "syntax": '3 + 2    # Add -> 5\n4 - 1    # Subtract -> 3\n2 * 3    # Multiply -> 6\n5 / 2    # Divide -> 2.5\n5 // 2   # Floor divide -> 2\n5 ** 2   # Exponent -> 25',
     "leetcode": ""},
    {"category": "Maths", "name": "The += Operator (Maths)",
     "description": "Combines the value with an operation and reassigns it in "
                     "one step — cleaner than writing x = x + 2.",
     "syntax": 'my_number = 4\nmy_number += 2   # 6\nmy_number *= 3   # 18',
     "leetcode": ""},
    {"category": "Maths", "name": "The Modulo Operator",
     "description": "Returns the remainder after division (%). The classic way "
                     "to test odd/even, or to 'wrap around' a range of numbers.",
     "syntax": '5 % 2        # 1\n10 % 2 == 0  # True -> even',
     "leetcode": "Happy Number, Add Digits — modulo splits off the last digit of a number."},

    # ── ERRORS ──────────────────────────────────────────────────────────
    {"category": "Errors", "name": "Syntax Error",
     "description": "Raised when code doesn't make sense to the parser at all — "
                     "a missing colon, mismatched brackets, or a typo in keywords.",
     "syntax": 'print(12 + 4))\n# SyntaxError: unmatched \')\'',
     "leetcode": ""},
    {"category": "Errors", "name": "Name Error",
     "description": "Raised when Python encounters a name it doesn't recognise — "
                     "usually a typo, or using a variable before it's defined. Names are case-sensitive.",
     "syntax": 'my_number = 4\nprint(my_Number)\n# NameError: name \'my_Number\' is not defined',
     "leetcode": ""},
    {"category": "Errors", "name": "Zero Division Error",
     "description": "Raised when dividing (or taking modulo) by zero — "
                     "mathematically undefined.",
     "syntax": '5 / 0\n# ZeroDivisionError: division by zero',
     "leetcode": ""},
    {"category": "Errors", "name": "Try / Except",
     "description": "Catches an exception instead of letting the program crash, "
                     "so you can handle bad input gracefully.",
     "syntax": 'try:\n    n = int(input("Number: "))\nexcept ValueError:\n    print("That was not a number.")\nfinally:\n    print("Done.")',
     "leetcode": ""},

    # ── FUNCTIONS ───────────────────────────────────────────────────────
    {"category": "Functions", "name": "Creating Functions",
     "description": "Bundle instructions under a name with def so you can run "
                     "them repeatedly. The body must be indented.",
     "syntax": 'def greet():\n    print("Hello")\n    name = input("Your name: ")\n    print(f"Hi {name}")',
     "leetcode": ""},
    {"category": "Functions", "name": "Calling Functions",
     "description": "Run a function by writing its name followed by parentheses.",
     "syntax": 'greet()\ngreet()\n# greet() runs twice',
     "leetcode": ""},
    {"category": "Functions", "name": "Functions with Inputs",
     "description": "Give a function parameters so it behaves differently "
                     "depending on the arguments passed in.",
     "syntax": 'def add(n1, n2):\n    print(n1 + n2)\n\nadd(2, 3)  # prints 5',
     "leetcode": ""},
    {"category": "Functions", "name": "Functions with Outputs",
     "description": "Use return to send a value back to the caller. Once "
                     "return runs, the function stops executing.",
     "syntax": 'def add(n1, n2):\n    return n1 + n2\n\nresult = add(2, 3)  # result is 5',
     "leetcode": ""},
    {"category": "Functions", "name": "Default Arguments",
     "description": "Give a parameter a fallback value used when the caller "
                     "doesn't supply one.",
     "syntax": 'def greet(name="friend"):\n    print(f"Hi {name}")\n\ngreet()          # Hi friend\ngreet("Angela")  # Hi Angela',
     "leetcode": ""},
    {"category": "Functions", "name": "Variable Scope",
     "description": "Variables created inside a function only exist while it "
                     "runs, and don't affect a same-named variable outside it.",
     "syntax": 'n = 2\ndef my_function():\n    n = 3\n    print(n)       # 3\n\nprint(n)           # 2\nmy_function()      # 3',
     "leetcode": ""},
    {"category": "Functions", "name": "Keyword Arguments",
     "description": "Pass arguments by name instead of position — order stops "
                     "mattering and the call becomes more readable.",
     "syntax": 'def divide(n1, n2):\n    return n1 / n2\n\ndivide(10, 5)         # positional\ndivide(n2=5, n1=10)   # keyword — same result',
     "leetcode": ""},
    {"category": "Functions", "name": "*args and **kwargs",
     "description": "*args collects extra positional arguments into a tuple; "
                     "**kwargs collects extra keyword arguments into a dict.",
     "syntax": 'def total(*args, **kwargs):\n    print(args, kwargs)\n\ntotal(1, 2, 3, x=4)\n# (1, 2, 3) {\'x\': 4}',
     "leetcode": ""},
    {"category": "Functions", "name": "Lambda Functions",
     "description": "A small, anonymous, single-expression function — handy as "
                     "a throwaway argument to sorted(), map(), or filter().",
     "syntax": 'square = lambda x: x * x\nsquare(5)   # 25\nsorted(["bb","a"], key=lambda s: len(s))',
     "leetcode": "Sort strings/tuples by a custom key without writing a full def."},

    # ── CONDITIONALS ────────────────────────────────────────────────────
    {"category": "Conditionals", "name": "If",
     "description": "Tests whether a condition is true. If it is, the indented "
                     "block underneath runs; otherwise it's skipped.",
     "syntax": 'n = 5\nif n > 2:\n    print("Larger than 2")',
     "leetcode": ""},
    {"category": "Conditionals", "name": "Else",
     "description": "Runs a fallback block when the if condition is false.",
     "syntax": 'age = 18\nif age > 16:\n    print("Can drive")\nelse:\n    print("Can\'t drive")',
     "leetcode": ""},
    {"category": "Conditionals", "name": "Elif",
     "description": "Chains extra conditions to check if the first is false. "
                     "As soon as one branch is true, the rest are skipped.",
     "syntax": 'weather = "sunny"\nif weather == "rain":\n    print("bring umbrella")\nelif weather == "sunny":\n    print("bring sunglasses")\nelse:\n    print("check the forecast")',
     "leetcode": ""},
    {"category": "Conditionals", "name": "and / or / not",
     "description": "Combine or invert boolean conditions. 'and' needs both "
                     "sides true, 'or' needs at least one, 'not' flips a result.",
     "syntax": 's = 58\nif s < 60 and s > 50:\n    print("Grade C")\n\nif s < 50 or s > 90:\n    print("edge case")\n\nif not s == 100:\n    print("not perfect")',
     "leetcode": ""},
    {"category": "Conditionals", "name": "Comparison Operators",
     "description": "Compare two values, always producing True or False. "
                     "Chaining like 1 < x < 10 is valid Python.",
     "syntax": '>   greater than\n<   less than\n>=  greater or equal\n<=  less or equal\n==  equal to\n!=  not equal to',
     "leetcode": ""},
    {"category": "Conditionals", "name": "Ternary Expression",
     "description": "A compact one-line if/else that evaluates to a value, "
                     "instead of running statements.",
     "syntax": 'age = 20\nstatus = "adult" if age >= 18 else "minor"',
     "leetcode": ""},

    # ── LOOPS ───────────────────────────────────────────────────────────
    {"category": "Loops", "name": "While Loop",
     "description": "Repeats a block for as long as its condition stays true. "
                     "Be careful to update something inside it, or it never ends.",
     "syntax": 'n = 1\nwhile n < 100:\n    n += 1',
     "leetcode": ""},
    {"category": "Loops", "name": "For Loop",
     "description": "Iterates over any iterable — a list, string, dict, tuple, "
                     "or range — running the block once per item.",
     "syntax": 'all_fruits = ["apple", "banana", "orange"]\nfor fruit in all_fruits:\n    print(fruit)',
     "leetcode": ""},
    {"category": "Loops", "name": "_ in a For Loop",
     "description": "When the loop variable isn't needed, using an underscore "
                     "signals 'I'm intentionally ignoring this value'.",
     "syntax": 'for _ in range(100):\n    print("hi")  # runs 100 times',
     "leetcode": ""},
    {"category": "Loops", "name": "break",
     "description": "Immediately exits the closest enclosing for/while loop.",
     "syntax": 'scores = [34, 67, 99, 105]\nfor s in scores:\n    if s > 100:\n        print("Invalid")\n        break\n    print(s)',
     "leetcode": ""},
    {"category": "Loops", "name": "continue",
     "description": "Skips straight to the next iteration, without running the "
                     "rest of the current one.",
     "syntax": 'n = 0\nwhile n < 10:\n    n += 1\n    if n % 2 == 0:\n        continue\n    print(n)   # prints odd numbers only',
     "leetcode": ""},
    {"category": "Loops", "name": "Infinite Loops",
     "description": "A loop whose condition never becomes false runs forever. "
                     "Usually a bug — unless intentionally combined with break.",
     "syntax": 'while True:\n    answer = input("quit? ")\n    if answer == "yes":\n        break',
     "leetcode": ""},
    {"category": "Loops", "name": "List/Dict Comprehensions",
     "description": "A concise, expressive way to build a new list, set, or "
                     "dict by transforming/filtering an existing iterable.",
     "syntax": 'squares = [x*x for x in range(6)]\nevens = [x for x in range(10) if x % 2 == 0]\nlookup = {x: x*x for x in range(5)}',
     "leetcode": "Two Sum, Group Anagrams — comprehensions build result lists concisely."},

    # ── LIST METHODS ────────────────────────────────────────────────────
    {"category": "List Methods", "name": "Adding Lists Together",
     "description": "Combine two lists into a new one with +, or extend one "
                     "in place with += or .extend().",
     "syntax": 'list1 = [1, 2, 3]\nlist2 = [9, 8, 7]\nnew_list = list1 + list2\nlist1 += list2   # extends list1 in place',
     "leetcode": ""},
    {"category": "List Methods", "name": ".append() / .insert()",
     "description": "append() adds one item to the end; insert() adds it at a "
                     "specific index, shifting later items right.",
     "syntax": 'fruits = ["apple", "banana"]\nfruits.append("pear")\nfruits.insert(1, "kiwi")\n# [\'apple\', \'kiwi\', \'banana\', \'pear\']',
     "leetcode": ""},
    {"category": "List Methods", "name": "List Index & Slicing",
     "description": "Access one item with [i] (negative indexes count from "
                     "the end), or a sub-list with [start:end:step].",
     "syntax": 'letters = ["a","b","c","d"]\nletters[0]     # \'a\'\nletters[-1]    # \'d\'\nletters[1:3]   # [\'b\', \'c\']\nletters[::-1]  # reversed list',
     "leetcode": "Rotate Array, Reverse String — slicing does both in one line."},
    {"category": "List Methods", "name": ".pop() / .remove()",
     "description": "pop() removes and returns an item by index (last item "
                     "by default); remove() deletes the first item matching a value.",
     "syntax": 'nums = [1, 2, 3, 4]\nnums.pop()       # removes & returns 4\nnums.remove(2)   # removes value 2 -> [1, 3]',
     "leetcode": ""},
    {"category": "List Methods", "name": ".sort() vs sorted()",
     "description": ".sort() sorts a list in place and returns None; sorted() "
                     "returns a brand-new sorted list, leaving the original untouched.",
     "syntax": 'nums = [3, 1, 2]\nnums.sort()          # nums is now [1, 2, 3]\n\nnums2 = [3, 1, 2]\nresult = sorted(nums2)  # nums2 unchanged, result is new',
     "leetcode": "Merge Intervals, Meeting Rooms II — sort first, then sweep."},

    # ── MODULES ─────────────────────────────────────────────────────────
    {"category": "Modules", "name": "Importing",
     "description": "Some modules ship with Python (random, math, datetime); "
                     "third-party ones are installed from PyPI with pip.",
     "syntax": 'import random\nn = random.randint(3, 10)',
     "leetcode": ""},
    {"category": "Modules", "name": "Aliasing",
     "description": "Use 'as' to give an imported module a shorter, "
                     "conventional nickname.",
     "syntax": 'import random as r\nimport numpy as np\nn = r.randint(1, 5)',
     "leetcode": ""},
    {"category": "Modules", "name": "Importing from Modules",
     "description": "Pull specific names out of a module with 'from ... import' "
                     "so you can use them without the module prefix.",
     "syntax": 'from random import randint\nn = randint(1, 5)',
     "leetcode": ""},
    {"category": "Modules", "name": "Importing Everything",
     "description": "The wildcard * imports every public name from a module. "
                     "Convenient but hurts readability — use sparingly.",
     "syntax": 'from random import *\nmy_list = [1, 2, 3]\nchoice(my_list)',
     "leetcode": ""},
    {"category": "Modules", "name": "Randomisation",
     "description": "The random module generates pseudo-random numbers and "
                     "choices. randint()'s start and end are both inclusive.",
     "syntax": 'import random\nrandom.randint(2, 5)     # int, 2 to 5 inclusive\nrandom.random()          # float, 0.0 to 1.0\nrandom.choice([1,2,3])   # random element',
     "leetcode": ""},

    # ── CLASSES & OBJECTS ───────────────────────────────────────────────
    {"category": "Classes & Objects", "name": "Creating a Python Class",
     "description": "Define a blueprint for objects with the class keyword. "
                     "Class names use PascalCase by convention.",
     "syntax": 'class MyClass:\n    pass',
     "leetcode": ""},
    {"category": "Classes & Objects", "name": "Creating an Object from a Class",
     "description": "Call the class name like a function to create ('instantiate') "
                     "a new object from it.",
     "syntax": 'class Car:\n    pass\n\nmy_toyota = Car()',
     "leetcode": ""},
    {"category": "Classes & Objects", "name": "Class Methods (Instance Methods)",
     "description": "A function defined inside a class is called a method. "
                     "Its first parameter, self, refers to the calling instance.",
     "syntax": 'class Car:\n    def drive(self):\n        print("vroom")\n\nmy_honda = Car()\nmy_honda.drive()',
     "leetcode": ""},
    {"category": "Classes & Objects", "name": "Class Variables",
     "description": "A variable defined directly in the class body is shared "
                     "by every instance, unless overridden per-object.",
     "syntax": 'class Car:\n    wheels = 4\n\ncar1 = Car()\nprint(car1.wheels)  # 4',
     "leetcode": ""},
    {"category": "Classes & Objects", "name": "The __init__ Method",
     "description": "A special method automatically called every time a new "
                     "object is created — used to set up initial state.",
     "syntax": 'class Car:\n    def __init__(self):\n        print("Building car")\n\nmy_toyota = Car()  # prints "Building car"',
     "leetcode": ""},
    {"category": "Classes & Objects", "name": "Class Properties (Attributes)",
     "description": "Store per-object data by assigning to self inside "
                     "__init__, so every instance can have its own values.",
     "syntax": 'class Car:\n    def __init__(self, name):\n        self.name = name\n\nmy_car = Car("Jimmy")\nprint(my_car.name)  # Jimmy',
     "leetcode": ""},
    {"category": "Classes & Objects", "name": "Class Inheritance",
     "description": "A new class can inherit the methods/properties of an "
                     "existing one, and override or extend them with super().",
     "syntax": 'class Animal:\n    def breathe(self):\n        print("breathing")\n\nclass Fish(Animal):\n    def breathe(self):\n        super().breathe()\n        print("underwater")\n\nFish().breathe()\n# breathing\n# underwater',
     "leetcode": ""},
    {"category": "Classes & Objects", "name": "Dunder / Magic Methods",
     "description": "Double-underscore methods let your objects hook into "
                     "built-in behaviour like printing, equality, or length.",
     "syntax": 'class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n    def __repr__(self):\n        return f"Point({self.x}, {self.y})"\n    def __eq__(self, other):\n        return (self.x, self.y) == (other.x, other.y)',
     "leetcode": ""},
]

# ══════════════════════════════════════════════════════════════════════════
# DATA — every function on docs.python.org/3/library/functions.html
# ══════════════════════════════════════════════════════════════════════════
def _f(name, description, syntax, leetcode=""):
    return {"category": "Built-in Functions", "name": name,
            "description": description, "syntax": syntax, "leetcode": leetcode}


BUILTIN_FUNCTIONS = [
    _f("abs()",
       "Returns the absolute value of a number — strips a negative sign from "
       "an int/float, or returns the magnitude of a complex number.",
       'abs(-4.6)     # 4.6\nabs(-7)       # 7\nabs(3 + 4j)   # 5.0  (magnitude)',
       "Best Time to Buy and Sell Stock — compare abs() price differences."),
    _f("aiter()",
       "Returns an asynchronous iterator for an async iterable, equivalent to "
       "calling x.__aiter__(). Used with 'async for'. Added in Python 3.10.",
       'async def gen():\n    yield 1\n    yield 2\n\nasync def main():\n    it = aiter(gen())\n    print(await anext(it))  # 1'),
    _f("all()",
       "Returns True if every element of an iterable is truthy (or the "
       "iterable is empty). Short-circuits on the first falsy value.",
       'all([1, 2, 3])   # True\nall([1, 0, 3])   # False\nall([])          # True',
       "Valid Sudoku — check that every row/column/box satisfies a rule with all()."),
    _f("anext()",
       "The async version of next(): awaited to retrieve the next item from "
       "an async iterator, optionally returning a default when exhausted.",
       'async def main():\n    it = aiter(gen())\n    val = await anext(it, "done")'),
    _f("any()",
       "Returns True if at least one element of an iterable is truthy; "
       "returns False for an empty iterable.",
       'any([0, 0, 1])   # True\nany([0, 0, 0])   # False\nany([])          # False',
       "Contains Duplicate — any(count > 1 for count in counts.values())."),
    _f("ascii()",
       "Like repr(), but escapes every non-ASCII character using \\x, \\u, "
       "or \\U escape sequences — handy for ASCII-only logs.",
       'ascii("café")\n# "\'caf\\\\xe9\'"'),
    _f("bin()",
       "Converts an integer to a binary string prefixed with '0b'. Negative "
       "numbers get a leading minus sign.",
       'bin(10)   # \'0b1010\'\nbin(-5)   # \'-0b101\'',
       "Number of 1 Bits / Counting Bits — bin(n).count('1') counts set bits."),
    _f("bool()",
       "Converts a value to True or False using Python's truthiness rules "
       "(0, '', [], None, {} are falsy; almost everything else is truthy).",
       'bool(0)      # False\nbool("")     # False\nbool([1])    # True\nbool("no")   # True (non-empty string!)'),
    _f("breakpoint()",
       "Drops you into the interactive debugger (pdb) at the exact line it's "
       "called — a shortcut for 'import pdb; pdb.set_trace()'.",
       'def calc(a, b):\n    breakpoint()   # execution pauses here\n    return a + b'),
    _f("bytearray()",
       "Creates a mutable sequence of bytes (integers 0-255). Build it from "
       "a size, a string + encoding, or any iterable of ints.",
       'ba = bytearray(5)              # 5 zero bytes\nba2 = bytearray("hi", "utf-8")\nba2[0] = 72                     # mutate in place'),
    _f("bytes()",
       "Creates an immutable sequence of bytes with the same construction "
       "rules as bytearray, but it can never be modified after creation.",
       'b = bytes("hi", "utf-8")\nb2 = bytes([104, 105])\n# b == b2  -> True'),
    _f("callable()",
       "Returns True if the object appears to support being called like a "
       "function (i.e. it has a __call__ method).",
       'callable(print)   # True\ncallable(42)      # False\ncallable(lambda: 1)  # True'),
    _f("chr()",
       "Returns the one-character string for a given Unicode code point — "
       "the inverse of ord().",
       "chr(97)     # 'a'\nchr(8364)   # '€'",
       "Caesar Cipher / Encode & Decode Strings shift letters with chr()/ord()."),
    _f("classmethod()",
       "A decorator that turns a method into a class method, so it receives "
       "the class itself (cls) as its first argument instead of an instance.",
       'class Pizza:\n    def __init__(self, toppings):\n        self.toppings = toppings\n\n    @classmethod\n    def margherita(cls):\n        return cls(["mozzarella", "tomato"])'),
    _f("compile()",
       "Compiles a source string (or AST) into a code object that can later "
       "be executed with exec() or eval().",
       'code = compile("print(1 + 2)", "<string>", "exec")\nexec(code)   # 3'),
    _f("complex()",
       "Creates a complex number from real and imaginary parts, or by "
       "parsing a string like '1+2j'.",
       'complex(2, 3)      # (2+3j)\ncomplex("1+2j")    # (1+2j)\n(2+3j).real, (2+3j).imag   # 2.0, 3.0'),
    _f("delattr()",
       "Deletes a named attribute from an object — equivalent to writing "
       "'del obj.name'.",
       'class P: pass\np = P()\np.x = 5\ndelattr(p, "x")   # same as: del p.x'),
    _f("dict()",
       "Creates a new dictionary from keyword arguments, a mapping, or an "
       "iterable of key-value pairs.",
       'dict(a=1, b=2)                # {\'a\': 1, \'b\': 2}\ndict([("a", 1), ("b", 2)])    # {\'a\': 1, \'b\': 2}',
       "Two Sum — a dict maps each seen value to its index for O(n) lookup."),
    _f("dir()",
       "Without arguments, lists names in the current scope. With an object, "
       "lists its valid attributes and methods — great for exploring an API.",
       'dir([])[-3:]        # last few list methods, e.g. [\'sort\', ...]\ndir()               # names in current scope'),
    _f("divmod()",
       "Returns (a // b, a % b) — quotient and remainder — in a single call, "
       "which is both convenient and slightly faster than computing separately.",
       'divmod(17, 5)   # (3, 2)\nminutes, seconds = divmod(125, 60)   # 2, 5',
       "Useful in problems that convert a total into (hours, minutes) etc."),
    _f("enumerate()",
       "Wraps an iterable to produce (index, value) pairs, saving you from "
       "manually tracking a counter variable in a loop.",
       'for i, fruit in enumerate(["a", "b", "c"], start=1):\n    print(i, fruit)\n# 1 a\n# 2 b\n# 3 c',
       "Two Sum II, Rotate Array — enumerate() gives index + value together."),
    _f("eval()",
       "Parses and evaluates a single Python *expression* given as a string, "
       "returning its value. Never eval() untrusted input — it's a security risk.",
       'x = 1\neval("x + 1")     # 2\neval("2 + 3 * 4") # 14'),
    _f("exec()",
       "Executes a string (or code object) containing arbitrary Python "
       "*statements*. Always returns None. Same security caveat as eval().",
       'exec("x = 5\\nprint(x * 2)")\n# 10'),
    _f("filter()",
       "Builds a lazy iterator of the elements from an iterable for which a "
       "function returns True. Pass None as the function to just drop falsy items.",
       'evens = list(filter(lambda x: x % 2 == 0, range(10)))\n# [0, 2, 4, 6, 8]',
       "Remove invalid entries before further processing in array problems."),
    _f("float()",
       "Converts a number or a numeric string into a floating-point number.",
       'float("3.14")   # 3.14\nfloat(7)        # 7.0\nfloat("-Infinity")  # -inf'),
    _f("format()",
       "Converts a value into a formatted string according to a format spec "
       "mini-language — useful for padding, decimal places, or number bases.",
       'format(3.14159, ".2f")   # \'3.14\'\nformat(255, "#x")        # \'0xff\'\nformat(7, "05d")         # \'00007\''),
    _f("frozenset()",
       "Returns an immutable, hashable version of a set — usable as a dict "
       "key or as an element inside another set, unlike a regular set.",
       'fs = frozenset([1, 2, 3])\nd = {fs: "immutable set as a key"}'),
    _f("getattr()",
       "Returns the value of a named attribute on an object; returns a "
       "default (or raises AttributeError) if it doesn't exist.",
       'class P:\n    x = 10\n\ngetattr(P, "x")          # 10\ngetattr(P, "y", "n/a")   # \'n/a\''),
    _f("globals()",
       "Returns a dictionary representing the current module's global "
       "symbol table — you can even read/modify it directly.",
       'x = 5\nglobals()["x"]     # 5\nglobals()["y"] = 9  # creates a new global y'),
    _f("hasattr()",
       "Returns True if the object has the named attribute, False otherwise "
       "(implemented by trying getattr() and catching AttributeError).",
       'hasattr("hello", "upper")   # True\nhasattr(5, "upper")         # False'),
    _f("hash()",
       "Returns the integer hash value of an object — used internally to "
       "place items in dicts/sets. Only hashable (typically immutable) types qualify.",
       'hash("abc")\nhash((1, 2))\n# hash([1,2]) would raise TypeError — lists aren\'t hashable'),
    _f("help()",
       "Launches Python's interactive help system, or prints documentation "
       "for whatever object/module/keyword you pass in.",
       'help(str.split)\nhelp(len)'),
    _f("hex()",
       "Converts an integer to a lowercase hexadecimal string prefixed with "
       "'0x'.",
       "hex(255)   # '0xff'\nhex(-42)   # '-0x2a'",
       "Convert a Number to Hexadecimal — hex() plus string slicing/formatting."),
    _f("id()",
       "Returns a unique integer that identifies an object for its lifetime "
       "— in CPython this is the object's memory address.",
       'a = []\nb = a\nid(a) == id(b)   # True, same object\nid(a) == id([])   # False, different objects'),
    _f("input()",
       "Prints an optional prompt, reads a line from standard input, and "
       "returns it as a string (with the trailing newline stripped).",
       'name = input("Your name: ")\nage = int(input("Your age: "))   # convert manually'),
    _f("int()",
       "Converts a number or string to an integer. An optional base "
       "(2-36) can be given when parsing a string.",
       'int("42")        # 42\nint("101", 2)    # 5  (binary)\nint(3.9)         # 3  (truncates toward zero)'),
    _f("isinstance()",
       "Returns True if an object is an instance of a given type (or a "
       "subclass of it). classinfo can also be a tuple of types.",
       'isinstance(5, int)             # True\nisinstance(5, (int, float))    # True\nisinstance(True, int)          # True — bool is a subclass of int'),
    _f("issubclass()",
       "Returns True if a class is a subclass of another (a class counts as "
       "a subclass of itself too).",
       'issubclass(bool, int)   # True\nissubclass(int, bool)   # False'),
    _f("iter()",
       "Returns an iterator for an iterable object. A two-argument form, "
       "iter(callable, sentinel), calls callable repeatedly until it returns sentinel.",
       'it = iter([1, 2, 3])\nnext(it)   # 1\nnext(it)   # 2'),
    _f("len()",
       "Returns the number of items in a sequence or collection — strings, "
       "lists, tuples, dicts, sets, and ranges all support it.",
       'len("hello")    # 5\nlen([1, 2, 3])  # 3\nlen({"a": 1})   # 1',
       "Used everywhere for bounds checks — Sliding Window, Two Pointers, etc."),
    _f("list()",
       "Builds a new mutable list from the items of any iterable, or an "
       "empty list if no argument is given.",
       'list("abc")       # [\'a\', \'b\', \'c\']\nlist(range(3))    # [0, 1, 2]\nlist()            # []'),
    _f("locals()",
       "Returns a dictionary representing the current local symbol table — "
       "inside a function, this is the function's local variables.",
       'def f():\n    x = 5\n    y = 10\n    print(locals())   # {\'x\': 5, \'y\': 10}'),
    _f("map()",
       "Applies a function to every item of one or more iterables, "
       "returning a lazy iterator of the results.",
       'list(map(str, [1, 2, 3]))\n# [\'1\', \'2\', \'3\']\nlist(map(lambda a, b: a + b, [1, 2], [3, 4]))\n# [4, 6]',
       "Convert a list of digit-strings to ints before summing/comparing."),
    _f("max()",
       "Returns the largest item in an iterable, or the largest of two or "
       "more arguments. The 'key' argument customises how items are compared.",
       'max([3, 1, 4, 1, 5])                  # 5\nmax(["a", "bbb", "cc"], key=len)      # \'bbb\'\nmax(3, 7, 1)                          # 7',
       "Maximum Subarray, Kth Largest Element — max()/key= drives comparisons."),
    _f("memoryview()",
       "Creates a 'memory view' that exposes an object's internal buffer "
       "(e.g. bytes) without copying the underlying data.",
       'mv = memoryview(b"hello")\nmv[0]        # 104\nbytes(mv[1:3])  # b\'el\''),
    _f("min()",
       "Returns the smallest item in an iterable, or the smallest of two or "
       "more arguments. Supports the same 'key' argument as max().",
       'min([3, 1, 4, 1, 5])   # 1\nmin(3, 7, 1)            # 1',
       "Best Time to Buy and Sell Stock — track the running minimum price seen so far."),
    _f("next()",
       "Retrieves the next item from an iterator by calling its __next__() "
       "method; returns a default (instead of raising StopIteration) if given.",
       'it = iter([1, 2])\nnext(it)          # 1\nnext(it)          # 2\nnext(it, "done")  # \'done\' — no StopIteration raised'),
    _f("object()",
       "Creates a new instance of the base class that every Python class "
       "ultimately inherits from — a plain, featureless object.",
       'o = object()\nisinstance(5, object)   # True — everything is an object'),
    _f("oct()",
       "Converts an integer to an octal string prefixed with '0o'.",
       "oct(8)    # '0o10'\noct(-56)  # '-0o70'"),
    _f("open()",
       "Opens a file and returns a file object you can read from or write "
       "to. Always prefer the 'with' statement so the file auto-closes.",
       'with open("data.txt", "r") as f:\n    content = f.read()\n\nwith open("out.txt", "w") as f:\n    f.write("hello")'),
    _f("ord()",
       "Returns the Unicode code point of a single-character string — the "
       "inverse of chr().",
       "ord('a')   # 97\nord('€')   # 8364",
       "Group Anagrams, Caesar Cipher — ord() enables letter-index arithmetic."),
    _f("pow()",
       "Returns base ** exp; with a third argument, computes "
       "(base ** exp) % mod far more efficiently than doing it in two steps.",
       'pow(2, 10)        # 1024\npow(2, 10, 1000)  # 24  — fast modular exponentiation',
       "Pow(x, n) — implement fast exponentiation, the same idea pow() uses."),
    _f("print()",
       "Writes values to standard output (or another stream), joined by sep "
       "and followed by end (defaults: a space and a newline).",
       'print("a", "b", sep="-")     # a-b\nprint("no newline", end="")\nprint("x", "y", file=None)   # stdout by default'),
    _f("property()",
       "Creates a managed attribute with getter/setter/deleter functions — "
       "most often used via the @property decorator for computed attributes.",
       'class Circle:\n    def __init__(self, r):\n        self._r = r\n\n    @property\n    def area(self):\n        return 3.14159 * self._r ** 2\n\nc = Circle(2)\nc.area   # 12.56636, computed on access'),
    _f("range()",
       "Creates an immutable, memory-efficient sequence of numbers — the "
       "classic way to control how many times a for loop runs.",
       'list(range(5))          # [0, 1, 2, 3, 4]\nlist(range(2, 10, 2))   # [2, 4, 6, 8]\nlist(range(10, 0, -1))  # countdown 10..1',
       "Used in nearly every array / DP problem to iterate over indices."),
    _f("repr()",
       "Returns an unambiguous, often eval()-able string representation of "
       "an object — geared toward developers, unlike str().",
       'repr("hi")     # "\'hi\'"\nrepr([1, 2])   # \'[1, 2]\''),
    _f("reversed()",
       "Returns a reverse iterator over a sequence, without creating a new "
       "reversed copy in memory the way slicing [::-1] does.",
       'list(reversed([1, 2, 3]))   # [3, 2, 1]\nfor ch in reversed("abc"):\n    print(ch)   # c, b, a',
       "Palindrome checks, Reverse Linked List — reversed() walks backward lazily."),
    _f("round()",
       "Rounds a number to a given precision (default 0 decimal places, "
       "returning an int). Ties round to the nearest even number ('banker's rounding').",
       'round(2.5)         # 2  — rounds to even, not always up!\nround(3.14159, 2)  # 3.14'),
    _f("set()",
       "Creates a mutable, unordered collection of unique, hashable "
       "elements — ideal for de-duplication and O(1) membership tests.",
       's = set([1, 2, 2, 3])   # {1, 2, 3}\ns.add(4)\n3 in s   # True — O(1) lookup',
       "Contains Duplicate, Intersection of Two Arrays — set() gives fast lookups."),
    _f("setattr()",
       "Sets a named attribute on an object to a value — equivalent to "
       "'obj.name = value', but the name can be computed at runtime.",
       'class P: pass\np = P()\nsetattr(p, "x", 10)   # same as: p.x = 10'),
    _f("slice()",
       "Creates a reusable slice object representing a range of indices, "
       "the same object Python builds internally for a[start:stop:step].",
       's = slice(1, 4)\n[0, 1, 2, 3, 4, 5][s]   # [1, 2, 3]'),
    _f("sorted()",
       "Returns a brand-new sorted list from any iterable, leaving the "
       "original untouched. key= and reverse= customise the ordering.",
       'sorted([3, 1, 2])                      # [1, 2, 3]\nsorted(["bb", "a", "ccc"], key=len)   # [\'a\', \'bb\', \'ccc\']\nsorted([3, 1, 2], reverse=True)       # [3, 2, 1]',
       "Merge Intervals, Meeting Rooms — sort first, then sweep through the data."),
    _f("staticmethod()",
       "A decorator that turns a method into a static method, which "
       "receives no implicit first argument (no self or cls) at all.",
       'class MathUtils:\n    @staticmethod\n    def add(a, b):\n        return a + b\n\nMathUtils.add(2, 3)   # 5'),
    _f("str()",
       "Returns a human-readable string version of an object by calling "
       "its __str__ method — the type used for basically all text in Python.",
       'str(42)        # \'42\'\nstr([1, 2])    # \'[1, 2]\'\nstr(3.14)      # \'3.14\''),
    _f("sum()",
       "Adds 'start' (default 0) plus every item of an iterable, from left "
       "to right, and returns the total. Items must be numeric.",
       'sum([1, 2, 3])        # 6\nsum([1, 2, 3], 10)    # 16 — custom starting value',
       "Subarray Sum Equals K, Running Sum of 1d Array — sum() drives prefix sums."),
    _f("super()",
       "Returns a proxy that delegates method calls to a parent (or "
       "sibling, in multiple inheritance) class — key to clean inheritance.",
       'class Animal:\n    def speak(self):\n        print("...")\n\nclass Dog(Animal):\n    def speak(self):\n        super().speak()\n        print("Woof")\n\nDog().speak()\n# ...\n# Woof'),
    _f("tuple()",
       "Builds a new immutable, ordered sequence from the items of an "
       "iterable — like a list that can never be changed after creation.",
       'tuple([1, 2, 3])   # (1, 2, 3)\ntuple("ab")        # (\'a\', \'b\')'),
    _f("type()",
       "With one argument, returns an object's type. With three arguments "
       "(name, bases, dict), dynamically creates a brand new class.",
       "type(5)                     # <class 'int'>\nX = type('X', (), {'a': 1})\nX().a                       # 1"),
    _f("vars()",
       "Returns the __dict__ of a module, class, or instance (its "
       "attribute storage). With no argument, behaves like locals().",
       'class P:\n    def __init__(self):\n        self.x = 1\n\nvars(P())   # {\'x\': 1}'),
    _f("zip()",
       "Iterates over several iterables in parallel, producing tuples that "
       "pair up corresponding items. Stops at the shortest iterable by default.",
       'list(zip([1, 2, 3], ["a", "b", "c"]))\n# [(1, \'a\'), (2, \'b\'), (3, \'c\')]\n\nx, y = [1, 2, 3], [4, 5, 6]\nlist(zip(x, y))            # pairs them up\nlist(zip(*zip(x, y)))      # unzips back to columns',
       "Pairing coordinates, or merging two lists index-by-index in matrix problems."),
    _f("__import__()",
       "The low-level function the 'import' statement actually calls "
       "under the hood. Prefer importlib.import_module() in everyday code.",
       'math = __import__("math")\nmath.sqrt(16)   # 4.0'),
]

ALL_DATA = CHEAT_DATA + BUILTIN_FUNCTIONS

CUSTOM_FILE = os.path.join(os.path.expanduser("~"), ".py_cheatsheet_custom.json")

CATEGORIES = sorted(set(d["category"] for d in ALL_DATA))

CAT_COLORS = {
    "Basics":             "#FFD580",
    "Data Types":         "#80CFFF",
    "Maths":              "#A8F0A8",
    "Errors":             "#FF9E9E",
    "Functions":          "#D4A8FF",
    "Conditionals":       "#FFB8A8",
    "Loops":              "#A8E8FF",
    "List Methods":       "#FFE4A8",
    "Built-in Functions": "#8CF0C8",
    "Modules":            "#F0C8FF",
    "Classes & Objects":  "#F0E8A0",
    "Custom":             "#B0F0E8",
}

# ══════════════════════════════════════════════════════════════════════════
# THEME
# ══════════════════════════════════════════════════════════════════════════
BG_APP    = "#14141f"
BG_PANEL  = "#1b1b2b"
BG_CARD   = "#1f1f33"
BG_CODE   = "#0c0c17"
BG_INPUT  = "#262640"
BORDER    = "#33334f"
TXT_MAIN  = "#eaeaf5"
TXT_DIM   = "#9797b8"
ACCENT    = "#80CFFF"
FONT_UI   = ("Segoe UI", 10)
FONT_UI_B = ("Segoe UI", 10, "bold")
FONT_CODE = ("Consolas", 10)
FONT_TITLE = ("Segoe UI", 12, "bold")


# ══════════════════════════════════════════════════════════════════════════
# APP
# ══════════════════════════════════════════════════════════════════════════
class PyCheatSheet:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Python Cheat Sheet")
        self.root.geometry("980x640+60+60")
        self.root.minsize(720, 460)
        self.root.configure(bg=BG_APP)
        self.pinned = False
        self.root.resizable(True, True)

        self.custom_entries = self._load_custom()
        self.all_data = ALL_DATA + self.custom_entries
        self.filtered = list(self.all_data)
        self.selected_key = None   # (category, name) of the shown entry

        self._build_style()
        self._build_ui()
        self._on_search()

    # ── Persistence ─────────────────────────────────────────────────────
    def _load_custom(self):
        try:
            with open(CUSTOM_FILE) as f:
                return json.load(f)
        except Exception:
            return []

    def _save_custom(self):
        with open(CUSTOM_FILE, "w") as f:
            json.dump(self.custom_entries, f, indent=2)

    # ── ttk styling ─────────────────────────────────────────────────────
    def _build_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TCombobox",
                         fieldbackground=BG_INPUT, background=BG_INPUT,
                         foreground=TXT_MAIN, arrowcolor=TXT_MAIN,
                         selectbackground=BG_INPUT, selectforeground=TXT_MAIN,
                         bordercolor=BORDER, lightcolor=BG_INPUT, darkcolor=BG_INPUT)
        style.map("TCombobox", fieldbackground=[("readonly", BG_INPUT)])

        style.configure("Treeview",
                         background=BG_PANEL, fieldbackground=BG_PANEL,
                         foreground=TXT_MAIN, rowheight=26, borderwidth=0,
                         font=FONT_UI)
        style.map("Treeview",
                   background=[("selected", "#33335a")],
                   foreground=[("selected", "#ffffff")])
        style.configure("Treeview.Heading",
                         background=BG_CARD, foreground=TXT_DIM,
                         font=FONT_UI_B, relief="flat")
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        style.configure("Vertical.TScrollbar", background=BG_CARD,
                         troughcolor=BG_APP, bordercolor=BG_APP,
                         arrowcolor=TXT_DIM)

    # ── UI construction ─────────────────────────────────────────────────
    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        self._build_titlebar()
        self._build_toolbar()
        self._build_body()
        self._build_statusbar()

    def _build_titlebar(self):
        bar = tk.Frame(self.root, bg="#0e0e18", height=40)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.columnconfigure(1, weight=1)

        tk.Label(bar, text="🐍", bg="#0e0e18", fg="#FFD580",
                 font=("Segoe UI", 15)).grid(row=0, column=0, padx=(14, 6))
        tk.Label(bar, text="Python Cheat Sheet", bg="#0e0e18", fg=TXT_MAIN,
                 font=FONT_TITLE).grid(row=0, column=1, sticky="w")

        self.pin_btn = tk.Button(bar, text="📍", bg="#0e0e18", fg=TXT_DIM,
                                  relief="flat", bd=0, cursor="hand2",
                                  activebackground="#0e0e18",
                                  command=self._toggle_pin, font=("Segoe UI", 12))
        self.pin_btn.grid(row=0, column=2, padx=4)

        tk.Button(bar, text="＋ Add", bg="#0e0e18", fg=ACCENT,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground="#0e0e18",
                  command=self._open_add_dialog,
                  font=FONT_UI_B).grid(row=0, column=3, padx=6)

        tk.Button(bar, text="✕", bg="#0e0e18", fg="#FF9E9E",
                  relief="flat", bd=0, cursor="hand2",
                  activebackground="#0e0e18",
                  command=self.root.destroy,
                  font=("Segoe UI", 12, "bold")).grid(row=0, column=4, padx=(6, 14))

        for w in (bar, *bar.winfo_children()):
            w.bind("<ButtonPress-1>", self._drag_start)
            w.bind("<B1-Motion>", self._drag_motion)

    def _build_toolbar(self):
        tb = tk.Frame(self.root, bg=BG_APP, pady=10)
        tb.grid(row=1, column=0, sticky="ew", padx=14)
        tb.columnconfigure(0, weight=1)

        # search box
        search_box = tk.Frame(tb, bg=BG_INPUT, highlightbackground=BORDER,
                               highlightthickness=1)
        search_box.grid(row=0, column=0, sticky="ew")
        search_box.columnconfigure(1, weight=1)

        tk.Label(search_box, text="🔍", bg=BG_INPUT, fg=TXT_DIM,
                 font=FONT_UI).grid(row=0, column=0, padx=(10, 4), pady=7)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        tk.Entry(search_box, textvariable=self.search_var, bg=BG_INPUT,
                 fg=TXT_MAIN, insertbackground=TXT_MAIN, relief="flat",
                 font=FONT_UI).grid(row=0, column=1, sticky="ew", pady=7)
        tk.Label(search_box, text="Search name, description, code…",
                 bg=BG_INPUT, fg=TXT_DIM, font=("Segoe UI", 8)
                 ).grid(row=0, column=2, padx=10)

        # category dropdown
        self.cat_var = tk.StringVar(value="All Categories")
        cats = ["All Categories"] + CATEGORIES
        self.cat_menu = ttk.Combobox(tb, textvariable=self.cat_var, values=cats,
                                      state="readonly", font=FONT_UI, width=22)
        self.cat_menu.grid(row=0, column=1, padx=(10, 0))
        self.cat_menu.bind("<<ComboboxSelected>>", self._on_search)

    def _build_body(self):
        body = tk.Frame(self.root, bg=BG_APP)
        body.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 8))
        body.columnconfigure(0, weight=0, minsize=300)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # ── Left: list panel ──
        left = tk.Frame(body, bg=BG_PANEL, highlightbackground=BORDER,
                         highlightthickness=1)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)

        cols = ("cat",)
        self.tree = ttk.Treeview(left, columns=cols, show="tree",
                                  selectmode="browse")
        self.tree.column("#0", width=280, stretch=True)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        vsb = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # ── Right: detail panel ──
        right = tk.Frame(body, bg=BG_CARD, highlightbackground=BORDER,
                          highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(5, weight=1)

        self.cat_badge = tk.Label(right, text="", bg=ACCENT, fg="#14141f",
                                   font=("Segoe UI", 8, "bold"), padx=8, pady=2)
        self.cat_badge.grid(row=0, column=0, sticky="w", padx=18, pady=(18, 6))

        self.name_lbl = tk.Label(right, text="", bg=BG_CARD, fg=ACCENT,
                                  font=("Segoe UI", 17, "bold"), anchor="w",
                                  justify="left", wraplength=560)
        self.name_lbl.grid(row=1, column=0, sticky="ew", padx=18)

        self.desc_lbl = tk.Label(right, text="", bg=BG_CARD, fg=TXT_MAIN,
                                  font=FONT_UI, anchor="w", justify="left",
                                  wraplength=560)
        self.desc_lbl.grid(row=2, column=0, sticky="ew", padx=18, pady=(8, 12))

        # syntax box
        code_outer = tk.Frame(right, bg=BG_CODE, highlightbackground=BORDER,
                               highlightthickness=1)
        code_outer.grid(row=3, column=0, sticky="ew", padx=18)
        code_outer.columnconfigure(0, weight=1)

        code_head = tk.Frame(code_outer, bg=BG_CODE)
        code_head.grid(row=0, column=0, sticky="ew", padx=10, pady=(6, 0))
        code_head.columnconfigure(0, weight=1)
        tk.Label(code_head, text="CODE", bg=BG_CODE, fg=TXT_DIM,
                 font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w")
        self.copy_btn = tk.Button(code_head, text="⎘ Copy", bg=BG_CODE,
                                   fg=ACCENT, relief="flat", bd=0,
                                   activebackground=BG_CODE,
                                   cursor="hand2", font=("Segoe UI", 8, "bold"),
                                   command=self._copy_syntax)
        self.copy_btn.grid(row=0, column=1, sticky="e")

        self.syntax_text = tk.Text(code_outer, bg=BG_CODE, fg="#B8E8FF",
                                    font=FONT_CODE, relief="flat", wrap="none",
                                    height=8, bd=10, insertbackground="#B8E8FF",
                                    selectbackground="#33335a", state="disabled")
        self.syntax_text.grid(row=1, column=0, sticky="ew")
        code_scroll = ttk.Scrollbar(code_outer, orient="horizontal",
                                     command=self.syntax_text.xview)
        code_scroll.grid(row=2, column=0, sticky="ew")
        self.syntax_text.configure(xscrollcommand=code_scroll.set)

        # leetcode note
        self.leet_frame = tk.Frame(right, bg=BG_CARD)
        self.leet_frame.grid(row=4, column=0, sticky="ew", padx=18, pady=(10, 0))
        self.leet_frame.columnconfigure(0, weight=1)
        tk.Label(self.leet_frame, text="🧩 WHERE YOU'D USE IT", bg=BG_CARD,
                 fg="#FFD580", font=("Segoe UI", 8, "bold")
                 ).grid(row=0, column=0, sticky="w")
        self.leet_lbl = tk.Label(self.leet_frame, text="", bg=BG_CARD,
                                  fg=TXT_DIM, font=("Segoe UI", 9),
                                  anchor="w", justify="left", wraplength=560)
        self.leet_lbl.grid(row=1, column=0, sticky="ew", pady=(2, 0))

        tk.Frame(right, bg=BG_CARD).grid(row=5, column=0, sticky="nsew")

    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg="#0e0e18", pady=6)
        bar.grid(row=3, column=0, sticky="ew")
        self.counter_lbl = tk.Label(bar, text="", bg="#0e0e18", fg=TXT_DIM,
                                     font=("Segoe UI", 9))
        self.counter_lbl.grid(row=0, column=0, padx=14)
        tk.Label(bar, text="↑↓ navigate   •   type to search   •   double-click to copy",
                 bg="#0e0e18", fg="#55557a", font=("Segoe UI", 8)
                 ).grid(row=0, column=1, sticky="e", padx=14)
        bar.columnconfigure(1, weight=1)

    # ── Drag / pin ──────────────────────────────────────────────────────
    def _drag_start(self, e):
        self._dx = e.x_root - self.root.winfo_x()
        self._dy = e.y_root - self.root.winfo_y()

    def _drag_motion(self, e):
        self.root.geometry(f"+{e.x_root - self._dx}+{e.y_root - self._dy}")

    def _toggle_pin(self):
        self.pinned = not self.pinned
        self.root.attributes("-topmost", self.pinned)
        self.pin_btn.config(fg="#FFD580" if self.pinned else TXT_DIM,
                             text="📌" if self.pinned else "📍")

    # ── Search / filter ─────────────────────────────────────────────────
    def _on_search(self, *_):
        q = self.search_var.get().lower().strip()
        cat = self.cat_var.get()

        self.all_data = ALL_DATA + self.custom_entries
        self.filtered = [
            d for d in self.all_data
            if (cat == "All Categories" or d["category"] == cat)
            and (not q or q in d["name"].lower()
                 or q in d["description"].lower()
                 or q in d["syntax"].lower()
                 or q in d.get("leetcode", "").lower())
        ]
        self._refresh_tree()

    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for i, entry in enumerate(self.filtered):
            iid = str(i)
            self.tree.insert("", "end", iid=iid,
                              text=f"  {entry['name']}   ·  {entry['category']}",
                              tags=(entry["category"],))
        self.counter_lbl.config(
            text=f"{len(self.filtered)} result{'s' if len(self.filtered) != 1 else ''}")

        if self.filtered:
            self.tree.selection_set("0")
            self.tree.focus("0")
            self._show_entry(self.filtered[0])
        else:
            self._show_empty()

    def _on_tree_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        if 0 <= idx < len(self.filtered):
            self._show_entry(self.filtered[idx])

    # ── Detail rendering ────────────────────────────────────────────────
    def _show_entry(self, e):
        cat = e["category"]
        color = CAT_COLORS.get(cat, "#888")
        self.cat_badge.config(text=cat, bg=color, fg="#14141f")
        self.name_lbl.config(text=e["name"])
        self.desc_lbl.config(text=e["description"])
        self._set_syntax(e["syntax"])

        leet = e.get("leetcode", "")
        if leet:
            self.leet_frame.grid()
            self.leet_lbl.config(text=leet)
        else:
            self.leet_frame.grid_remove()

    def _show_empty(self):
        self.cat_badge.config(text="")
        self.name_lbl.config(text="No results")
        self.desc_lbl.config(text="Try a different search term or category.")
        self._set_syntax("")
        self.leet_frame.grid_remove()

    def _set_syntax(self, text):
        self.syntax_text.config(state="normal")
        self.syntax_text.delete("1.0", "end")
        self.syntax_text.insert("1.0", text)
        self.syntax_text.config(state="disabled")

    # ── Copy ────────────────────────────────────────────────────────────
    def _copy_syntax(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        self.root.clipboard_clear()
        self.root.clipboard_append(self.filtered[idx]["syntax"])
        self.copy_btn.config(text="✔ Copied!", fg="#A8F0A8")
        self.root.after(1400, lambda: self.copy_btn.config(text="⎘ Copy", fg=ACCENT))

    # ── Add custom entry dialog ─────────────────────────────────────────
    def _open_add_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add Custom Entry")
        dlg.geometry("380x420")
        dlg.configure(bg=BG_APP)
        dlg.resizable(False, False)
        dlg.attributes("-topmost", True)
        dlg.transient(self.root)

        pad = {"padx": 16, "pady": (10, 3)}

        def label(txt):
            tk.Label(dlg, text=txt, bg=BG_APP, fg=TXT_MAIN, font=FONT_UI_B,
                      anchor="w").pack(fill="x", **pad)

        def entry_field():
            e = tk.Entry(dlg, bg=BG_INPUT, fg=TXT_MAIN,
                         insertbackground=TXT_MAIN, relief="flat",
                         font=FONT_UI, bd=6)
            e.pack(fill="x", padx=16)
            return e

        label("Name")
        name_e = entry_field()

        label("Description")
        desc_e = entry_field()

        label("Code / Syntax")
        syn_e = tk.Text(dlg, bg=BG_CODE, fg="#B8E8FF",
                         insertbackground="#B8E8FF", relief="flat",
                         font=FONT_CODE, height=6, bd=8, wrap="none")
        syn_e.pack(fill="x", padx=16)

        label("Leetcode / Use case (optional)")
        leet_e = entry_field()

        def save():
            n = name_e.get().strip()
            d = desc_e.get().strip()
            s = syn_e.get("1.0", "end").strip()
            l = leet_e.get().strip()
            if not n:
                messagebox.showerror("Error", "Name is required.", parent=dlg)
                return
            entry = {"category": "Custom", "name": n, "description": d,
                      "syntax": s, "leetcode": l}
            self.custom_entries.append(entry)
            self._save_custom()
            self.cat_var.set("Custom")
            self._on_search()
            dlg.destroy()

        btn_frame = tk.Frame(dlg, bg=BG_APP)
        btn_frame.pack(fill="x", padx=16, pady=14)
        tk.Button(btn_frame, text="Save", bg=BG_INPUT, fg="#A8F0A8",
                  relief="flat", font=FONT_UI_B, cursor="hand2",
                  command=save, padx=14, pady=4).pack(side="right", padx=4)
        tk.Button(btn_frame, text="Cancel", bg=BG_INPUT, fg="#FF9E9E",
                  relief="flat", font=FONT_UI, cursor="hand2",
                  command=dlg.destroy, padx=14, pady=4).pack(side="right")


# ══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = PyCheatSheet(root)

    def _nav(delta):
        sel = app.tree.selection()
        if not sel or not app.filtered:
            return
        idx = max(0, min(len(app.filtered) - 1, int(sel[0]) + delta))
        app.tree.selection_set(str(idx))
        app.tree.focus(str(idx))
        app.tree.see(str(idx))

    root.bind("<Down>", lambda e: _nav(1))
    root.bind("<Up>", lambda e: _nav(-1))

    root.mainloop()