from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, body, owner):
        
        self.title = title
        self.body = body
        self.completed = True
        self.owner = owner  

#@app.before_request
#def require_login():
    #allowed_routes = ['login', 'blogpost', 'index', 'signup']

    #if request.endpoint not in allowed_routes and 'username' not in session:
        #return redirect('/login')


@app.route('/blog', methods=['POST', 'GET'])
def index():
    #if request.method == 'POST':
        #blog_name = request.form['new_blog']
        #blog_title = request.form['title']
        
        
        #new_blog = Blog(blog_title, blog_name)
        #db.session.add(new_blog)
        #db.session.commit()    

    

        #blog = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build a Blog", 
        completed_blogs=completed_blogs)

#@app.route('/newpost', methods=['POST','GET'])
#def new_blog():
    #return render_template('newpost.html')

@app.route("/blogpost", methods=['GET'])
def blogpost():
    if request.args.get('id'):
        blog_id = request.args.get('id')
        post = Blog.query.get(blog_id)
        owner_id = request.args.get('id')
        owner = Blog.query.get(owner_id)
        return render_template('post.html', post=post, owner=owner)

    
    if request.args.get('user'):
        username = request.args.get('user')
        user = User.query.filter_by(username=username).first()
        posts = user.blogs
        return render_template('user.html', posts=posts, user=user)
    
    if request.method == 'POST':
        blog_title = request.form['blog_entry_title']
        blog_content = request.form['blog_entry_content']

        if not blog_title or not blog_content:
            flash('Please fill in both fields', 'error')
            return render_template('newpost.html')

        else:
            owner = User.query.filter_by(username=session['username']).first()
            new_post = Blog(blog_title, blog_content, owner)
            db.session.add(new_post)
            db.session.commit()
            new_post = Blog.query.filter_by(blog_title=blog_title).first()

            return redirect('/blog?id={0}'.format(new_post.blog_id))

            

    posts = Blog.query.all()
    users = User.query.all()

    return render_template('blog.html', posts=posts, users=users)

    
    #id = request.args.get("id")
    #blog = Blog.query.get(id)
    #title = blog.title
    #body = blog.body


    #return render_template('blogpost.html', title=title, body=body)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        login_username_error = ""

        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            login_error = "No user by this username or password is incorrect"
            return render_template("login.html", login_error=login_error)

    return render_template('login.html')

    if request.method == 'GET':
        return render_template('login.html')



    
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username_error = ""
    password_error = ""
    verify_error = ""
    user_exists_error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if len(username) < 3 or len(username) > 20:
            flash('please enter a user name more then 3 characters')

            return render_template("signup.html", username_error=username_error)

        if " " in username:
            flash('Username cannot contain spaces')

            return render_template("signup.html", username_error=username_error)

        if len(password) < 3 or len(password) > 20:
            flash('Please enter a password between 3 and 50 chr')
            return render_template("signup.html", password_error=password_error)

        if " " in password:
            flash('password cannot have spaces')
            return render_template("signup.html", password_error=password_error)

        if password != verify:
            flash('passowords dont match')
            return render_template("signup.html", verify_error=verify_error)

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            user_exists_error = "Username already exists"
            return render_template("signup.html", user_exists_error=user_exists_error)

    return render_template('signup.html', username_error=username_error, password_error=password_error, verify_password_error=verify_password_error)


@app.route('/logout')
def logout():
    del session['username']
    flash("Logged Out")

    return redirect('/blog')



#@app.route('/', methods=['POST', 'GET'])
#def index():

    #users = User.query.all()
    #return render_template('index.html', users=users)



@app.route('/newpost', methods=['POST', 'GET'])
def new_blog():
    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        body = request.form['body']
        title = request.form['title']

        title_error = ''
        body_error = ''

        if not title:
            title_error = 'Please Enter a Title'
            title = ''
    
        if not body:
            body_error = 'Please Enter a New Blog Entry'
            body = ''
        
    
        if not title_error and not body_error:
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()   

            id = new_blog.id 
            
            return redirect ('/blogpost?id={0}'.format(id))
        
       

        
        else:
            
            return render_template('newpost.html', title_error=title_error,
            body_error=body_error, title=title, body=body)

        

    


    #blog_id = int(request.form['new_blog'])
    #blog = Blog.query.get(blog_id)
    #blog.completed = True
    #db.session.add(blog)
    #db.session.commit()

        


if __name__ == '__main__':
    app.run() 