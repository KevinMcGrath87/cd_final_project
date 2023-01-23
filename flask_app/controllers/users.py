from flask_app.__init__ import app
from flask import render_template, request, flash, redirect, session, url_for
from flask_app.models import user, zine as zineModel
from flask_app.config.utils import UPLOAD_FOLDER,ALLOWED_EXTENSIONS
import os
import random



@app.route('/', methods =['GET'])
def home():
    if 'user' in session:
        return(redirect('/profile'))
    return(render_template('home.html'))
    # get list of zine id's into an array and randomly select one via randint.



@app.route('/login_register')
def loginRegister():
    return(render_template('login_registration.html'))

@app.route('/register', methods = ['POST'])
def register():
    data = request.form.to_dict()
    if user.User.validate(data):
        currentUser = user.User.insertUser(data)
        session['user'] = currentUser
        print(currentUser)
        return(redirect('/profile'))
    else:
        return(redirect('/'))

@app.route('/login', methods = ['POST'])
def login():
    data = request.form.to_dict()
    print(data)
    if user.User.validate_login(data):
        print("validation passed")
        currentUser = user.User.getUserByEmail(data['email'])
        print(currentUser.username)
        session['user'] = currentUser.id
        return(redirect('/profile'))
    else:
        return(redirect('/'))

@app.route('/logout')
def logout():
    session.clear()
    return(redirect('/'))


@app.route('/profile')
def profile():
    if 'user' in session:
        currentUser = user.User.get_user_with_zines(session['user'])
        return(render_template('profile.html',currentUser = currentUser ))
    else: return(redirect('/'))


@app.route('/view', methods = ['GET','POST'])
def view():
    data = request.form.to_dict()
    zineId = data['zineId']
    print(data)
    page = 0
    return(redirect(f'/viewpage/{zineId}/{page}'))


@app.route('/viewpage/<int:zineId>/<int:currentPage>')
def viewpage(zineId, currentPage):
    zineData = zineModel.Zine.get_zine(zineId)
    zineToView = zineModel.Zine(zineModel.Zine.get_by_id(zineId)[0])
    zinePath = zineData[0]['path']
    zineTitle = zineData[0]['title']
    # should print path of zine
    print(os.listdir(zinePath))
    fileArray = os.listdir(zinePath)
    if fileArray:
    # fileArray.reverse()
        return render_template("view.html",fileArray = fileArray, zinePath = zinePath, currentPage = currentPage, zineId = zineId, zineTitle=zineTitle, zineToView = zineToView)
    else:
        return(redirect('/profile'))

@app.route('/arrowClick/<int:currentPage>/<int:length>/<int:zineId>',methods = ['POST'])
def arrowClick(currentPage, length, zineId):
    data = request.form.to_dict()
    if data['click'] == 'down' and currentPage > 0:
        currentPage -= 1
    if data['click']=='up' and currentPage < length -1:
        currentPage += 1 
    # return(redirect("/viewpage",currentPage= currentPage, zineId = zineId))
# should it be a redirect?
    return(redirect(url_for('.viewpage', currentPage = currentPage, zineId = zineId)))


@app.route('/search', methods = ['GET'])
def search():
    if 'userSearch' in session:
        data = session['userSearch']
        print(data)
        users = user.User.user_search(data)
        print(users)
        session.pop('userSearch')
        return(render_template('search.html', users = users))
    if 'zineSearch' in session:
        data = session['zineSearch']
        users = ''
        return(render_template('search.html', users = users))
    else: return render_template('search.html')

@app.route('/search/people', methods =['POST'])
def search_users():
    if request.method == 'POST':
        session['userSearch'] = request.form['userSearch']
        return(redirect('/search'))

