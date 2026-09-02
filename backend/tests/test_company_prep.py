from app.services.company_prep_service import parse_company_questions


SAMPLE = """
# Example Company
## Technical Round Questions
<article>
What is a database index, and when should you use one?
<details><summary>Show Answer</summary>
An index speeds up reads but adds storage and write overhead.
</details>
</article>
<article>
Given:
- an array of integers
- a target value

Return the matching pair.
[**Submit Code**](https://example.com/problem)
</article>
"""


def test_parse_company_questions_extracts_articles_and_hides_markup():
    questions = parse_company_questions(SAMPLE, "example.md")

    assert len(questions) == 2
    assert questions[0]["section"] == "Technical Round Questions"
    assert questions[0]["question"] == (
        "What is a database index, and when should you use one?"
    )
    assert questions[0]["answer"].startswith("An index speeds up reads")
    assert questions[1]["question"].endswith("Submit Code")
    assert "<article>" not in questions[1]["question"]


def test_parse_company_questions_produces_stable_ids():
    first = parse_company_questions(SAMPLE, "example.md")
    second = parse_company_questions(SAMPLE, "example.md")

    assert [item["id"] for item in first] == [item["id"] for item in second]
