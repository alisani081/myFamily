from flask import Flask, render_template, request, url_for, session, flash, redirect, jsonify 
from models import *
import datetime as dt
from auth import login_user, login_required, create_account  

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://alisani:37277079@localhost/myFamily"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = b'"\x0eV\xb4\x97\n\x1e\xcd\x81\x9f\x9c]~I\xa4\xdb'
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=365)

def last_update_time():
    contribution = Contribution.query.order_by(Contribution.created.desc()).first()
    donation = Expenses.query.order_by(Expenses.created.desc()).first()

    if contribution.created > donation.created:
        return contribution.created
    else:
        return donation.created

@app.route("/admin", methods=["POST", "GET"])
@login_required
def admin():
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password')
        role = request.form.get('role')

        return create_account(username, password, role)

    return render_template("admin/admin.html")

@app.route("/auth/login", methods=["POST", "GET"])
def login(): 
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password')

        return login_user(username, password)

    if session.get('user_id') is not None:
       return redirect(url_for('index'))
       
    return render_template("auth/login.html")

@app.route("/")
@login_required
def index():
    contributions = Contribution.query.order_by(Contribution.created.desc()).all()
    month = dt.datetime.today().strftime("%b")   
    month_conts = Contribution.query.filter(Contribution.month.like(f"%{month}%")).order_by(Contribution.created.desc()).all()  
    donations = Expenses.query.all()
    return render_template("index.html", contributions=contributions, month_conts=month_conts, donations=donations, last_update_time=last_update_time())

@app.route("/manage", methods=["POST", "GET"])
@login_required
def manage():
    members = Member.query.all()
    contributions = Contribution.query.all()
    month = dt.datetime.today().strftime("%b")
    month_conts = Contribution.query.filter(Contribution.month.like(f"%{month}%")).all()
    donations = Expenses.query.all()
    return render_template("admin/manage.html", members=members, contributions=contributions, month_conts=month_conts, donations=donations, last_update_time=last_update_time())
    
@app.route("/contribute", methods=["POST"])
def contribute():
    if request.method == "POST":
        error = False
        name = request.form["name"]
        amount = request.form["amount"]
        month = request.form["month"]

        cont = Contribution(name=name, amount=amount, month=month)
        db.session.add(cont)
        db.session.commit()

        if not error:
            return jsonify(success=True,name=name,amount=amount,month=month)
        else:
            return jsonify(success=False,error='There was an error, please, try aagin')

@app.route("/withdraw", methods=["POST"])
def withdraw():
    if request.method == "POST":
        # Get form data
        title = request.form["title"]
        amount = int(request.form["withdrawAmt"])
        remark = request.form["remark"]

        # Get current balance
        amounts = []
        contributions = Contribution.query.all()
        for contribution in contributions:        
            amounts.append(contribution.amount)
        balance = int(sum(amounts))

        if amount > balance:
            return jsonify(success=False,error="Withdrawal error, Insufficient fund...")
        else:
            expense = Expenses(name=title,amount=amount,remark=remark)
            db.session.add(expense)
            db.session.commit()

            return jsonify(success=True,title=title,amount=amount,remark=remark)

@app.route("/donation")
@login_required
def donation():
    month = dt.datetime.today().strftime("%b")
    month_conts = Contribution.query.filter(Contribution.month.like(f"%{month}%")).all()
    donations = Expenses.query.order_by(Expenses.created.desc()).all()
    contributions = Contribution.query.all()
    return render_template("donation.html", donations=donations, contributions=contributions, month_conts=month_conts, last_update_time=last_update_time())

@app.route("/statement")
@login_required
def statement():
    ctr_credits = Contribution.query.order_by(Contribution.created.desc()).all()
    exp_debits = Expenses.query.order_by(Expenses.created.desc()).all()
    statements = []
    statements.append(ctr_credits)
    statements.append(exp_debits)
    return render_template("statement.html", statements=statements)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))
