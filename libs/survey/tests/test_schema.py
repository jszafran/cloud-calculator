from typing import Any

import pytest
from survey.errors import (
    ColumnMinValueMustBeSmallerThanMaxValueError,
    ColumnMissingCodeValueError,
    ColumnMissingTextValueError,
)
from survey.schemas import Column, ColumnType, Schema


@pytest.fixture
def column_test_data() -> dict[str, Any]:
    return {
        "code": "c1",
        "text": "c1 text",
        "min_value": 1,
        "max_value": 5,
        "nullable": True,
    }


def test_creating_question_with_ok_data(column_test_data):
    question = Column(
        type=ColumnType.QUESTION,
        **column_test_data,
    )

    assert question.type == ColumnType.QUESTION
    assert question.code == column_test_data.get("code")
    assert question.text == column_test_data.get("text")
    assert question.min_value == column_test_data.get("min_value")
    assert question.max_value == column_test_data.get("max_value")
    assert question.nullable is column_test_data.get("nullable")


def test_creating_demographics_with_ok_data(column_test_data):
    question = Column(
        type=ColumnType.DEMOGRAPHICS,
        **column_test_data,
    )

    assert question.type == ColumnType.DEMOGRAPHICS
    assert question.code == column_test_data.get("code")
    assert question.text == column_test_data.get("text")
    assert question.min_value == column_test_data.get("min_value")
    assert question.max_value == column_test_data.get("max_value")
    assert question.nullable is column_test_data.get("nullable")


@pytest.mark.parametrize(
    "params,exception",
    [
        ({"code": ""}, ColumnMissingCodeValueError),
        ({"text": ""}, ColumnMissingTextValueError),
        (
            {"min_value": 2, "max_value": 2},
            ColumnMinValueMustBeSmallerThanMaxValueError,
        ),
        (
            {"min_value": 2, "max_value": 1},
            ColumnMinValueMustBeSmallerThanMaxValueError,
        ),
    ],
)
def test_column_raises_error_when_created_with_bad_data(
    params, exception, column_test_data
):
    with pytest.raises(exception):
        data = column_test_data | params
        Column(
            type=ColumnType.QUESTION,
            **data,
        )


def test_creating_schema():
    q1 = Column(
        type=ColumnType.QUESTION,
        code="q1",
        text="q1 text",
        min_value=1,
        max_value=2,
        nullable=True,
    )
    q2 = Column(
        type=ColumnType.QUESTION,
        code="q1",
        text="q1 text",
        min_value=1,
        max_value=3,
        nullable=True,
    )

    d1 = Column(
        type=ColumnType.DEMOGRAPHICS,
        code="d1",
        text="d1 text",
        min_value=1,
        max_value=2,
        nullable=False,
    )

    schema = Schema(
        org_node_column_name="org_node",
        columns=tuple([q1, q2, d1]),
    )

    assert schema.questions == (q1, q2)
    assert schema.demographics == (d1,)


def test_parsing_schema_from_yaml(test_data_dir):
    print(test_data_dir, "hello!")
    test_file = test_data_dir / "test_schema.yml"

    q1 = Column(
        type=ColumnType.QUESTION,
        code="Q1",
        text="Q1 text",
        min_value=1,
        max_value=6,
        nullable=True,
    )

    q2 = Column(
        type=ColumnType.QUESTION,
        code="Q2",
        text="Q2 text",
        min_value=1,
        max_value=3,
        nullable=True,
    )

    q3 = Column(
        type=ColumnType.QUESTION,
        code="Q3",
        text="Q3 text",
        min_value=1,
        max_value=2,
        nullable=False,
    )

    d1 = Column(
        type=ColumnType.DEMOGRAPHICS,
        code="D1",
        text="D1 text",
        min_value=1,
        max_value=3,
        nullable=True,
    )

    d2 = Column(
        type=ColumnType.DEMOGRAPHICS,
        code="D2",
        text="D2 text",
        min_value=1,
        max_value=2,
        nullable=True,
    )

    schema = Schema.from_yaml(test_file)

    assert schema.questions[0] == q1
    assert schema.questions[1] == q2
    assert schema.questions[2] == q3
    assert schema.demographics[0] == d1
    assert schema.demographics[1] == d2
