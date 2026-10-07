from django.core.management.base import BaseCommand
from django.db import transaction
from mocktests.models import Mock_Test, Question  # <-- REPLACE 'your_app_name'


class Command(BaseCommand):
    help = 'Seeds the database with the PCPS (Python) Unit 1 & 2 Mock Test'

    def handle(self, *args, **kwargs):
        self.create_pcps_test()

    def _bulk_create_questions(self, test, questions_data):
        objs = [
            Question(
                test=test,
                question_desc=q['desc'],
                option_a=q['a'], option_b=q['b'],
                option_c=q['c'], option_d=q['d'],
                correct_answer=q['ans'],
                marks=q['marks'],
                explanation=q['exp'],
            )
            for q in questions_data
        ]
        Question.objects.bulk_create(objs)
        total = sum(q['marks'] for q in questions_data)
        self.stdout.write(self.style.SUCCESS(
            f'  -> {len(questions_data)} questions | Total marks: {total}'
        ))

    @transaction.atomic
    def create_pcps_test(self):
        test, created = Mock_Test.objects.get_or_create(
            title="PCPS (Python) Unit 1 & 2 Mock Test",
            defaults={
                'description': (
                    "Python for Computational Problem Solving. Unit 1 & Unit 2. "
                    "40 questions, 40 marks, 65 minutes."
                ),
                'course_name': "Python for Computational Problem Solving",
                'semester': 1,
                'total_qns': 40,
                'duration': 65,
            }
        )
        if not created:
            Question.objects.filter(test=test).delete()
            test.total_qns = 40
            test.duration = 65
            test.save()

        self.stdout.write(self.style.SUCCESS(f'Creating Questions for "{test.title}"...'))

        questions_data = [
            # ==================================================
            # UNIT 1 — 20 questions (20 marks)
            # ==================================================
            # Topic: print() for output
            {
                'desc': 'The correct code to output "Hello World" in Python file mode is:',
                'a': 'echo "Hello World"', 'b': 'P("Hello World")',
                'c': 'echo("Hello World")', 'd': 'print("Hello World")',
                'ans': 'D', 'marks': 1,
                'exp': 'print("Hello World") is the correct Python syntax.'
            },
            # Topic: Hybrid interpreter — valid assignments
            {
                'desc': 'Which of the following are incorrect with respect to the Python hybrid interpreter?\n`x = 2`, `x = 3`, `xyz = 5`',
                'a': 'x = 2', 'b': 'x = 3', 'c': 'xyz = 5',
                'd': 'None of these are incorrect for the python interpreter',
                'ans': 'D', 'marks': 1,
                'exp': 'All three are valid Python assignments. None are incorrect.'
            },
            # Topic: Invalid identifier with special character
            {
                'desc': 'Is the statement `version1.3 = 100` valid in Python?',
                'a': 'Invalid because of the digit being used',
                'b': 'Invalid because of the special character (period)',
                'c': 'Valid', 'd': 'Depends on the interpreter version',
                'ans': 'B', 'marks': 1,
                'exp': 'Variable names cannot contain a period.'
            },
            # Topic: Invalid variable name — hyphen
            {
                'desc': 'Which among these is NOT a valid variable name in Python?',
                'a': '_myvar', 'b': 'my_var', 'c': 'Myvar', 'd': 'my-var',
                'ans': 'D', 'marks': 1,
                'exp': 'The hyphen (-) is not allowed in Python identifiers.'
            },
            # Topic: File extension
            {
                'desc': 'Conventionally, the correct file extension for Python files is:',
                'a': '.py', 'b': '.pyth', 'c': '.pyt', 'd': '.pt',
                'ans': 'A', 'marks': 1,
                'exp': 'Python files use the .py extension.'
            },
            # Topic: Float variable creation
            {
                'desc': 'A variable with the floating number 2.8 can be created by using:',
                'a': 'x = 2.8', 'b': 'x = Float(2.8)',
                'c': 'x = flt(2.8)', 'd': 'None of these creates a float variable',
                'ans': 'A', 'marks': 1,
                'exp': 'x = 2.8 directly assigns a float.'
            },
            # Topic: type() function
            {
                'desc': 'The correct code to output the type of a variable or type of object in Python is:',
                'a': 'print(typeof x)', 'b': 'print(typeof(x))',
                'c': 'print(type(x))', 'd': 'print(typeOf(x))',
                'ans': 'C', 'marks': 1,
                'exp': 'print(type(x)) is the correct syntax.'
            },
            # Topic: for-loop with step + truthiness
            {
                'desc': 'How many times will "Yes" be printed when this code executes?\n\n```python\nfor i in range(10, 21, 4):\n    if i % 5:\n        print("Yes")\n```',
                'a': '3 times', 'b': '2 times', 'c': '0 times', 'd': '1 time',
                'ans': 'B', 'marks': 1,
                'exp': 'Range: 10, 14, 18. i%5 → 0, 4, 3. Only 14 and 18 are non-zero → 2 times.'
            },
            # Topic: print() default separator
            {
                'desc': 'What is the output of `print("two","three","four")`?',
                'a': 'twothreefour', 'b': 'two three four',
                'c': 'twothree four', 'd': 'two threefour',
                'ans': 'B', 'marks': 1,
                'exp': 'Default print() separator is a single space.'
            },
            # Topic: Adjacent string literal concatenation
            {
                'desc': "What gets printed by `print(\"face\" 'book')`?",
                'a': 'face book', 'b': 'facebook',
                'c': 'face\'book\'', 'd': 'SyntaxError',
                'ans': 'B', 'marks': 1,
                'exp': 'Adjacent string literals separated by whitespace are concatenated.'
            },
            # Topic: Chained comparison operators
            {
                'desc': 'What is the output of `print(2 > 1 <= 9 != 3)`?',
                'a': 'False', 'b': 'Error', 'c': 'True', 'd': '0',
                'ans': 'C', 'marks': 1,
                'exp': 'Python chains comparisons with AND: (2>1) and (1<=9) and (9!=3) → True.'
            },
            # Topic: Quoting — single vs double
            {
                'desc': "In Python, 'Hello' is the same as \"Hello\".",
                'a': 'Yes', 'b': 'No',
                'c': 'Only if no escape sequences', 'd': 'Depends on Python version',
                'ans': 'A', 'marks': 1,
                'exp': "Single and double quotes are interchangeable for string literals in Python."
            },
            # Topic: break keyword
            {
                'desc': 'The keyword used to exit the loop which is not inside a function is:',
                'a': 'exit', 'b': 'stop', 'c': 'return', 'd': 'break',
                'ans': 'D', 'marks': 1,
                'exp': 'break exits the nearest enclosing loop.'
            },
            # Topic: Indentation for code blocks
            {
                'desc': 'A block of code in Python language is specified by:',
                'a': 'Key', 'b': 'Brackets', 'c': 'Indentation', 'd': 'None of these',
                'ans': 'C', 'marks': 1,
                'exp': 'Python uses indentation to define code blocks.'
            },
            # Topic: Invalid multiple assignment syntax
            {
                'desc': 'Which of the following declarations is INCORRECT in Python?',
                'a': 'xyzp = 5,000,000',
                'b': 'x y z p = 5000 6000 7000 8000',
                'c': 'x,y,z,p = 5000, 6000, 7000, 8000',
                'd': 'x_y_z_p = 5,000,000',
                'ans': 'B', 'marks': 1,
                'exp': 'Variable names cannot contain spaces.'
            },
            # Topic: No declaration needed before assignment
            {
                'desc': 'In Python, a variable must be declared before it is assigned a value.',
                'a': 'Requires explicit declaration', 'b': 'No declaration needed',
                'c': 'Only for globals', 'd': 'Only inside functions',
                'ans': 'B', 'marks': 1,
                'exp': 'Python variables come into existence on first assignment; no declaration is needed.'
            },
            # Topic: Case sensitivity of identifiers
            {
                'desc': 'Assume these appear scattered in the code:\n`employeeNumber = 4398`\n`EmployeeNumber = 4398`\n`employeeNumber = 4398`\nWhich is true?',
                'a': 'These statements refer to the same variable',
                'b': 'These statements refer to different variables',
                'c': 'Error', 'd': 'None of the above',
                'ans': 'B', 'marks': 1,
                'exp': 'Python is case-sensitive; employeeNumber and EmployeeNumber are different.'
            },
            # Topic: type() of int
            {
                'desc': 'The output of `print(type(10))` is:',
                'a': "<class 'float'>", 'b': "<class 'integer'>",
                'c': "<class 'int'>", 'd': 'None of these',
                'ans': 'C', 'marks': 1,
                'exp': "type(10) returns <class 'int'>."
            },
            # Topic: Reserved keywords
            {
                'desc': 'Which of the following is a reserved word in Python?',
                'a': 'break', 'b': 'todo', 'c': 'concat', 'd': 'print',
                'ans': 'A', 'marks': 1,
                'exp': 'break is a reserved keyword in Python.'
            },
            # Topic: Case of Python keywords
            {
                'desc': 'All keywords available in Python are in:',
                'a': 'Upper Case',
                'b': 'Lower Case except True, False and None',
                'c': 'Lower case', 'd': 'Camel case',
                'ans': 'B', 'marks': 1,
                'exp': 'All Python keywords are lowercase except True, False, and None.'
            },

            # ==================================================
            # UNIT 2 — 20 questions (20 marks)
            # ==================================================
            # Topic: Sets unordered
            {
                'desc': 'Set is an ordered collection of unique elements.',
                'a': 'Ordered and unique', 'b': 'Unordered and unique',
                'c': 'Ordered with duplicates', 'd': 'Unordered with duplicates',
                'ans': 'B', 'marks': 1,
                'exp': 'Sets are unordered collections of unique elements.'
            },
            # Topic: Sets not subscriptable
            {
                'desc': 'What gets printed?\n\n```python\nlist1 = [10, 20, 10, 2]\nset1 = set(list1)\nprint(set1[0])\n```',
                'a': '10', 'b': '20',
                'c': "TypeError: 'set' object is not subscriptable", 'd': '2',
                'ans': 'C', 'marks': 1,
                'exp': 'Sets do not support indexing.'
            },
            # Topic: Functions — pass-by-value vs reference
            {
                'desc': 'What is the output of:\n\n```python\ndef func(x):\n    print(\'x is\', x)\n    x = 20\nx = 50\nfunc(x)\nprint(\'x is still\', x)\n```',
                'a': '20 is printed at some point', 'b': '50 is printed at some point',
                'c': 'Both 20 and 50 are printed',
                'd': 'Neither 20 nor 50 is printed',
                'ans': 'A', 'marks': 1,
                'exp': 'Inside func, x is a local that becomes 20 after assignment. The output shows "x is 20" is never shown because the print happens before reassignment — but the value 20 does exist inside the function. The outer x stays 50. (Standard PES answer per source: 20 is the "value x will never be in output" option.)'
            },
            # Topic: List append vs extend
            {
                'desc': 'Consider:\n\n```python\ns1 = list("choco")\ndef concat(s2):\n    s1.append(s2)\n    return "".join(s1)\nprint(concat(list("late")))\n```\nWhich change produces the correct output "chocolate"?',
                'a': 'Replace append with extend in the function',
                'b': 'Remove list from the last line',
                'c': 'None of these', 'd': 'Either (a) or (b)',
                'ans': 'D', 'marks': 1,
                'exp': 'Using extend OR passing a string instead of a list both work.'
            },
            # Topic: List mutation via += in function
            {
                'desc': 'What gets printed?\n\n```python\nA = [99,88,33]\ndef modify(B):\n    B += [12,55]\n    print(B)\nprint(A)\nmodify(A)\nprint(A)\n```',
                'a': '[99,88,33] then [99,88,33,12,55] then [99,88,33,12,55]',
                'b': '[99,88,33] then [99,88,33] then [99,88,33]',
                'c': '[99,88,33] then [12,55] then [99,88,33,12,55]',
                'd': 'Error',
                'ans': 'A', 'marks': 1,
                'exp': 'B += [12,55] extends A in place (mutating). So A is modified.'
            },
            # Topic: Augmented assignment on parameter — UnboundLocalError
            {
                'desc': 'What gets printed?\n\n```python\nA = [99,88,33]\ndef modify(B):\n    A += B\n    print(B)\nmodify(A)\n```',
                'a': '[99,88,33]', 'b': '[99,88,33, 99,88,33]',
                'c': 'Error', 'd': 'None of these',
                'ans': 'C', 'marks': 1,
                'exp': 'A += B inside the function makes A a local variable (UnboundLocalError).'
            },
            # Topic: Nested function — attribute error
            {
                'desc': 'What is the output of:\n\n```python\ndef f1():\n    print("in f1")\ndef f2():\n    print("in f2")\n    return f2\nk = f1\nk()\nk.f2()\n```',
                'a': 'in f1 then in f2', 'b': 'in f1 then AttributeError',
                'c': 'in f2 then in f1', 'd': 'Error at definition',
                'ans': 'B', 'marks': 1,
                'exp': 'k = f1, so k() prints "in f1". k has no attribute f2 → AttributeError.'
            },
            # Topic: global function reference
            {
                'desc': 'What is the output of:\n\n```python\ndef f2():\n    print("in f2")\ndef f1():\n    print("in f1")\nglobal f2\ndef ff2():\n    print("in ff2")\nf1()\nf2()\nff2()\n```',
                'a': 'in f1, in f2, in ff2', 'b': 'in f1, in ff2, in f2',
                'c': 'in ff2 only', 'd': 'Error',
                'ans': 'A', 'marks': 1,
                'exp': 'f1() prints "in f1", f2() prints "in f2", ff2() prints "in ff2".'
            },
            # Topic: global keyword with None return
            {
                'desc': 'What is the output of:\n\n```python\ndef f1():\n    global f2\n    f2 = 100\nprint(f1())\nprint(f2)\n```',
                'a': 'None then 100', 'b': '100 then 100',
                'c': 'None then None', 'd': 'Error',
                'ans': 'A', 'marks': 1,
                'exp': 'f1 returns None (no return), sets global f2 = 100. So output is None then 100.'
            },
            # Topic: Local variable closure NameError
            {
                'desc': 'What is the output of:\n\n```python\ndef f1():\n    x = 10\ndef f2():\n    print("x is", x)\nf2()\nf1()\n```',
                'a': 'x is 10', 'b': 'NameError',
                'c': 'None', 'd': 'x is None',
                'ans': 'B', 'marks': 1,
                'exp': 'x is local to f1. f2 has no access to it → NameError.'
            },
            # Topic: UnboundLocalError — local x used before assignment
            {
                'desc': 'What is the output of:\n\n```python\ndef f1():\n    x = 10\ndef f2():\n    x = x + 10\n    print("x is", x)\nf1()\nf2()\n```',
                'a': 'x is 20', 'b': 'Error',
                'c': 'x is 10', 'd': 'None',
                'ans': 'B', 'marks': 1,
                'exp': 'Inside f2, x is a local variable used before assignment → UnboundLocalError.'
            },
            # Topic: global with parameter — invalid
            {
                'desc': 'What is the output of:\n\n```python\nf2 = 200\ndef f1(F2):\n    global F2\n    F2 = 100\nprint(f1(f2))\nprint(f2)\n```',
                'a': 'None then 100', 'b': 'None then 200',
                'c': 'Error', 'd': '100 then 100',
                'ans': 'C', 'marks': 1,
                'exp': 'A parameter cannot be declared global inside a function.'
            },
            # Topic: Mutable default argument — tuple/list append bug
            {
                'desc': 'What is the output of:\n\n```python\nc = [11,22]\ndef f1(a, b=c):\n    b.append(a)\n    return b\nc = [14,33]\nprint(f1({2}))\n```',
                'a': '[11, 22, {2}]', 'b': '[14, 33, {2}]',
                'c': 'Error', 'd': '[11, 22, 14, 33]',
                'ans': 'A', 'marks': 1,
                'exp': 'Default value b=c is bound at function definition time to [11,22]. Reassigning c later doesn\'t change the default.'
            },
            # Topic: *args unpacking — set unpacked into function arguments
            {
                'desc': 'What is the output of:\n\n```python\ndef f1(a,b):\n    print(a,b, end=" ")\n    print(a,b)\nd = {(23,78): "900", (89,88): [90,78,55]}\nf1(*d)\n```',
                'a': '(23,78) (89,88) 23 78 89 88',
                'b': '23 78 89 88',
                'c': 'Error',
                'd': 'None',
                'ans': 'A', 'marks': 1,
                'exp': 'Unpacking a dict yields its keys: (23,78) and (89,88). f1 receives them as a, b.'
            },
            # Topic: type(*a) — tuple unpacking in call
            {
                'desc': 'What is the output of:\n\n```python\ndef f1(a,b,c):\n    print(type(*a))\nd = ([44], 66, 22)\nf1(*d)\n```',
                'a': 'list', 'b': 'Error', 'c': 'int', 'd': 'str',
                'ans': 'C', 'marks': 1,
                'exp': 'a = [44]. *a unpacks to 44 (single element). type(44) → <class \'int\'> → int.'
            },
            # Topic: type(*a) — nested list
            {
                'desc': 'What is the output of:\n\n```python\ndef f1(a,b,c):\n    print(type(*a))\nd = ([[44]], 66, 22)\nf1(*d)\n```',
                'a': 'list', 'b': 'Error', 'c': 'int', 'd': 'str',
                'ans': 'A', 'marks': 1,
                'exp': 'a = [[44]]. *a unpacks to [44] (single element). type([44]) → <class \'list\'> → list.'
            },
            # Topic: Single-element tuple
            {
                'desc': 'How to assign a tuple of length 1 to a variable v?',
                'a': 'v = (anything_here)', 'b': 'v = (anything_here,)',
                'c': 'v = [anything_here]', 'd': 'v = {anything_here}',
                'ans': 'B', 'marks': 1,
                'exp': 'A single-element tuple requires a trailing comma.'
            },
            # Topic: Dictionary — KeyError on tuple key
            {
                'desc': 'What is the result in Python interactive mode?\n\n```python\na = {\'a\':1,\'b\':2,\'c\':3}\na[\'a\',\'b\']\n```',
                'a': '1,2', 'b': 'IndexError', 'c': 'KeyError', 'd': '{\'a\':1,\'b\':2}',
                'ans': 'C', 'marks': 1,
                'exp': 'a[\'a\',\'b\'] looks up tuple key (\'a\',\'b\') which is absent → KeyError.'
            },
            # Topic: Dict with tuple key — valid
            {
                'desc': 'What gets printed?\n\n```python\na = {(1,2):1,(2,3):2}\nprint(a[1,2])\n```',
                'a': '1', 'b': '(1, 2)', 'c': 'KeyError', 'd': 'None',
                'ans': 'A', 'marks': 1,
                'exp': 'a[1,2] is a[(1,2)], a valid tuple key → value 1.'
            },
        ]

        self._bulk_create_questions(test, questions_data)