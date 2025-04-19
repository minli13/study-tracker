from flask import Flask, redirect, render_template, request, session, jsonify, flash, get_flashed_messages
from flask_session import Session
import bcrypt
from helpers import login_required
import mysql.connector
from datetime import timedelta, datetime
import re
from config import Config

# Connect to the database
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="study_tracker",
    connection_timeout=300
)

# Create a cursor object to execute SQL commands
mydb = db.cursor()

# Configure application
app = Flask(__name__)
app.config.from_object(Config)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False # Session expires on browser close
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_SECURE'] = True  # Ensures cookies are sent only over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevents JavaScript access to cookies

Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

@app.route('/update_database', methods=['POST'])
def update_database():
    try:
        # Get the list of updated task IDs
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400
        updated_task_ids = data.get('taskIds', [])

        print(f"Updated task IDs to update database: {updated_task_ids}")

        # Loop through each updated task and update the database
        for task_id in updated_task_ids:
            now = datetime.now()
            week_name = now.strftime("%A")
            month_name = now.strftime("%B")
            day = now.strftime("%d")
            year = now.strftime("%Y")
            completed_date = f"{week_name}, {month_name} {day}, {year}"
            # Update the database with the new completion status and completed_date
            mydb.execute(
                "UPDATE tasks SET completion = %s, completed_date = %s WHERE id = %s", 
                ('1', completed_date, task_id)
            )
        db.commit()
        return jsonify({'status': 'success', 'message': 'Tasks updated successfully'})
    except Exception as e:
        print(f"Error updating tasks in database: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect("/login")
    
    # Fetch username
    try:
        mydb.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        username = mydb.fetchone()
        username = username[0]
    except Exception as e:
        print(f"Error fetching username: {e}")

    # Fetch all tasks for GET requests
    try:
        mydb.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        tasks = mydb.fetchall()
    except Exception as e:
        print(f"Error fetching tasks: {e}")

    if request.method=="POST":
        action = request.form.get("action")
        # Add a new task to the database
        if action == "add_task":
            task = request.form.get("task")
            due_date = request.form.get("due_date")
            tags = request.form.get("tags")
            try:
                mydb.execute("INSERT INTO tasks (user_id, task, due_date, tags) VALUES (%s, %s, %s, %s)", (user_id, task, due_date, tags))
                db.commit()
                print("Task added")
            except Exception as e:
                print(f"Error adding task: {e}")
        return redirect("/")
    return render_template("index.html", name=username, tasks=tasks)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget the user ID without clearing flashed messages
    session.pop("user_id", None)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get("remember")

        # Fetch the hashed password from the database
        mydb.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = mydb.fetchone()

        # Fetch the user_id from the database
        mydb.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = mydb.fetchone()
        if result:
            stored_hashed_password = result[0]
            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                # Make session permanent if "Remember Me" is checked
                if remember:
                    session.permanent = True  # Has a default time for session to expire
                else:
                    session.permanent = False  # Session expires on browser close
                # Remember which user has logged in
                session["user_id"] = user_id[0]
                user_id = session.get("user_id")
                return redirect("/")    
            else:
                flash("Invalid username or password.", "error")
                return redirect("/login")
        else:
            flash("Invalid username or password.", "error")
            return redirect("/login")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    session["user_id"] = None
    print("Logged out.")

    # Redirect user to login form
    return redirect("/login")

def checkPassword(password):
    # ensure at least one letter
    # ensure at least one digit
    # ensure at least one special character
    # ensure password is at least 8 characters long
    pattern = re.compile(r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$')
    if pattern.match(password): 
        return True 
    else: 
        return False

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        # Check if password is same as confirm password
        if password != confirm_password:
            flash("Invalid password confirmation.", "error")
            return redirect("/register")
        strong = checkPassword(password)
        if not strong:
            flash("Passsword is not strong enough. Please ensure your password meets the following criteria:"
                "<ul><li>At least one letter.</li><br>"
                "<li>At least one digit.</li><br>"
                "<li>At least one special character.</li><br>"
                "<li>Minimum length of 8 characters.</li></ul>",
                "error")
            return redirect("/register")

        # Check if username exists
        mydb.execute(
            "SELECT * FROM users WHERE username = %s", (username,)
        )
        if len(mydb.fetchall()) > 0:
            flash("Username already exists.", "error")
            return redirect("/register")
        
        '''Future implementation'''
        # Check if email exists
        '''
        mydb.execute(
            "SELECT * FROM users WHERE email = %s", (email,)
        )
        if len(mydb.fetchall()) > 0:
            flash("Email is already in use.", "error")
            return redirect("/register")
        '''
        try:
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # Insert username and hashed password into the database
            mydb.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password)
            )
            db.commit()
            print("Account made.")
            return redirect("/login")
        except Exception as e:
            print(f"Error registering: {e}")
    else:
        return render_template("register.html")

@app.route("/timer", methods=["GET", "POST"])
@login_required
def timer():
    user_id = session.get('user_id')
    if not user_id:
        return redirect("/login")
    # Fetch all tasks for GET requests
    try:
        mydb.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        tasks = mydb.fetchall()
    except Exception as e:
        print(f"Error fetching tasks: {e}")
    return render_template("timer.html", tasks=tasks)

@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    user_id = session.get('user_id')
    if not user_id:
        return redirect("/login")
    
    if request.method == "POST":
        currentPassword = request.form.get("currentPassword")
        newPassword = request.form.get("newPassword")
        confirmPassword = request.form.get("confirmNewPassword")

        # Get username
        mydb.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        username = mydb.fetchone()
        username = username[0]

        # Ensure username is correct
        if request.form.get("username") != username:
            flash("Invalid username or password.", "error")
            return redirect("/changePassword")

        # Query database for hashed password
        mydb.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
        stored_hashed_password = mydb.fetchone()
        stored_hashed_password = stored_hashed_password[0]
        if not bcrypt.checkpw(currentPassword.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            flash("Invalid username or password.", "error")
            return redirect("/changePassword")
        
        # Ensure new password is same as confirm password
        if confirmPassword != newPassword:
            flash("Invalid username or password.", "error")
            return redirect("/changePassword")
        
        # Ensure new password is not the same as old password
        if bcrypt.checkpw(newPassword.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            flash("New password cannot be the same as old password.", "error")
            return redirect("/changePassword")

        # Ensure new password is strong
        strong = checkPassword(newPassword)
        if not strong:
            flash("New password is not strong enough. Please ensure your password meets the following criteria:"
                "<ul><li>At least one digit.</li><br>"
                "<li>At least one special character.</li><br>"
                "<li>Minimum length of 8 characters.</li></ul>",
                "error")
            return redirect("/changePassword")

        else:
            # Update database with new password
            try:
                # Hash the password
                hashed_password = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                # Insert username and hashed password into the database
                mydb.execute("UPDATE users SET password_hash = %s WHERE username = %s", (hashed_password, username))
                db.commit()
                # Redirect to login
                session.clear()
                return redirect("/login")
            except Exception as e:
                return(f"Error changing passwords: {e}")
    else:
        return render_template("changePassword.html")

if __name__ == "__main__":
    app.run(debug=True)