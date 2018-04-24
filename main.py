from flask import Flask, request, redirect, render_template, session
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
    id = request.args.get("id")
    blog = Blog.query.get(id)
    title = blog.title
    body = blog.body


    return render_template('blogpost.html', title=title, body=body)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()



#@app.route('/signup', methods=['POST', 'GET'])
#def signup():
    #if request.method == 'POST':





@app.route







#def is_empty(text):
    #if text == "":
        #return True
    #else:
        #return False

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