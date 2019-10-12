#create user and add to database.
def create_user(username, password, firstName, lastName, email, confirmation, dbclient):
    db = dbclient["moolaDatabase"]
    users = db["users"]
    x = users.find({},{"username":username})
    if x.count() > 0:
        print("Username exists")
    else:
        if(password != confirmation):
            print("Passwords do not match. ")
        else:
            user = {"username": username,"password": password, "firstName":firstName, "lastName": lastName, "email": email}
            users.insert_one(user)


