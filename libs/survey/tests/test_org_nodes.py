import pytest
from survey.errors import IncorrectOrgNodeValueError
from survey.org_nodes import OrgNode


@pytest.mark.parametrize(
    "test_input",
    (
        "",
        "foobar",
    ),
)
def test_constructing_org_node_with_bad_value_raises_error(test_input):
    with pytest.raises(IncorrectOrgNodeValueError):
        OrgNode.from_str(test_input)


@pytest.mark.parametrize(
    "test_input,expected",
    (
        ("N01", OrgNode((1,))),
        ("N01.", OrgNode((1,))),
        ("N01.01", OrgNode((1, 1))),
        ("N01.01.", OrgNode((1, 1))),
        ("N01.02.03.01", OrgNode((1, 2, 3, 1))),
        ("N01.02.03.01.", OrgNode((1, 2, 3, 1))),
        ("N002.003.0001", OrgNode((2, 3, 1))),
        ("N002.003.0001.", OrgNode((2, 3, 1))),
    ),
)
def test_org_node_can_be_constructed_from_valid_string(test_input, expected):
    assert OrgNode.from_str(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    (
        ((1, 1), "OrgNode(N01.01)"),
        ((1,), "OrgNode(N01)"),
        ((2, 5), "OrgNode(N02.05)"),
        ((1, 1, 1, 1, 1), "OrgNode(N01.01.01.01.01)"),
        ((1, 5, 3), "OrgNode(N01.05.03)"),
        ((2, 0, 1), "OrgNode(N02.00.01)"),
    ),
)
def test_org_node_repr(test_input, expected):
    assert repr(OrgNode(levels=test_input)) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    (
        # case 1
        (
            [
                OrgNode.from_str("N02.02."),
                OrgNode.from_str("N01.01."),
                OrgNode.from_str("N01."),
                OrgNode.from_str("N03."),
                OrgNode.from_str("N02."),
            ],
            [
                OrgNode.from_str("N01."),
                OrgNode.from_str("N01.01."),
                OrgNode.from_str("N02."),
                OrgNode.from_str("N02.02."),
                OrgNode.from_str("N03."),
            ],
        ),
        # case 2
        (
            [
                OrgNode.from_str("N02.02."),
                OrgNode.from_str("N02.02."),
            ],
            [
                OrgNode.from_str("N02.02."),
                OrgNode.from_str("N02.02."),
            ],
        ),
        # case 3
        (
            [
                OrgNode.from_str("N01.01.01.01.01.100."),
                OrgNode.from_str("N01."),
                OrgNode.from_str("N01.02."),
            ],
            [
                OrgNode.from_str("N01."),
                OrgNode.from_str("N01.01.01.01.01.100."),
                OrgNode.from_str("N01.02."),
            ],
        ),
        # case 4
        (
            [
                OrgNode.from_str("N01.01.01."),
                OrgNode.from_str("N01.01.01.01.01.01."),
                OrgNode.from_str("N01.01."),
                OrgNode.from_str("N01."),
            ],
            [
                OrgNode.from_str("N01."),
                OrgNode.from_str("N01.01."),
                OrgNode.from_str("N01.01.01."),
                OrgNode.from_str("N01.01.01.01.01.01."),
            ],
        ),
    ),
)
def test_sort_org_nodes(test_input, expected):
    assert sorted(test_input) == expected


@pytest.mark.parametrize(
    "obj_a,obj_b,expected",
    [
        (OrgNode.from_str("N01."), OrgNode.from_str("N01."), True),
        (OrgNode.from_str("N02."), OrgNode.from_str("N02."), True),
        (OrgNode.from_str("N03."), OrgNode.from_str("N03."), True),
        (OrgNode.from_str("N05."), OrgNode.from_str("N07."), False),
        (OrgNode.from_str("N05."), OrgNode.from_str("N05.01."), False),
        (OrgNode.from_str("N05."), OrgNode.from_str("N05.01."), False),
        (OrgNode.from_str("N05.05.03."), OrgNode.from_str("N05.05.03."), True),
        (
            OrgNode.from_str("N05.05.03."),
            OrgNode.from_str("N05.05.03.02.10.15."),
            False,
        ),
        (OrgNode.from_str("N05.05.03."), "foo", False),
        (OrgNode.from_str("N05.05.03."), 1, False),
    ],
)
def test_equality_of_org_nodes(obj_a, obj_b, expected):
    result = obj_a == obj_b
    assert result is expected


@pytest.mark.parametrize(
    "node",
    (
        OrgNode.from_str("N01."),
        OrgNode.from_str("N01.02."),
        OrgNode.from_str("N01.02.01."),
        OrgNode.from_str("N01.02.01.01."),
        OrgNode.from_str("N5."),
        OrgNode.from_str("N1.2."),
        OrgNode.from_str("N1.2.3"),
    ),
)
def test_converting_to_string_and_back_to_python_object(node: "OrgNode"):
    string_representation = node.to_str()
    assert OrgNode.from_str(string_representation) == node
