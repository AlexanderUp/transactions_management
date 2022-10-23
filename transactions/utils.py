from Cryptodome.Hash import SHA1


def sign_transaction(private_key,
                     transaction_id,
                     user_id,
                     account_id,
                     amount):
    data = (f"{private_key}"
            f":{transaction_id}"
            f":{user_id}"
            f":{account_id}"
            f":{amount}".encode(encoding="utf-8"))
    hasher = SHA1.new()
    hasher.update(data)
    return hasher.hexdigest()
