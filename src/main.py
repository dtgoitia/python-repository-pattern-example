from src.model import Account, Transaction


def main() -> None:
    from src.repository import Repository, create_session, engine

    session = create_session(engine)
    repo = Repository(session)

    account_a = Account(id="account_a", name="A")
    account_b = Account(id="account_b", name="B")

    transaction_a = Transaction(
        from_account=account_a,
        to_account=account_b,
        quantity=100,
    )
    transaction_b = Transaction(
        from_account=account_a,
        to_account=account_b,
        quantity=100,
    )

    repo.add_account(account_a)
    repo.add_account(account_b)

    repo.add_transaction(transaction_a)
    repo.add_transaction(transaction_b)

    accounts = repo.read_accounts()
    transactions = repo.read_transactions()

    print(accounts)
    print(transactions)

    assert accounts == [account_a, account_b]
    assert transactions == [transaction_a, transaction_b]


if __name__ == "__main__":
    main()
