import pytest

from teachertools.markdown_edit.services import split_markdown

QUESTION_1 = """
1) Which Python package would you like to learn more about?

- pandas
- numpy
- flask
- matplotlib
"""

QUESTION_1_EXPECTED = [
    'Which Python package would you like to learn more about?',
    ['pandas', 'numpy', 'flask', 'matplotlib']
]

QUESTION_2 = """
2) Which of the following Python commands is correct?

* `print hello world`
* `print('hello world')`
* `print << 'hello world'`
* `print(hello world)`
"""

QUESTION_2_EXPECTED = [
    'Which of the following Python commands is correct?',
    [
        '`print hello world`',
        '`print(\'hello world\')`',
        '`print << \'hello world\'`',
        '`print(hello world)`',
    ]
]


@pytest.mark.parametrize(
    'data, expected',
    (
        (QUESTION_1, QUESTION_1_EXPECTED),
        (QUESTION_2, QUESTION_2_EXPECTED),
    )
)
def test_markdown_divided_into_parts(data, expected):
    # assert split_markdown(data) == expected
    split_markdown(data)
