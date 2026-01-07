import tempfile
import os
from library_system.storage import LibraryStorage


def test_add_book_and_member_and_borrow_return(tmp_path):
    data_file = tmp_path / "lib.json"
    storage = LibraryStorage(path=str(data_file))

    b = storage.add_book("The Hobbit", "Tolkien", copies=2)
    assert b.id == 1
    m = storage.add_member("Alice")
    assert m.id == 1

    loan = storage.borrow_book(book_id=b.id, member_id=m.id)
    assert loan.book_id == b.id

    # copies decremented
    books = storage.list_books()
    assert books[0].copies == 1

    returned = storage.return_book(book_id=b.id, member_id=m.id)
    assert returned.returned_at is not None

    books = storage.list_books()
    assert books[0].copies == 2
