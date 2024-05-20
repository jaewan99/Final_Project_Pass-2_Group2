from flask import Flask,redirect
from flask import render_template
from flask import request
import database as db
import authentication
import logging
from flask import session
from bson.json_util import loads, dumps
from flask import make_response

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'


logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
    courses = db.get_courses()
    return render_template('index.html', page="Index", courses=courses)

@app.route('/coursedetails')
def coursedetails():
    courses = db.get_courses()

    code = request.args.get('code', '')
    subcourses = db.get_subcourses(int(code))

    return render_template('coursedetails.html', code=code, courses=courses,subcourses= subcourses)

@app.route('/subcoursedetails')
def subcoursedetails():
    subcode = request.args.get('code', '')
    subcourse = db.get_subcourse(int(subcode))

    subcourse_topics = db.get_subcourse_topics(int(subcode))
    subcourse_topics_list = subcourse_topics[0]
    subcourse_topics_head = subcourse_topics[1][0]['maintopics']

    return render_template('subcoursedetails.html', subcourse=subcourse, subcourse_topics_list= subcourse_topics_list, subcourse_topics_head=subcourse_topics_head)


@app.route('/subcoursetopic')
def subcoursetopic():
    subtopiccode = request.args.get('subtopiccode', '')
    subcourse_topic = db.get_subcourse_topic(int(subtopiccode))
    if session.get("user") is not None:
        username = (session["user"]["username"])
        usercomments = db.get_user_comments_with_subtopiccode(username,subtopiccode)
        print(usercomments)
        return render_template('subcoursetopic.html', subcourse_topic=subcourse_topic, usercomments=usercomments)


    return render_template('subcoursetopic.html', subcourse_topic=subcourse_topic)



@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user, errorMessage = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return render_template('login.html', errorMessage=errorMessage)

@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect('/')

@app.route('/changepassword')
def changepassword():
    return render_template('changepassword.html')

@app.route('/userchangepassword', methods = ['POST'])
def userchangepassword():
    stype = request.form.get("stype")
    if stype == "Update":
        oldpwd = request.form.get("pwd")
        newpwd = request.form.get("pwdnew")
        renewpwd = request.form.get("pwdnewre")
        if oldpwd == db.get_user_password(session["user"]["username"]):
            if newpwd == renewpwd:
                db.change_user_password(newpwd)
                return redirect('/')
            else:
                return redirect('/changepassword')
    return redirect('/changepassword')

@app.route('/createaccount')
def createaccount():
    return render_template('createaccount.html')


@app.route('/usercreateaccount', methods = ['POST'])
def usercreateaccount():
    stype = request.form.get("stype")
    if stype == "Create":
        username = request.form.get("email")
        password = request.form.get("pwd")
        repassword = request.form.get("repwd")
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        if password == repassword:
            print('createaccount')
            db.create_user(username, password, first_name, last_name)
            return redirect('/login')
        else:
            return redirect('/createaccount')
    return redirect('/createaccount')

@app.route('/usercomment')
def usercomment():
    username = (session["user"]["username"])
    usercomments = db.get_user_comments(username)
    return render_template('usercomment.html', usercomments=usercomments)

@app.route('/addusercomment', methods = ['POST'])
def addusercomment():
    username = (session["user"]["username"])
    comment = request.form.get('comment')
    subtopiccode = request.form.get('subtopiccode')
    db.add_user_comment(username, comment, subtopiccode)
    return redirect('/subcoursetopic?subtopiccode='+subtopiccode)