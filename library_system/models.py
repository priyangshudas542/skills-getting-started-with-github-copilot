from dataclasses import dataclass, asdict
from typing import Optional
import datetime


@dataclass
class Book:
    id: int
    title: str
    author: str
    copies: int = 1

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Book(**d)


@dataclass
class Member:
    id: int
    name: str

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Member(**d)


@dataclass
class Loan:
    book_id: int
    member_id: int
    borrowed_at: str
    returned_at: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Loan(**d)
