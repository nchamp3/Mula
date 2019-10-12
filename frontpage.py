#create user and add to database.
def create_user(username, password, firstName, lastName, email, confirmation, dbclient):
    db = dbclient["moolaDatabase"]
    users = db["users"]
    x = users.find({},{"username":username})
    if x.count() > 0:
        print("Username exists")
    else:
        #TODO : Check if confirm equals passowrd
        user = {"username": username,"password": password, "firstName":firstName, "lastName": lastName, "email": email}
        users.insert_one(user)