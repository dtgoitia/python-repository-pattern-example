import attr

AccountId = str
AccountName = str


@attr.s(auto_attribs=True)
class Account:
    id: AccountId
    name: AccountName


@attr.s(auto_attribs=True)
class Transaction:
    from_account: Account
    to_account: Account
    quantity: int  # in cents
