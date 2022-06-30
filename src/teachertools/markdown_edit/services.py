import re

import markdown
import markdownify

ANSWERS_UL = r'^(.*?)<ul>(.*?)</ul>(.*?)$'
ANSWERS_OL = r'^(.*?)<ol>(.*?)</ol>(.*?)$'
ANSWER = r'<li>(.*?)</li>'


def md2html(md):
    return markdown.markdown(md.strip())


def html2md(html):
    return markdownify.markdownify(html.strip()).strip()


def split_question_html(html):
    for pattern in [ANSWERS_UL, ANSWERS_OL]:
        if re.match(pattern, html, re.DOTALL):
            before, answers, after = re.findall(ANSWERS_UL, html, re.DOTALL)[0]
            return (
                before.strip() or after.strip(),
                answers
            )
    raise ValueError('No answers detected')


def parse_answers_html(html):
    return [html2md(a) for a in re.findall(ANSWER, html, re.DOTALL)]


def parse_question(data):
    """
    0. Clean: strip
    1. Parse md -> html
    2. Extract answers list:
        Find ul -> None: Find ol -> None: ValueError
    3. Prepare question text: html -> md
    4. Prepare answers list: split, remove li, html -> md

    Return
        - question text (md str)
        - answers list (each answer as md str)
    """
    html = md2html(data)
    text_html, answers_html = split_question_html(html)

    text = html2md(text_html)
    answer_list = parse_answers_html(answers_html)

    return text, answer_list


def is_question_valid(md):
    html = md2html(md)
    for pattern in [ANSWERS_UL, ANSWERS_OL]:
        if re.match(pattern, html, re.DOTALL):
            return True
    return False
