#create user and add to database.
def create_user(userID, dbclient):
    db = dbclient["moolaDatabase"]
    users = db["users"]
    x = users.find({},{"id":userID})
    if x.count() == 0:
        users.insert_one({"id": userID, "value": 0})

def check_transaction(transaction, userID, dbclient):
    db = dbclient["moolaDatabase"]
    transactions = db["transactions"]
    x = transactions.find({"id":transaction["transaction_info"]["transaction_id"]})
    if x.count() == 0:
        amount = transaction["transaction_info"]["transaction_amount"]["value"]
        addend = float(str(amount)[-3:]) if '.' in str(amount)[-2:] else int(str(amount)[-2:])

        if addend != 0:
            addend = 100 - addend
        else:
            addend = 0

        addend /= 100.0

        transactions.insert({"id":transaction["transaction_info"]["transaction_id"], "userID": userID, "value": amount, "mula_value": addend})
        update_amount(userID, transaction["transaction_info"]["transaction_amount"]["value"], dbclient)
        return False
    else:
        return True

def update_amount(userID, amount, dbclient):
    db = dbclient["moolaDatabase"]
    users = db["users"]
    #get last 2 digits.
    addend = float(str(amount)[-3:]) if '.' in str(amount)[-2:] else int(str(amount)[-2:])
    print(addend)
    if addend != 0:
        addend = 100 - addend
    else:
        addend = 0

    addend/=100.0

    users.update({"id":userID},{"$inc": {"value": float(addend)}})





