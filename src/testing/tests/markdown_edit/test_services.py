import pytest

from teachertools.markdown_edit.services import parse_question

QUESTION_1 = """
1) Which Python package would you like to learn more about?

- pandas
- numpy
- flask
- matplotlib
"""

QUESTION_1_EXPECTED = (
    '1) Which Python package would you like to learn more about?',
    ['pandas', 'numpy', 'flask', 'matplotlib']
)

QUESTION_2 = """
2) Which of the following Python commands is correct?

* `print hello world`
* `print('hello world')`
* `print << 'hello world'`
* `print(hello world)`
"""

QUESTION_2_EXPECTED = (
    '2) Which of the following Python commands is correct?',
    [
        '`print hello world`',
        '`print(\'hello world\')`',
        '`print << \'hello world\'`',
        '`print(hello world)`',
    ]
)

QUESTION_3 = """
- pandas
- numpy
- flask
- matplotlib
"""

QUESTION_3_EXPECTED = (
    '',
    ['pandas', 'numpy', 'flask', 'matplotlib']
)

QUESTION_4 = """
- pandas
- numpy
- flask
- matplotlib


Which Python package would you like to learn more about?
"""

QUESTION_4_EXPECTED = (
    'Which Python package would you like to learn more about?',
    ['pandas', 'numpy', 'flask', 'matplotlib']
)


@pytest.mark.parametrize(
    'data, expected',
    (
        (QUESTION_1, QUESTION_1_EXPECTED),
        (QUESTION_2, QUESTION_2_EXPECTED),
        (QUESTION_3, QUESTION_3_EXPECTED),
        (QUESTION_4, QUESTION_4_EXPECTED),
    )
)
def test_markdown_divided_into_parts(data, expected):
    assert parse_question(data) == expected
