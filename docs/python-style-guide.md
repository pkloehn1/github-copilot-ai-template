# Python Style Guide

This document is the single source of truth for Python code style.

## Table of Contents

- [Python Style Guide](#python-style-guide)
  - [Table of Contents](#table-of-contents)
  - [Source Documents](#source-documents)
  - [Source Contribution Map](#source-contribution-map)
  - [Enforcement](#enforcement)
    - [Linter Configuration](#linter-configuration)
  - [Hierarchy](#hierarchy)
  - [Scope](#scope)
  - [Introduction](#introduction)
    - [Consistency Principles](#consistency-principles)
    - [When to Deviate](#when-to-deviate)
  - [File Structure Order](#file-structure-order)
    - [Module-Level Ordering](#module-level-ordering)
    - [Class-Level Ordering](#class-level-ordering)
    - [.gitignore Patterns](#gitignore-patterns)
    - [requirements.txt](#requirementstxt)
  - [Code Layout](#code-layout)
    - [Indentation](#indentation)
    - [Line Length](#line-length)
    - [Blank Lines](#blank-lines)
    - [Imports](#imports)
    - [Source File Encoding](#source-file-encoding)
  - [Whitespace](#whitespace)
    - [Pet Peeves](#pet-peeves)
    - [Operators](#operators)
    - [Trailing Commas](#trailing-commas)
  - [Comments](#comments)
    - [Block Comments](#block-comments)
    - [Inline Comments](#inline-comments)
  - [Docstrings](#docstrings)
    - [One-Line Docstrings](#one-line-docstrings)
    - [Multi-Line Docstrings](#multi-line-docstrings)
    - [Module Docstrings](#module-docstrings)
    - [Class Docstrings](#class-docstrings)
    - [Function Docstrings](#function-docstrings)
  - [Naming Conventions](#naming-conventions)
    - [Package and Module Names](#package-and-module-names)
    - [Class Names](#class-names)
    - [Function and Variable Names](#function-and-variable-names)
    - [Constants](#constants)
    - [Type Variables](#type-variables)
    - [Exception Names](#exception-names)
  - [Programming Recommendations](#programming-recommendations)
    - [Comparisons](#comparisons)
    - [Boolean Comparisons](#boolean-comparisons)
    - [Exceptions](#exceptions)
    - [Context Managers](#context-managers)
    - [Return Statements](#return-statements)
    - [String Methods](#string-methods)
    - [Sequences](#sequences)
  - [Type Annotations](#type-annotations)
    - [Function Annotations](#function-annotations)
    - [Variable Annotations](#variable-annotations)
    - [Collection Types](#collection-types)
    - [Union Types](#union-types)
    - [Callable Types](#callable-types)
    - [Type Aliases](#type-aliases)
    - [Generics](#generics)
  - [Language Rules](#language-rules)
    - [Lint](#lint)
    - [Default Arguments](#default-arguments)
    - [Properties](#properties)
    - [True/False Evaluations](#truefalse-evaluations)
    - [Decorators](#decorators)
    - [Threading](#threading)
    - [Power Features](#power-features)
  - [Security](#security)
    - [Security Source Documents](#security-source-documents)
    - [Security Section Map](#security-section-map)
    - [Input Validation](#input-validation)
    - [Injection Prevention](#injection-prevention)
    - [Secrets Management](#secrets-management)
    - [Dependency Security](#dependency-security)
    - [Error Handling](#error-handling)
    - [Cryptography](#cryptography)
    - [Logging](#logging)

## Source Documents

This guide merges these authoritative sources:

| Document     | Updated    | License       | URL                                                |
| ------------ | ---------- | ------------- | -------------------------------------------------- |
| PEP 8        | 2025-04-04 | Public Domain | <https://peps.python.org/pep-0008/>                |
| PEP 257      | 2024-04-17 | Public Domain | <https://peps.python.org/pep-0257/>                |
| Google Style | 2024       | CC-BY 3.0     | <https://google.github.io/styleguide/pyguide.html> |

## Source Contribution Map

| Section              | PEP 8 | PEP 257 | Google |
| -------------------- | :---: | :-----: | :----: |
| Introduction         |   ✓   |         |        |
| File Structure Order |       |         |   ✓    |
| Code Layout          |   ✓   |         |   ✓    |
| Whitespace           |   ✓   |         |        |
| Comments             |   ✓   |         |        |
| Docstrings           |       |    ✓    |   ✓    |
| Naming Conventions   |   ✓   |         |   ✓    |
| Programming          |   ✓   |         |        |
| Type Annotations     |   ✓   |         |   ✓    |
| Language Rules       |       |         |   ✓    |

## Enforcement

This guide is enforced by:

- **ruff** — Linter and formatter (see `pyproject.toml`)
- **pre-commit** — Runs ruff on staged files
- **super-linter** — CI validation using ruff

### Linter Configuration

Enable these ruff rule sets to enforce this guide:

| Rule Set             | Code | Enforces Section               |
| -------------------- | ---- | ------------------------------ |
| Pyflakes             | F    | Programming Recommendations    |
| pycodestyle errors   | E    | Code Layout, Whitespace        |
| pycodestyle warnings | W    | Code Layout, Whitespace        |
| isort                | I    | File Structure Order (imports) |
| pep8-naming          | N    | Naming Conventions             |
| pydocstyle           | D    | Docstrings                     |
| pyupgrade            | UP   | Type Annotations               |
| flake8-bugbear       | B    | Programming Recommendations    |
| flake8-simplify      | SIM  | Programming Recommendations    |

**pyproject.toml configuration:**

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "D", "UP", "B", "SIM"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
docstring-code-format = true
```

**Disable rules only when:**

- The rule conflicts with this document
- A specific line requires deviation (use `# noqa: XXXX` with justification)
- The rule produces false positives in specific contexts

## Hierarchy

When sources conflict:

1. This document (project-specific decisions)
2. PEP 8 / PEP 257 (official Python standards)
3. Google Python Style Guide (extended coverage)

## Scope

- **Runtime:** Python 3.12+ LTS
- **Applies to:** All `.py` files in this repository

---

## Introduction

Code is read more often than it is written.
These guidelines improve readability and consistency across Python code.

### Consistency Principles

A style guide is about consistency. Apply these rules in order:

1. **Project consistency** — Follow this document
2. **Module consistency** — Match the existing file style
3. **Function consistency** — Match the surrounding code

### When to Deviate

**Deviation requires human approval.** AI tools may recommend deviations but
cannot decide to deviate on their own.

A human may approve deviation when:

- Applying the rule makes the code less readable
- Surrounding code breaks the rule (historical reasons)
- Code must remain compatible with older Python versions
- No clear way exists to follow the guideline

Do not break backwards compatibility just to comply with style rules.

---

## File Structure Order

Organize Python files in a consistent, predictable order.
This enables readers to find elements quickly.

### Module-Level Ordering

Place elements in this sequence:

| Order | Element                    | Example                          |
| ----: | -------------------------- | -------------------------------- |
|     1 | Module docstring           | `"""Module description."""`      |
|     2 | Future imports             | `from __future__ import ...`     |
|     3 | Module dunders             | `__all__`, `__version__`         |
|     4 | Standard library imports   | `import os`                      |
|     5 | Third-party imports        | `import requests`                |
|     6 | Local application imports  | `from myapp import utils`        |
|     7 | Constants                  | `MAX_RETRIES = 3`                |
|     8 | Type variables and aliases | `T = TypeVar("T")`               |
|     9 | Exception classes          | `class MyError(Exception): ...`  |
|    10 | Module-level functions     | `def helper(): ...`              |
|    11 | Classes                    | `class MyClass: ...`             |
|    12 | Main guard                 | `if __name__ == "__main__": ...` |

**Notes:**

- Separate import groups with a blank line
- Place helper functions before public API functions
- Place base classes before derived classes

### Class-Level Ordering

Place elements within a class in this sequence:

| Order | Element                 | Example                             |
| ----: | ----------------------- | ----------------------------------- |
|     1 | Class docstring         | `"""Class description."""`          |
|     2 | Class constants         | `DEFAULT_SIZE = 100`                |
|     3 | Class variables         | `instances: list = []`              |
|     4 | `__init__`              | `def __init__(self): ...`           |
|     5 | `__post_init__`         | For dataclasses                     |
|     6 | Other dunder methods    | `__str__`, `__repr__`, `__eq__`     |
|     7 | `@classmethod` methods  | `@classmethod def create(): ...`    |
|     8 | `@staticmethod` methods | `@staticmethod def validate(): ...` |
|     9 | `@property` methods     | `@property def name(): ...`         |
|    10 | Public instance methods | `def process(self): ...`            |
|    11 | Private methods         | `def _helper(self): ...`            |

**Notes:**

- Group related methods together within their category
- Place abstract methods before concrete implementations

### .gitignore Patterns

Include these patterns in `.gitignore` for Python projects:

```gitignore
# Byte-compiled files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/
*.egg

# Virtual environments
.venv/
venv/
ENV/

# IDE and editor files
.idea/
.vscode/
*.swp
*.swo

# Testing and coverage
.pytest_cache/
.coverage
htmlcov/
.tox/

# Type checking
.mypy_cache/
.pytype/

# Jupyter notebooks
.ipynb_checkpoints/
```

### requirements.txt

Pin dependencies to specific versions for reproducibility:

```text
requests==2.31.0
numpy==1.26.0
pandas==2.1.0
```

**Rules:**

- Pin major and minor versions at minimum: `package>=1.2,<2.0`
- Use exact pins for production: `package==1.2.3`
- Separate dev dependencies into `requirements-dev.txt`
- Generate from a locked environment: `pip freeze > requirements.txt`

**Prefer pyproject.toml** for modern projects. Use requirements.txt only when:

- Legacy tooling requires it
- Deployment systems expect it
- Simple scripts without package structure

---

## Code Layout

### Indentation

Use 4 spaces per indentation level. Never use tabs.

For continuation lines, align wrapped elements vertically or use hanging indent:

```python
# Aligned with opening delimiter
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Hanging indent with 4 spaces
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)

# Distinguish arguments from body
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```

### Line Length

Limit all lines to 100 characters maximum.

Limit docstrings and comments to 80 characters.

Use Python's implicit line joining inside parentheses, brackets, and braces.
Prefer this over backslash continuation:

```python
# Preferred: implicit continuation
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction)

# Acceptable: backslash for with statements
with open('/path/to/file') as file_1, \
     open('/path/to/other') as file_2:
    file_2.write(file_1.read())
```

### Blank Lines

Use blank lines as follows:

| Context                        | Blank Lines |
| ------------------------------ | :---------: |
| Top-level function/class       |      2      |
| Method definitions in a class  |      1      |
| Logical sections in a function |      1      |
| After class docstring          |      1      |

### Imports

Place imports at the top of the file, after module docstring and dunders.

Group imports in this order, separated by blank lines:

1. Standard library imports
2. Third-party imports
3. Local application imports

```python
"""Module docstring."""

__all__ = ["MyClass"]

import os
import sys

import requests
import numpy as np

from myapp import utils
from myapp.models import User
```

**Rules:**

- One import per line: `import os` and `import sys` on separate lines
- Absolute imports are preferred over relative imports
- Avoid wildcard imports (`from module import *`)
- Use `from module import Class` when importing classes

### Source File Encoding

Use UTF-8 encoding. Do not include an encoding declaration.

Use ASCII-only identifiers. Use English words for names.

---

## Whitespace

### Pet Peeves

Avoid extraneous whitespace in these situations:

```python
spam(ham[1], {eggs: 2})
foo = (0,)
if x == 4: print(x, y); x, y = y, x
dct['key'] = lst[index]
```

For slices, treat the colon as a binary operator with equal spacing:

```python
ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3]
ham[lower:upper], ham[lower + offset : upper + offset]
```

### Operators

Surround binary operators with a single space:

```python
i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)
```

Do not use spaces around `=` for keyword arguments or defaults:

```python
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
```

When combining annotations with defaults, use spaces around `=`:

```python
def munge(sep: AnyStr = None): ...
```

### Trailing Commas

Use trailing commas when a list will be extended over time:

```python
# Trailing comma for future extension
FILES = [
    'setup.cfg',
    'tox.ini',
]

# Single-element tuple requires trailing comma
FILES = ('setup.cfg',)
```

---

## Comments

Comments that contradict the code are worse than no comments.
Keep comments current when the code changes.

Write comments as complete sentences with proper capitalization.
Use English for comments in projects with a global audience.

### Block Comments

Block comments apply to the code that follows them.
Indent them to the same level as that code.

Start each line with `#` and a single space:

```python
# This is a block comment that explains
# the complex logic in the following code.
#
# A blank comment line separates paragraphs.
def complex_function():
    pass
```

### Inline Comments

Use inline comments sparingly. Separate them by at least two spaces.

Do not state the obvious. Inline comments should add context, not repeat code:

```python
x = x + 1  # Compensate for border offset
```

---

## Docstrings

Write docstrings for all public modules, functions, classes, and methods.
Use triple double quotes (`"""`). Follow Google docstring convention.

### One-Line Docstrings

Use for simple functions where the description fits on one line:

```python
def load_config():
    """Load configuration from the default path."""
    return Config.from_file(DEFAULT_PATH)
```

The closing quotes are on the same line. No blank line after.

### Multi-Line Docstrings

Use when more detail is needed:

```python
def connect(host, port, timeout=30):
    """Establish a connection to the remote server.

    Opens a TCP connection and performs the initial handshake.
    Retries up to three times on transient failures.

    Args:
        host: The server hostname or IP address.
        port: The port number to connect to.
        timeout: Connection timeout in seconds.

    Returns:
        A Connection object representing the established connection.

    Raises:
        ConnectionError: If the connection cannot be established.
        TimeoutError: If the connection times out.
    """
```

Place a blank line after the summary. Closing quotes on their own line.

### Module Docstrings

Place at the top of the file, before imports:

```python
"""HTTP client utilities for the application.

This module provides high-level HTTP client functions with
automatic retry, connection pooling, and error handling.

Typical usage:
    from myapp import http
    response = http.get("https://api.example.com/data")
"""

import requests
```

### Class Docstrings

Describe the class purpose and list public attributes:

```python
class User:
    """A registered user in the system.

    Represents a user account with authentication credentials
    and profile information.

    Attributes:
        id: Unique identifier for the user.
        email: The user's email address.
        created_at: Timestamp when the account was created.
    """

    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email
        self.created_at = datetime.now()
```

### Function Docstrings

Document arguments, return values, and exceptions:

```python
def calculate_discount(price, percentage, minimum=0.0):
    """Calculate the discounted price.

    Args:
        price: Original price in dollars.
        percentage: Discount percentage (0-100).
        minimum: Minimum discount amount to apply.

    Returns:
        The final price after applying the discount.

    Raises:
        ValueError: If percentage is not between 0 and 100.
    """
```

**Docstring sections in order:**

1. Summary line
2. Extended description (optional)
3. Args
4. Returns (or Yields for generators)
5. Raises

---

## Naming Conventions

Names should be descriptive and reveal intent.
Avoid abbreviations except for well-known acronyms (HTTP, URL, ID).

### Package and Module Names

Use short, lowercase names. Underscores are permitted but discouraged:

```python
# Modules
utils.py
http_client.py
database.py

# Packages
mypackage/
    __init__.py
    core.py
```

### Class Names

Use CapWords (PascalCase):

```python
class HttpClient:
    pass

class UserAccount:
    pass

class XMLParser:
    pass
```

### Function and Variable Names

Use lowercase with underscores (snake_case):

```python
def calculate_total(items):
    item_count = len(items)
    total_price = sum(item.price for item in items)
    return total_price

user_name = "alice"
connection_timeout = 30
```

### Constants

Use uppercase with underscores:

```python
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
```

Define constants at module level, after imports.

### Type Variables

Use CapWords, typically short names:

```python
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# Descriptive names for constrained type variables
AnyStr = TypeVar("AnyStr", str, bytes)
Number = TypeVar("Number", int, float, complex)
```

### Exception Names

Use CapWords with `Error` suffix for exceptions:

```python
class ValidationError(Exception):
    pass

class ConnectionTimeoutError(Exception):
    pass

class AuthenticationError(Exception):
    pass
```

**Naming summary:**

| Element   | Convention       | Example           |
| --------- | ---------------- | ----------------- |
| Package   | lowercase        | `mypackage`       |
| Module    | snake_case       | `http_client.py`  |
| Class     | CapWords         | `HttpClient`      |
| Exception | CapWords + Error | `ValidationError` |
| Function  | snake_case       | `calculate_total` |
| Variable  | snake_case       | `user_name`       |
| Constant  | UPPER_SNAKE      | `MAX_CONNECTIONS` |
| TypeVar   | CapWords         | `T`, `AnyStr`     |

---

## Programming Recommendations

### Comparisons

Use `is` and `is not` for singletons like `None`:

```python
if value is None:
    return default

if result is not None:
    process(result)
```

Use `isinstance()` for type checking:

```python
if isinstance(obj, str):
    obj = obj.encode("utf-8")

if isinstance(items, (list, tuple)):
    items = list(items)
```

### Boolean Comparisons

Use implicit boolean evaluation:

```python
if items:
    process(items)

if not name:
    raise ValueError("Name required")
```

For explicit length checks, use comparison:

```python
if len(items) > 10:
    paginate(items)
```

### Exceptions

Catch specific exceptions, not bare `except`:

```python
try:
    value = mapping[key]
except KeyError:
    value = default_value
```

Use exception chaining with `from`:

```python
try:
    result = external_api.fetch(id)
except ApiError as e:
    raise DataError(f"Failed to fetch {id}") from e
```

Use `raise` without arguments to re-raise:

```python
try:
    process(data)
except ValidationError:
    log.error("Validation failed")
    raise
```

### Context Managers

Use `with` for resource management:

```python
with open("data.json") as f:
    data = json.load(f)

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Return Statements

Be consistent with return statements. If any return has a value, all should:

```python
def find_user(user_id):
    user = database.get(user_id)
    if user is None:
        return None
    return user
```

Use early returns to reduce nesting:

```python
def process_order(order):
    if not order.is_valid():
        return OrderResult.invalid()

    if order.is_duplicate():
        return OrderResult.duplicate()

    return order.execute()
```

### String Methods

Use string methods instead of the `string` module:

```python
text = "  hello world  "
clean = text.strip().lower()

if filename.endswith(".py"):
    process_python_file(filename)
```

### Sequences

Use list comprehensions for simple transformations:

```python
squares = [x * x for x in range(10)]
names = [user.name for user in users if user.active]
```

Use generator expressions for large sequences:

```python
total = sum(order.amount for order in orders)
```

---

## Type Annotations

Use type annotations for all public APIs. They improve readability and
enable static analysis tools.

### Function Annotations

Annotate all function parameters and return types:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def calculate_total(items: list[Item], tax_rate: float = 0.0) -> float:
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

Use `None` return type explicitly:

```python
def log_message(message: str) -> None:
    logger.info(message)
```

For functions that never return, use `NoReturn`:

```python
from typing import NoReturn

def fatal_error(message: str) -> NoReturn:
    logger.critical(message)
    sys.exit(1)
```

### Variable Annotations

Annotate variables when the type is not obvious:

```python
# Type is clear from assignment
name = "Alice"
count = 0

# Type annotation adds clarity
items: list[str] = []
mapping: dict[str, int] = {}
result: User | None = None
```

### Collection Types

Use built-in generic syntax (Python 3.9+):

```python
names: list[str] = []
scores: dict[str, int] = {}
coordinates: tuple[float, float] = (0.0, 0.0)
unique_ids: set[int] = set()
```

### Union Types

Use the `|` operator (Python 3.10+):

```python
def parse(value: str | bytes) -> dict:
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    return json.loads(value)

def find_user(user_id: int) -> User | None:
    return database.users.get(user_id)
```

### Callable Types

Use `Callable` for function parameters:

```python
from collections.abc import Callable

def retry(
    operation: Callable[[], T],
    max_attempts: int = 3,
) -> T:
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception:
            if attempt == max_attempts - 1:
                raise
```

### Type Aliases

Create aliases for complex types:

```python
type UserId = int
type Headers = dict[str, str]
type Handler = Callable[[Request], Response]

def fetch(url: str, headers: Headers) -> bytes:
    ...
```

### Generics

Use `TypeVar` for generic functions:

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

Use generic classes for containers:

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()
```

---

## Language Rules

### Lint

Run ruff on all code. Address all findings before committing.

Suppress warnings only when necessary, with justification:

```python
# noqa: E501 - URL cannot be split across lines
API_ENDPOINT = "https://api.example.com/v2/resources/items"
```

### Default Arguments

Never use mutable default arguments:

```python
def append_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

Immutable defaults are safe:

```python
def connect(host: str, port: int = 8080, timeout: float = 30.0) -> Connection:
    return Connection(host, port, timeout)
```

### Properties

Use properties for simple attribute access that requires logic:

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius must be non-negative")
        self._radius = value

    @property
    def area(self) -> float:
        return 3.14159 * self._radius ** 2
```

Properties should be cheap to compute. Use methods for expensive operations.

### True/False Evaluations

Use implicit boolean evaluation for sequences and mappings:

```python
if users:
    notify(users)

if not errors:
    return success()
```

Use explicit comparison for numeric zero checks when zero is a valid value:

```python
if count == 0:
    initialize()
```

### Decorators

Use decorators for cross-cutting concerns:

```python
import functools
import time

def timing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

@timing
def process_batch(items: list[Item]) -> None:
    for item in items:
        item.process()
```

Always use `@functools.wraps` to preserve function metadata.

### Threading

Use `threading.Lock` for shared mutable state:

```python
import threading

class Counter:
    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value
```

Prefer `queue.Queue` for thread communication over shared variables.

### Power Features

Avoid these features unless necessary:

| Feature                  | Guidance                                   |
| ------------------------ | ------------------------------------------ |
| Metaclasses              | Use only for frameworks and ORMs           |
| Dynamic attribute access | Prefer explicit attributes                 |
| `exec` and `eval`        | Security risk; avoid entirely              |
| `__del__`                | Unpredictable timing; use context managers |
| Multiple inheritance     | Use composition or mixins instead          |

When power features are required, document the rationale clearly.

---

## Security

Write secure code by default. These guidelines address common vulnerabilities
in Python applications.

### Security Source Documents

| Source               | Version | URL                                                        |
| -------------------- | ------- | ---------------------------------------------------------- |
| CWE Top 25           | 2024    | <https://cwe.mitre.org/top25/>                             |
| OWASP Top 10         | 2021    | <https://owasp.org/www-project-top-ten/>                   |
| OpenSSF Python Guide | 2024    | <https://best.openssf.org/Secure-Coding-Guide-for-Python/> |

### Security Section Map

| Section              | CWE                     | OWASP    | OpenSSF |
| -------------------- | ----------------------- | -------- | ------- |
| Input Validation     | CWE-20 (#12)            | A03:2021 | ✓       |
| Injection Prevention | CWE-78, CWE-89 (#3, #7) | A03:2021 | ✓       |
| Secrets Management   | CWE-798 (#22)           | A07:2021 | ✓       |
| Dependency Security  | —                       | A06:2021 | ✓       |
| Error Handling       | CWE-200 (#17)           | A09:2021 | ✓       |
| Cryptography         | —                       | A02:2021 | ✓       |
| Logging              | CWE-117, CWE-532        | A09:2021 | ✓       |

### Input Validation

Validate all external input before use:

```python
def process_age(value: str) -> int:
    try:
        age = int(value)
    except ValueError:
        raise ValidationError("Age must be an integer")

    if not 0 <= age <= 150:
        raise ValidationError("Age must be between 0 and 150")

    return age
```

Use allowlists over denylists:

```python
ALLOWED_EXTENSIONS = {".png", ".jpg", ".gif"}

def validate_filename(filename: str) -> bool:
    ext = pathlib.Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS
```

### Injection Prevention

Use parameterized queries for SQL:

```python
cursor.execute(
    "SELECT * FROM users WHERE id = ?",
    (user_id,),
)
```

Avoid shell commands. When necessary, use list arguments:

```python
import subprocess

subprocess.run(
    ["ls", "-la", directory],
    capture_output=True,
    check=True,
)
```

Never use `eval()` or `exec()` with untrusted input.

### Secrets Management

Never hardcode credentials:

```python
import os

DATABASE_URL = os.environ["DATABASE_URL"]
API_KEY = os.environ["API_KEY"]
```

For automation and CI, inject secrets via environment variables from your
secrets management service (1Password, HashiCorp Vault, Doppler, etc.):

```shell
# 1Password CLI example
op run --env-file=.env -- python script.py

# HashiCorp Vault example
vault kv get -field=password secret/database
```

### Dependency Security

Pin dependencies to specific versions:

```toml
[project]
dependencies = [
    "requests==2.31.0",
    "cryptography==41.0.0",
]
```

Audit dependencies regularly:

```shell
pip-audit
safety check
```

Monitor for CVEs in CI pipelines.

### Error Handling

Never expose internal details in error messages:

```python
def authenticate(username: str, password: str) -> User:
    user = database.get_user(username)
    if user is None or not user.verify_password(password):
        raise AuthenticationError("Invalid credentials")
    return user
```

Log details internally, return generic messages externally:

```python
try:
    result = process_payment(order)
except PaymentError as e:
    logger.error("Payment failed: %s", e, exc_info=True)
    raise UserError("Payment could not be processed")
```

### Cryptography

Use standard libraries. Never implement custom cryptography:

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

encrypted = cipher.encrypt(b"secret data")
decrypted = cipher.decrypt(encrypted)
```

Use secure password hashing:

```python
import hashlib
import secrets

def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = secrets.token_bytes(32)
    key = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=2**14,
        r=8,
        p=1,
    )
    return salt, key
```

### Logging

Never log sensitive data:

```python
logger.info("User %s authenticated", user.id)
```

Sanitize log output to prevent injection:

```python
import re

def sanitize_log(value: str) -> str:
    return re.sub(r"[\n\r]", "", value)

logger.info("Processing request: %s", sanitize_log(user_input))
```

Exclude from logs:

- Passwords and API keys
- Personal identifiable information (PII)
- Session tokens and credentials
- Credit card numbers
- Health records
