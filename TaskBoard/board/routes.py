from board import app,db
from flask import render_template,request, flash, url_for, redirect, jsonify, session
from sqlalchemy import text
#import mysql.connector



@app.route('/')
def home_page():
    cookie = request.cookies.get('name')
    print("<>home_page()")
    return render_template('home.html', cookie=cookie)

@app.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        print(username)
        print(password)

        if (username is None or
                isinstance(username,str) is False
                or len(username) < 3):
            print("not valid")
            flash(f"Username is not valid", category='warning')
            return render_template('login.html', cookie = None)

        if (password is None or
                isinstance(password, str) is False
                or len(password) < 3):
            print("not valid")
            flash(f"Password is not valid", category='warning')
            return render_template('login.html', cookie = None)

        query_stmt = f"select username from users where username = '{username}' and password = '{password}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))
        user = result.fetchall()

        if not user:
            flash(f"Try again", category='warning')
            print("debug2")
            return render_template('login.html')
        #wenn alles gut
        flash(f"You are logged in {user}", category='success')
        session['name'] = username
        #resp = redirect('board')
        #resp.set_cookie('name', username)
        print('<- login_page(),go to board_page')
        return redirect(url_for('board_page'))

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register_page():
    if request.method == 'POST':
        print('Post')

        username = request.form.get('Username')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        print(username)
        print(email)
        print(password1)
        print(password2)

        if (username is None or
                isinstance(username,str) is False
                or len(username) < 3):
            print("not valid")
            #flash(f"Username is not valid", category='danger')
            return render_template('register.html', cookie=None)

        if (email is None or
                isinstance(email,str) is False
                or len(email) < 3):
            print("not valid")
            #flash(f"Email is not valid", category='danger')
            return render_template('register.html', cookie = None)

        if (password1 is None or
                isinstance(password1, str) is False
                or len(password1) < 3) or password1 != password2:
            print("not valid")
            #flash(f"Password is not valid", category='danger')
            return render_template('register.html', cookie = None)

        query_stmt = f"select * from users where username = '{username}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))
        item = result.fetchall()
        print(item)

        # User already in db
        if len(item) != 0:
            print("Bin Hier")
            #flash(f"User exists, try again", category='danger')
            return render_template('register.html', cookie = None)

        query_insert = f"insert into users (username, email, password) values ('{username}','{email}','{password2}')"
        print("debug1")
        print(query_insert)
        db.session.execute(text(query_insert))
        print("debug2")
        db.session.commit()
        #flash(f"You are registered", category='success')
        #resp = redirect('/board')
        #resp.set_cookie('name', username)
        session['name'] = username
        print('<- register_page(),go to board_page')
        return redirect(url_for('board_page'))

    return render_template('register.html')



@app.route('/table')
def table_page():
   cookie = request.cookies.get('name')
   print("->tickets_pages()", cookie)
   if not request.cookies.get('name'):
       print("->table_page() no cookie")
       return redirect(url_for('login_page'))
   query_stmt = f"SELECT tasks.id, users.username, tasks.title, tasks.status, tasks.priority,tasks.description FROM tasks JOIN users ON tasks.userID = users.ID"
   result = db.session.execute(text(query_stmt))
   itemsquery = result.fetchall()
   print(itemsquery)
   return render_template('table.html', items=itemsquery, cookie=cookie)


@app.route('/board')
def board_page():
   #cookie = request.cookies.get('name')
   #print("->tickets_pages()", cookie)
   if not session.get('name'):
       print("->board_page() no cookie")
       return redirect(url_for('login_page'))

   query_stmt = f"SELECT tasks.id, users.username, tasks.title, tasks.status, tasks.priority,tasks.description FROM tasks JOIN users ON tasks.userID = users.ID"
   result = db.session.execute(text(query_stmt))
   itemsquery = result.fetchall()

   print(itemsquery)
   return render_template('board.html', items=itemsquery)



@app.route('/logout')
def logout():
    #resp = redirect('/')
    #resp.set_cookie('name','',expires=0)
    session['name'] = None
    return redirect(url_for('home_page'))


@app.route('/task_entry', methods=['GET','POST'])
def task_entry():
    #cookie = request.cookies.get('name')
    #print("->task_entry()",cookie)
    if not session.get("name"):
        print("No cookie")
        return redirect(url_for('login'))
    if request.method == 'POST':
        priority = request.form.get('Priority')
        username = request.form.get('Username')
        title = request.form.get('Title')
        description = request.form.get('Description')
        status = request.form.get('Status')

        # Benutzer-ID anhand des Benutzernamens abfragen
        user_id_result = db.session.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": username}
        )

        user_id = user_id_result.fetchone()
        if user_id is not None:
            user_id = user_id[0]

        query_insert = f"insert into tasks (userID, title, description, status, priority) values ({user_id},'{title}','{description}','{status}',{priority})"
        print(query_insert)
        db.session.execute(text(query_insert))
        #commit immer nach insert
        db.session.commit()
        #resp = redirect('/board')
        #resp.set_cookie('name',cookie)
        return redirect(url_for('board_page'))

    return render_template('task_entry.html')


@app.route('/task_item/<int:item_id>', methods=['GET'])
def ticket_item(item_id):
    print("ticket_item -->Debug1")
    query_stmt = f"select * from tasks where id={item_id}"
    result = db.session.execute(text(query_stmt))
    item = result.fetchall()
    print("ticket_item  ",query_stmt)

    if not item:
        print("item not existing")
        # error handling ...
    print(item)
    #cookie = request.cookies.get('name')

    return render_template('task_item.html', items=item)