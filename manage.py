import csv
from flask import Flask, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://alisani:37277079@localhost/myFamily"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

    # Insert names to db
    f = open("names.csv")
    reader = csv.reader(f)
    for name, relationship in reader:
        member = Member(name=name, relationship=relationship)
        db.session.add(member)
        print(f"Added {name} successfully!")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()