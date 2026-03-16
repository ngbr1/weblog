from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.secret_key = 'super_secret_key_change_this_later'


users = {'endmin': 'sixseven'} 

online_users = {} 


@app.before_request
def track_user():
    if 'username' in session:
      
        if not request.path.startswith('/static'):
            online_users[session['username']] = request.path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
  
        action = request.form.get('action')
        user = request.form.get('username')
        pw = request.form.get('password')

        if action == 'register':
            if user in users:
                flash("Username already exists! Try another.")
            elif not user or not pw:
                flash("Please fill in both fields to register.")
            else:
                users[user] = pw
                flash("Registration successful! You can now log in.")
                
        elif action == 'login':
            if user in users and users[user] == pw:
              
                session['username'] = user
                return redirect(url_for('mainpage'))
            else:
                # Failed login
                flash("Login failed. Incorrect username or password.")

    return render_template('login.html')

@app.route('/mainpage')
def mainpage():
   
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('mainpage.html', username=session['username'])

@app.route('/security')
def security():
   
    if session.get('username') != 'endmin':
        return redirect(url_for('mainpage'))
    
    return render_template('security.html', all_users=users, online_users=online_users)

@app.route('/logout')
def logout():
    user = session.pop('username', None)
   
    if user in online_users:
        del online_users[user]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
