from flask import url_for, render_template, redirect, flash, request
from rrumble import app, db, guard, osyrus
from rrumble.forms import SignUp, Login, MakeRequest, PicMod, UpdateProf
from rrumble.models import User, Task
from flask_login import login_user, logout_user, current_user
from rrumble.otherfuncs import photo_update


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/serv', methods=['GET', 'POST'])
def serv():
    form = MakeRequest()
    if form.validate_on_submit():
        new_task = Task(guest_name=form.name.data, guest_email=form.email.data, guest_tel=form.telephone.data, subject=form.subject.data, guest_msg=form.text.data)
        db.session.add(new_task)
        db.session.commit()
        flash('your message has been sent', 'info')
        return redirect(url_for('serv'))
    return render_template('serv.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form=Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and guard.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('invalid credentials. check and try again', 'danger')
    return render_template('login.html', title='Login', form=form, current_user=current_user)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=SignUp()
    if form.validate_on_submit():
        pw_hsh = guard.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(name=form.name.data, email=form.email.data, password=pw_hsh)
        db.session.add(new_user)
        db.session.commit()
        flash('new user successfully added', 'success')
        logout_user()
        return redirect(url_for('login'))
    user_prof = url_for('static', filename='media/profphot/'+ current_user.prof_photo)
    return render_template('signup.html', title='New User', form=form, user_prof = user_prof)


@app.route('/usaccnt', methods=['GET', 'POST'])
def usaccnt():
    user_prof = url_for('static', filename='media/profphot/'+ current_user.prof_photo)
    return render_template('account.html', user_prof=user_prof, title='User Profile')

@app.route('/updtuser', methods=['GET', 'POST'])
def updtuser():
    form = UpdateProf()
    if form.validate_on_submit():
        if form.photo.data:
            new_phot = photo_update(form.photo.data)
            current_user.prof_photo = new_phot
        current_user.email = form.email.data
        current_user.post = form.post.data
        current_user.expertise = form.expertise.data
        current_user.xpduration = form.durat.data
        db.session.commit()
        flash("user's details were successfully updated", 'success')
        return redirect(url_for('usaccnt'))
    elif request.method == 'GET':
        form.post.data = current_user.post
        form.email.data = current_user.email
        form.expertise.data = current_user.expertise
        form.durat.data = current_user.xpduration
    user_prof = url_for('static', filename='media/profphot/'+ current_user.prof_photo)
    return render_template('updtuser.html', form = form, user_prof=user_prof, title='Update Profile')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/requests', methods=['GET', 'POST'])
def requests():
    user_prof = url_for('static', filename='media/profphot/'+ current_user.prof_photo)
    return render_template('requests.html', user_prof=user_prof)


@app.route('/viewreq/(int:id)', methods=['GET', 'POST'])
def viewreq(id):
    request = Task.query.get_or_404(id)
    user_prof = url_for('static', filename='media/profphot/'+ current_user.prof_photo)
    return render_template('viewreq.html', request=request, user_prof=user_prof)


