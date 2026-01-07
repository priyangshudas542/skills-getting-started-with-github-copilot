import json
from typing import Dict, List
from .models import Book, Member, Loan
import os
import threading
import datetime


class LibraryStorage:
    """Simple JSON file backed storage for library objects."""

    def __init__(self, path: str = None):
        self._path = path or os.path.join(os.getcwd(), "library_data.json")
        self._lock = threading.Lock()
        self._data = {"books": [], "members": [], "loans": []}
        self._load()

    def _load(self):
        if os.path.exists(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self._data = raw
            except Exception:
                self._data = {"books": [], "members": [], "loans": []}

    def _save(self):
        with self._lock:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)

    # Books
    def add_book(self, title: str, author: str, copies: int = 1) -> Book:
        books = [Book.from_dict(b) for b in self._data["books"]]
        next_id = max((b.id for b in books), default=0) + 1
        book = Book(id=next_id, title=title, author=author, copies=copies)
        self._data["books"].append(book.to_dict())
        self._save()
        return book

    def list_books(self) -> List[Book]:
        return [Book.from_dict(b) for b in self._data["books"]]

    def find_book(self, book_id: int) -> Book:
        for b in self.list_books():
            if b.id == book_id:
                return b
        raise KeyError("Book not found")

    # Members
    def add_member(self, name: str) -> Member:
        members = [Member.from_dict(m) for m in self._data["members"]]
        next_id = max((m.id for m in members), default=0) + 1
        member = Member(id=next_id, name=name)
        self._data["members"].append(member.to_dict())
        self._save()
        return member

    def list_members(self) -> List[Member]:
        return [Member.from_dict(m) for m in self._data["members"]]

    def find_member(self, member_id: int) -> Member:
        for m in self.list_members():
            if m.id == member_id:
                return m
        raise KeyError("Member not found")

    # Loans
    def borrow_book(self, book_id: int, member_id: int) -> Loan:
        book = self.find_book(book_id)
        if book.copies <= 0:
            raise ValueError("No copies available")
        # decrement copy count
        for b in self._data["books"]:
            if b["id"] == book_id:
                b["copies"] = b.get("copies", 1) - 1
                break
        now = datetime.datetime.utcnow().isoformat()
        loan = Loan(book_id=book_id, member_id=member_id, borrowed_at=now)
        self._data["loans"].append(loan.to_dict())
        self._save()
        return loan

    def return_book(self, book_id: int, member_id: int) -> Loan:
        # find active loan
        for l in self._data["loans"]:
            if l["book_id"] == book_id and l["member_id"] == member_id and l.get("returned_at") is None:
                l["returned_at"] = datetime.datetime.utcnow().isoformat()
                # increment copies
                for b in self._data["books"]:
                    if b["id"] == book_id:
                        b["copies"] = b.get("copies", 0) + 1
                        break
                self._save()
                return Loan.from_dict(l)
        raise KeyError("Active loan not found")

    def list_loans(self):
        return [Loan.from_dict(l) for l in self._data["loans"]]
