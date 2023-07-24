import dataclasses
from functools import total_ordering
from typing import Self

from survey.errors import IncorrectOrgNodeValueError


@dataclasses.dataclass(frozen=True)
@total_ordering
class OrgNode:
    """
    Object representing single node (or unit) in an organization structure.
    Depending on the structure of company, you could think of it as a business unit
    (Marketing, Finance) or some kind of person (manager).
    """

    levels: tuple[int, ...]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_str()})"

    def __len__(self) -> int:
        return len(self.levels)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrgNode):
            return NotImplemented
        return self.levels == other.levels

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, OrgNode):
            raise NotImplementedError

        if self == other:
            return False

        non_zero_diffs = [
            v1 - v2 for v1, v2 in zip(self.levels, other.levels) if v1 - v2 != 0
        ]

        if not non_zero_diffs:
            return len(self) < len(other)

        return non_zero_diffs[0] < 0

    def to_str(self) -> str:
        return f"N{'.'.join(f'0{i}' if i < 10 else str(i) for i in self.levels)}"

    @classmethod
    def from_str(cls, v: str) -> Self:
        if not v:
            raise IncorrectOrgNodeValueError(
                "Cannot construct org node from empty string."
            )

        v = "".join(v[:-1]) if v[-1] == "." else v
        try:
            levels = tuple([int(x) for x in v[1:].split(".")])
        except ValueError:
            raise IncorrectOrgNodeValueError(
                f"Cannot construct org node from value {v}."
            )
        return cls(levels=levels)
