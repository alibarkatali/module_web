from db import Db

db = Db()


test = db.select("SELECT * FROM Player")
print test
