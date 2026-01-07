"""Simple command-line interface for the library system."""
import argparse
from .storage import LibraryStorage


def main(argv=None):
    parser = argparse.ArgumentParser(prog="library-cli")
    parser.add_argument("--data", help="path to data file (JSON)")
    sub = parser.add_subparsers(dest="cmd")

    # add-book
    p = sub.add_parser("add-book")
    p.add_argument("title")
    p.add_argument("author")
    p.add_argument("--copies", type=int, default=1)

    # list-books
    sub.add_parser("list-books")

    # add-member
    p = sub.add_parser("add-member")
    p.add_argument("name")

    # list-members
    sub.add_parser("list-members")

    # borrow
    p = sub.add_parser("borrow")
    p.add_argument("book_id", type=int)
    p.add_argument("member_id", type=int)

    # return
    p = sub.add_parser("return")
    p.add_argument("book_id", type=int)
    p.add_argument("member_id", type=int)

    # list-loans
    sub.add_parser("list-loans")

    args = parser.parse_args(argv)
    storage = LibraryStorage(path=args.data) if args.data else LibraryStorage()

    if args.cmd == "add-book":
        b = storage.add_book(args.title, args.author, copies=args.copies)
        print(f"Added book: {b}")
    elif args.cmd == "list-books":
        for b in storage.list_books():
            print(b)
    elif args.cmd == "add-member":
        m = storage.add_member(args.name)
        print(f"Added member: {m}")
    elif args.cmd == "list-members":
        for m in storage.list_members():
            print(m)
    elif args.cmd == "borrow":
        loan = storage.borrow_book(args.book_id, args.member_id)
        print(f"Loan created: {loan}")
    elif args.cmd == "return":
        loan = storage.return_book(args.book_id, args.member_id)
        print(f"Returned: {loan}")
    elif args.cmd == "list-loans":
        for l in storage.list_loans():
            print(l)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
