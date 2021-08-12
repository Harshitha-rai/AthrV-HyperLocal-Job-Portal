from flask import Flask, render_template, request, url_for, flash, session, redirect
from validate_number import is_valid
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from twilio.rest import Client
import random
from db import *
import string
from datetime import datetime, timedelta
import smtplib
import re

app = Flask(__name__)
app.secret_key = 'athrv-hyper-local-job-portal'
login_manager = LoginManager()
login_manager.login_view = 'first'
login_manager.init_app(app)


@app.route('/')
def first():
    return render_template('index.html')


@app.route('/seeker_registration', methods=['GET', 'POST'])
def seeker_registration():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('re_pass')
        if check_seeker_email(email):
            if len(password1) and password1 == password2:
                session['details'] = [username, email, password1]
                return render_template('verify_otp.html')
            else:
                flash('Passwords do not match')
        else:
            flash('Email already exists!')
    return render_template('seeker_registration.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        if request.form['user_verify'] == 'Send OTP':
            mobile_number = request.form.get('mobile_number')
            address = request.form.get('address')
            details = [str(mobile_number), str(address)]
            if is_valid(mobile_number):
                val = send_otp(mobile_number)
                if val:
                    flash('OTP has been sent to your number')
                    return render_template('verify_otp.html', details=details)
            else:
                flash('Please enter a valid Mobile number')
        elif request.form['user_verify'] == 'Verify OTP':
            address = request.form.get('address')
            mobile_number = request.form.get('mobile_number')
            details = [str(mobile_number), str(address)]
            received_otp = request.form.get('otp')
            if 'response' in session:
                sent_otp = session['response']
                session.pop('response', None)
                if len(received_otp) and sent_otp == received_otp:
                    if 'details' in session:
                        user_data = session['details']
                        session.pop('details', None)
                        get1 = save_seeker_details(user_data[0], user_data[1], user_data[2])
                        seeker_id = get1[0][0]
                        save_seeker_address(seeker_id, address)
                        save_seeker_mobile(seeker_id, mobile_number)
                        return render_template('seeker_login.html')
                else:
                    flash('INVALID OTP')
                    return render_template('verify_otp.html', details=details)


def send_otp(number):
    otp = random.randint(1000, 9999)
    session['response'] = str(otp)
    auth_sid = "AC2c4686cd32685b947b296ea02f0ceaf3"
    auth_token = "5ca62b475eee5547a3a7697d985ee2a4"
    client = Client(auth_sid, auth_token)
    message = client.messages.create(
        from_='+19384440145',
        body='OTP for your number verification is ' + str(otp),
        to='+91' + number
    )
    if message.sid:
        return True
    else:
        False


@app.route('/creator_registration', methods=['GET', 'POST'])
def creator_registration():
    if request.method == 'POST':
        post_name = request.form['user_name']
        post_email = request.form['user_email']
        post_password = request.form['user_password']
        post_confirm_pass = request.form['u_confirm_password']
        if check_creator_email(post_email):
            if len(post_password) and post_password == post_confirm_pass:
                session['c_details'] = [post_name, post_email, post_password]
                return render_template("verify_otp2.html")
            else:
                flash("Passwords do not match")
        else:
            flash("This Email id already exists")
    return render_template("creator_registration.html")


@app.route("/verify_otp2", methods=['GET', 'POST'])
def verify_otp2():
    if request.method == 'POST':
        if request.form['user_send_otp'] == "Send OTP":
            otp_address = request.form['Address']
            otp_mbl = request.form['user_Mb_number']
            c_details = [str(otp_mbl), str(otp_address)]
            if is_valid(otp_mbl):
                val = send_otp(otp_mbl)
                if val:
                    flash('OTP has been sent to your number')
                    return render_template('verify_otp2.html', details=c_details)
            else:
                flash('Please enter a valid Mobile number')
        elif request.form['user_send_otp'] == 'Verify':
            otp_address = request.form['Address']
            otp_mbl = request.form['user_Mb_number']
            c_details = [str(otp_mbl), str(otp_address)]
            otp_otp = request.form['user_otp']
            if 'response' in session:
                sent_otp = session['response']
                session.pop('response', None)
                if len(otp_otp) and sent_otp == otp_otp:
                    if 'c_details' in session:
                        user_data = session['c_details']
                        session.pop('c_details', None)
                        get1 = save_creator_details(user_data[0], user_data[1], user_data[2])
                        creator_id = get1[0]
                        update_creator_details(creator_id, otp_mbl, otp_address)
                        return render_template('creator_login.html')
                else:
                    flash('INVALID OTP')
                    return render_template("verify_otp2.html", details=c_details)


@app.route('/seeker_education', methods=['GET', 'POST'])
@login_required
def seeker_education():
    if request.method == 'POST':
        college = request.form['college']
        degree = request.form['degree']
        field_study = request.form['field']
        start_year = request.form['start_year']
        end_year = request.form['end_year']
        user_mail = current_user.email
        seeker_id = get_seeker_id_from_mail(user_mail)
        save_seeker_education(seeker_id, college, degree, field_study, start_year, end_year)
    return render_template('add_seeker_education.html')


@app.route('/seeker_dashboard')
@login_required
def seeker_dashboard():
    return render_template('seeker_dashboard.html')


@app.route('/creator_dashboard')
@login_required
def creator_dashboard():
    return render_template('creator_dashboard.html')


@app.route('/seeker_login', methods=['GET', 'POST'])
def seeker_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = get_seeker(email)
        if user and user.check_password(password):
            login_user(user)
            session['user'] = 'seeker'
            return redirect(url_for('seeker_dashboard'))
        else:
            flash('Login Unsuccessful. Please check Email and password', 'danger')
    return render_template('seeker_login.html')


@app.route('/creator_login', methods=['GET', 'POST'])
def creator_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = get_creator(email)
        if user and user.check_password(password):
            login_user(user)
            session['user'] = 'creator'
            return redirect(url_for('creator_dashboard'))
        else:
            flash('Login Unsuccessful. Please check Email and password', 'danger')
    return render_template('creator_login.html')


@login_manager.user_loader
def load_user(email):
    if 'user' in session:
        value = session['user']
        # session.pop('user', None)
        if value == 'seeker':
            return get_seeker(email)
        else:
            return get_creator(email)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('first'))


@app.route('/creator_forgot', methods=['POST', 'GET'])
def creator_forgot():
    if request.method == 'POST':
        email = request.form.get("email")
        if creator_forgot_password(email) is None:
            flash("Please enter valid email ")
            return render_template("forgot_password_creator.html")
        else:
            N = 5
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=N))

            x = datetime.now()

            new_datetime = timedelta(minutes=30)
            date = x + new_datetime
            k = creator_update_token(token, date, email)
            try:
                with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login('athrvservices@gmail.com', 'Space@307#')
                    email = email;
                    subject = 'Reset your Password'
                    body = "Token for Your Reset Password is", {token}
                    msg = f'Subject: {subject}\n\n {body}'
                    smtp.sendmail('athrvservices@gmail.com', email, msg)
                    return render_template("creator_reset.html")
            except:
                flash('Mail not sent. Try again')
    return render_template('forgot_password_creator.html')


@app.route("/creator_reset",
           methods=["GET", "POST"])  # creator_reset.html is the page which checks the token of creator
def creator_reset():
    if request.method == "POST":
        token = request.form.get("token")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")
        if password != cpassword:
            flash("Passwords do not match")
            return render_template("creator_reset.html")
        else:
            x = datetime.now()
            s = creator_select_result(token)
            if s is None:
                flash("your token is invalid")
                return render_template("creator_reset.html")
            else:
                y = s[1] > x
                if y:
                    d = creator_update_password(password, s)
                else:
                    flash("token expired")
                    return render_template("forgot_password_creator.html")
                flash("Password Updated Successfully! Try to Login now")
                return redirect(url_for('creator_login'))
    return render_template("creator_reset.html")


@app.route('/seeker_forgot', methods=['POST', 'GET'])
def seeker_forgot():
    if request.method == 'POST':
        email = request.form.get('email')
        if seeker_forgot_password(email) is None:
            flash("Invalid Email Id")
            return render_template('forgot_password_seeker.html')
        else:
            # length of the string
            N = 5
            # with random.choices()
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=N))
            # result
            x = datetime.now()
            new_datetime = timedelta(minutes=15)
            date = x + new_datetime
            u = seeker_update_token(token, date, email)
            try:
                with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login('athrvservices@gmail.com', 'Space@307#')
                    email = email
                    subject = 'Reset your Password'
                    body = "Token for Your Reset Password is", {token}
                    msg = f'Subject: {subject}\n\n {body}'
                    smtp.sendmail('athrvservices@gmail.com', email, msg)
                    return render_template('seeker_reset.html')
            except:
                flash('Mail was not sent. Try again')
    return render_template('forgot_password_seeker.html')


@app.route('/seeker_reset', methods=["POST", "GET"])  # seeker_reset.html is the page which verifies the token of seeker
def seeker_reset():
    if request.method == 'POST':
        token = request.form.get('token')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if cpassword != password:
            flash("Entered Password should be same")
            return render_template('seeker_reset.html')
        else:
            x = datetime.now()
            t = seeker_select_result(token)
            if t is None:
                flash("Invalid Token")
                return render_template('seeker_reset.html')
            else:
                y = t[1] > x
                if y:
                    up = seeker_update_password(password, t)
                else:
                    flash("Token Expired")
                    return render_template('forgot_password_seeker.html')
                flash("Password Updated Successfully! Try to Login now")
                return redirect(url_for('seeker_login'))
    return render_template("seeker_reset.html")


@app.route('/seeker_profile_edit', methods=['GET', 'POST'])
def seeker_profile_edit():
    email = current_user.email
    seeker_id = get_seeker_id_from_mail(email)
    s_mobile = get_seeker_mobile(seeker_id)
    s_address = get_seeker_address(seeker_id)
    s_education = get_seeker_education(seeker_id)
    s_experience = get_experience(seeker_id)
    s_skills = get_skill(seeker_id)
    if request.method == 'POST':
        username = request.form.get('username')
        address = request.form.get('address')
        if username and address:
            update_seeker_profile(seeker_id, address, username)
            return redirect(url_for('seeker_dashboard'))
    return render_template('seeker_profile_edit.html', address=s_address, mobile=s_mobile, education=s_education, experience=s_experience, skills=s_skills)


# # Mokshith 26/05
# @app.route('/create_job', methods=['GET', 'POST'])
# def create_job():
#     if request.method == 'POST':
#         job_name = request.form.get('job_name')
#         job_description = request.form.get('job_description')
#         skills_required = request.form.get('skills_required')
#         salary = request.form.get('salary')
#         location = request.form.get('location')
#         vacancy = int(request.form.get('vacancy'))
#         experience = request.form.get('experience')
#         time_limit = request.form.get('time_limit')
#         contact_details = request.form.get('contact_details')
#         scale = request.form.get('scale')
#         creator_mail = current_user.email

#         create_new_job(creator_mail, job_name, job_description, skills_required, salary, location, vacancy, experience,
#                        contact_details, scale, time_limit)
#     return render_template('create_job.html')


# @app.route('/edit_create_job', methods=['GET', 'POST'])
# def edit_create_job():
#     job_id = 105  # integrate this
#     data = edit_create_new_job(job_id)  # integrate this
#     z = []
#     for x in data:
#         z.append(x)

#     if request.method == 'POST':
#         job_name = request.form.get('job_name')
#         job_description = request.form.get('job_description')
#         skills_required = request.form.get('skills_required')
#         salary = request.form.get('salary')
#         location = request.form.get('location')
#         vacancy = int(request.form.get('vacancy'))
#         experience = request.form.get('experience')
#         time_limit = request.form.get('time_limit')
#         contact_details = request.form.get('contact_details')
#         scale = request.form.get('scale')

#         if time_limit == "":  # if time_limit== null   then display messagebox to alert user
#             print("succcccesssssssssssssssssssssssssssssss")
#             time_limit = z[7]
#         print(skills_required)
#         print(job_description)

#         creator_mail = current_user.email
#         edit_create_new_job2(creator_mail, job_name, job_description, skills_required, salary, location, vacancy,
#                              experience, contact_details, scale, time_limit)

#         data = edit_create_new_job(job_id)  # integrate this
#         z = []
#         for x in data:
#             z.append(x)

#     return render_template('edit_create_job.html', job_name=z[0], job_description=z[1], skills_required=z[2],
#                            salary=z[3], location=z[4], vacancy=z[5], experience=z[6], time_limit=z[7],
#                            contact_details=z[8], scale=z[9])


@app.route('/recomendation_list', methods=['GET', 'POST'])
def recomendation_list():  # recommendation based on skills,location,deadline,applied or not
    seeker_mail = current_user.email
    id_of_seeker = get_seeker_id_from_mail(seeker_mail)

    data_from_database = recommend_list_database1(id_of_seeker)
    data = data_from_database[0]  # skills from seeker_skils
    seeker_location = data_from_database[1]  # location from seeker_location
    data1 = data_from_database[2]  # * from posted jobs
    status_check = data_from_database[3]  # * from applied_jobs
    xy = ""
    for x in data:
        x = str(xy) + str(x)
    b = []
    for ij in range(1, len(x), 1):
        if x[ij] == "\t":  # skills r collected by avoiding the space
            forget = "forget"
        else:
            b.append(x[ij])
    b = "".join(b)
    z = re.split("\s|(?<!\d)[,](?!\d)", str(b))  # skills r collected by avoiding the ,
    for abc in z:
        if abc == "":
            z.remove(abc)  # final skills r collected here

    job_ids_of_display = []
    status1 = []

    for x in z:

        for y in data1:
            y1 = str(y)
            if x in y1:
                if seeker_location[0].lower() == y[6].lower():

                    import datetime  # datetime verification so that present date is less than deadline
                    datetime_verify = datetime.datetime.today().replace(microsecond=0)
                    if datetime_verify > y[9]:
                        forget = "forget"
                    else:

                        for status in status_check:
                            status1.append(status[0])

                        job_ids_of_display.append(y[0])

    status1 = list(set(status1))
    status2 = []
    for x in job_ids_of_display:
        if x in status1:
            forget = "forget"
        else:
            status2.append(x)

    job_ids_of_display = list(dict.fromkeys(status2))
    # print(len(job_ids_of_display))  # can add if len is less than 10 display all in that skill or place

    value = recommend_list_database2(job_ids_of_display)

    return render_template("recomendation_list.html", posted_jobs=value)


@app.route('/recomendation_list/<job_id>', methods=['GET', 'POST'])
def recomended_select_list(job_id):
    creator_mail = current_user.email
    id_of_seeker = get_seeker_id_from_mail(creator_mail)

    recommend_list_database3(job_id, id_of_seeker)

    return redirect(url_for('recomendation_list'))


# Sahana
@app.route("/addskill")
def addskill():
    email = current_user.email
    s_id = get_seeker_id_from_mail(email)
    global back
    back = get_skill(s_id)  # to get the skills
    print(back)
    if (back):
        return render_template('view_skills.html', names=back)
    else:
        return render_template("add_skills.html")
    # to open remove experience page
    '''back2 = get_experience(s_id)  # to get the skills
    print(back2)
    if(back2):
      return render_template('r_experience.html', names=back2)
    else:
        return render_template("add_experience.html")'''


@app.route("/add_skills", methods=["GET", "POST"])
def add_seeker_skill():
    if request.method == "POST":
        email = current_user.email
        s_id = get_seeker_id_from_mail(email)  # to get the id using email
        skill = request.form["add_skill"]
        value2 = add_skill(s_id, skill)  # to add the skills
        if value2 == 0:
            b1 = get_skill(s_id)
            return render_template('view_skills.html', names=b1)
        else:
            return render_template('add_skills.html', error=value2)


@app.route("/remove_skills", methods=["GET", "POST"])
def remove_seeker_skill():
    if request.method == "POST":
        email = current_user.email
        s_id = get_seeker_id_from_mail(email)  # to get the id
        if request.form["r_skill"] == "Add_skill":
            return render_template('add_skills.html')
        else:
            name = request.form["r_skill"]
            print(
                name)  # .getlist("Remove_skill", type=None) # to get all the values that are selected in remove skill option
            remove_skill(s_id, name)  # to remove the skills
            b1 = get_skill(s_id)
            print(b1)
            if (b1):
                return render_template('view_skills.html', names=b1)
            else:
                return render_template('add_skills.html')


# Meghana
@app.route("/user_experience")
def user_experience():
    email = current_user.email
    s_id = get_seeker_id_from_mail(email)
    back2 = get_experience(s_id)  # to get the added exp
    if (back2):
        return render_template('r_experience.html', names=back2)
    else:
        return render_template("add_experience.html")


@app.route("/add_experience", methods=["GET", "POST"])
def add_experience():
    if request.method == "POST":
        email = current_user.email
        s_id = get_seeker_id_from_mail(email)  # to get the id using email
        experience = request.form["add_Experience"]
        value2 = adding_experience(s_id, experience)  # to add the skills
        if value2 == 0:
            b2 = get_experience(s_id)
            return render_template('r_experience.html', names=b2)
        else:
            flash(value2)
            return render_template('add_experience.html')


@app.route("/remove_experience", methods=["GET", "POST"])
def remove_experience():
    if request.method == "POST":
        email = current_user.email
        s_id = get_seeker_id_from_mail(email)  # to get the id
        if request.form["r_experience"] == "Add_experience":
            return render_template('add_experience.html')
        else:
            name2 = request.form["r_experience"]
            removing_experience(s_id, name2)  # to remove the skills
            b2 = get_experience(s_id)
            if (b2):
                return render_template('r_experience.html', names=b2)
            else:
                return render_template('add_experience.html')


# mokshith2
@app.route('/my_current_job')
def my_current_job():
    post_email = current_user.email
    # post_email = "p1@p.com"
    get2 = my_current_job_db(post_email)

    return render_template("seekerm_current_job.html", posted_jobs1=get2)


@app.route('/rejected_jobs')
def rejected_jobs():
    # post_email = "p1@p.com"
    post_email = current_user.email
    get3 = rejected_jobs_db(post_email)
    return render_template("seekerm_rejected_jobs.html", posted_jobs2=get3)


@app.route('/applied_jobs')
def applied_jobs():
    # post_email = "p1@p.com"
    post_email = current_user.email
    get4 = applied_jobs_db(post_email)

    return render_template("seekerm_applied_jobs.html", posted_jobs3=get4)


@app.route('/applied_job_cancel/<job_id>', methods=['GET', 'POST'])
def applied_job_cancel(job_id):
    # post_email = "p1@p.com"
    post_email = current_user.email
    app_job_cancel = applied_job_cancel_db(job_id, post_email)
    return redirect(url_for('applied_jobs'))


@app.route('/approve_jobs')
def approve_jobs():
    # post_email = "p1@p.com"
    post_email = current_user.email
    get5 = approve_jobs_db(post_email)
    return render_template("seekerm_approve_jobs.html", posted_jobs4=get5)


@app.route('/approve_job_cancel/<job_id>', methods=['GET', 'POST'])
def approve_job_cancel(job_id):  # not working. do check
    # post_email = "p1@p.com"
    post_email = current_user.email
    app_db = approve_job_cancel_db(job_id, post_email)

    return redirect(url_for('approve_jobs'))


@app.route('/approve_job_approve/<job_id>', methods=['GET', 'POST'])
def approve_job_approve(job_id):
    # post_email = "p1@p.com"
    post_email = current_user.email
    approve = approve_job_approve_db(job_id, post_email)
    return redirect(url_for('approve_jobs'))


@app.route('/completed_job', methods=["POST", "GET"])
def completed_job():
    print("start")
    # post_email = "p1@p.com"
    post_email = current_user.email
    if request.method == 'POST':
        creator_rating = request.form.get("creator_rating")

        job_id = request.form["submit_button"]
        # print("job_id_is",job_id)
        job_id = list(job_id.split(','))
        job_id = job_id[0]

        # print("the job id issssssssss",job_id)
        # seeker_id = 7                                                 #########integrate this

        print(job_id, creator_rating)
        completed_job2_db(job_id, creator_rating, post_email)

        flash("Thanks for the Rating")
        # return redirect(url_for('completed_job'))

    # post_email = "p1@p.com"

    get6 = completed_job1_db(post_email)

    get61 = []
    for x in get6:
        get61.append(x)
        print(x)
    get6 = get61

    return render_template("seekerm_completed_job.html", posted_jobs6=get6)



@app.route('/create_job/<string:email>', methods=['GET', 'POST'])
def create_job(email):
    if request.method == 'POST':
        job_name = request.form.get('job_name')
        job_description = request.form.get('job_description')
        skills_required = request.form.get('skills_required')
        salary = request.form.get('salary')
        location = request.form.get('location')
        vacancy = int(request.form.get('vacancy'))
        experience = request.form.get('experience')
        time_limit = request.form.get('time_limit')
        contact_details = request.form.get('contact_details')
        scale = request.form.get('scale')
        creator_mail = current_user.email

        create_new_job(creator_mail, job_name, job_description, skills_required, salary, location, vacancy, experience,
                       contact_details, scale, time_limit)
    return render_template('create_job.html')


@app.route('/edit_create_job/<string:email>', methods=['GET', 'POST'])
def edit_display_job(email):
    #print(email)
    creator_id = get_creator_id(email)
    #print("creator_id", creator_id)
    display_j_edit = get_all_job_for_creator(creator_id)
    #print(display_j_edit)
    return render_template("disp_for_edit_job.html", disp_j_crea=display_j_edit)


@app.route('/edit_create_job/edit_create_job_second', methods=['GET', 'POST'])
def edit_display_job_second():
    if request.method == "POST":
        job_id = request.form['edit_job']
        print(job_id)
        '''job = get_creator_id(email)
        job_ = get_job_id(job)
        job_id = int(job_[0])
        print(int(job_[0]), "jobid")'''

        data = edit_create_new_job(job_id)
        z = []
        for x in data:
            z.append(x)
        return render_template('edit_create_job.html', job_name=z[0], job_description=z[1], skills_required=z[2],
                               salary=z[3], location=z[4], vacancy=z[5], experience=z[6], time_limit=z[7],
                               contact_details=z[8], scale=z[9], job_id=job_id)


@app.route('/edit_create_job/edit_job_display', methods=['GET', 'POST'])
def edit_create_job():
    if request.method == 'POST':
        job_id = request.form.get('submit_button')
        print(job_id)
        job_name = request.form.get('job_name')
        job_description = request.form.get('job_description')
        skills_required = request.form.get('skills_required')
        salary = request.form.get('salary')
        location = request.form.get('location')
        vacancy = int(request.form.get('vacancy'))
        experience = request.form.get('experience')
        time_limit = request.form.get('time_limit')
        contact_details = request.form.get('contact_details')
        scale = request.form.get('scale')

        if time_limit == "":  # if time_limit== null   then display messagebox to alert user
            print("succcccesssssssssssssssssssssssssssssss")
            time_limit = z[7]
        print(skills_required)
        print(job_description)

        creator_mail = current_user.email
        print("creator_email", creator_mail)
        edit_create_new_job2(creator_mail, job_id, job_name, job_description, skills_required, salary, location,
                             vacancy,
                             experience, contact_details, scale, time_limit)

        '''data = edit_create_new_job(job_id)  # integrate this
        z = []
        for x in data:
            z.append(x)

        return render_template('edit_create_job.html', job_name=z[0], job_description=z[1], skills_required=z[2],
                           salary=z[3], location=z[4], vacancy=z[5], experience=z[6], time_limit=z[7],
                           contact_details=z[8], scale=z[9])'''

        return redirect(url_for("edit_display_job", email=creator_mail))


def display_all(job, status):  # to display the seekers list with their experience and skills
    #print(job)
    job = int(job)
    #print("id is display", job)
    if status == "Completed":
        output = get_seeker_id_for_rating(job)
    else:
        output = get_seeker_id_based_on_status(int(job), status)
    #print(output)
    #print(output, "output in pending")
    if output:
        list1 = []  # to store seeker_basic_details
        list2 = []  # to store seeker_skills
        list3 = []  # to store seeker_experience

        d = ["None"]
        for k in output:  # k is seeker_id
            m = {}
            #print(k)
            # cur.execute("select email, mobile_number, name from seeker_details where seeker_id= '%d'" % (int(k[0])))
            if status == "Completed":  # here we need to check for rating conditions(whether rating is already been
                # given or not)
                a = get_seeker_for_rating(int(k[0]), job)
                #print(a)
            else:
                a = get_seeker_basic_details(int(k[0]))  # cur.fetchall()
            if a:
                m["details"] = a[0]
                # cur.execute("select skills from seeker_skils where seeker_id= '%d'" % (int(k[0])))
                b = get_seeker_skill(int(k[0]))  # (cur.fetchall())
                #print("skill is", b)
                if b:
                    # print("yes")
                    list2.clear()
                    for j in b:
                        list2.append(j[0])
                        #print("list2 is ", list2)
                    m["skills"] = list2
                    #print("done", m)
                else:
                    #print("else part")
                    m["skills"] = d
                #print("done m is", m)
                # cur.execute("select experience from seeker_experience where seeker_id= '%d'" % (int(k[0])))
                c = get_seeker_exp(int(k[0]))  # cur.fetchall()
                #print("exp is", c)
                #print("done m is", m)
                list3.clear()
                if c:
                    for j in c:
                        list3.append(j[0])
                    m["experience"] = list3
                else:

                    m["experience"] = d
                m["Job_id"] = str(job)
                m["seeker_id"] = str(k[0])
                list1.append(m)
                #print("list1 is", list1)
                #print("m is", m)
                del m
        #print(list1)
        return list1
    else:
        return []


@app.route('/creator_disp_job/<string:all_in_1>/<string:creator_email>', methods=['GET', 'POST'])
def display_jobs(all_in_1, creator_email):  # this is to display the job for creator #all_in_1 used to indicate
    # whether p/A/f/completed button is clicked
    x = all_in_1
    #print(x, creator_email)
    id = get_creator_id(creator_email)
    if x == "AorR":
        '''cur.execute(
            "select a.* from posted_jobs a where a.creator_id='%d' and a.job_id in(select job_id from applied_jobs "
            "where status='A' and status_of_the_project IS NULL )" % ( 
                id))'''
        status = 'A'
        pending = get_jobs_based_on_status(id, status)  # cur.fetchall()
        #print(pending)
        if pending:
            return render_template("creator_disp_job.html", pen_jb=pending)
        else:
            flash("No matching Results")
            return render_template("creator_disp_job.html")
    elif x == "Approve":
        status = 'AP'
        approved = get_jobs_based_on_status(id, status)
        #print(approved)
        if approved:
            return render_template("creator_disp_job.html", appr_jb=approved)
        else:
            flash("No matching Results")
            return render_template("creator_disp_job.html")
    elif x == "Finalise":
        status = 'Final'
        finalised = get_jobs_based_on_status(id, status)  # cur.fetchall()
        #print(finalised)
        if finalised:
            return render_template("creator_disp_job.html", fina_jb=finalised)
        else:
            flash("No matching Results")
            return render_template("creator_disp_job.html")
    else:
        status = 'Completed'
        completed = get_jobs_based_on_status_of_proj(id, status)  # cur.fetchall()
        #print(completed)
        if completed:
            return render_template("creator_disp_job.html", comp_jb=completed)
        else:
            flash("No matching Results")
            return render_template("creator_disp_job.html")


@app.route('/creator_disp_job/Approve/approved_application', methods=['GET', 'POST'])
def appr_application():  # if he wants to view the candidates whom he accepted
    if request.method == "POST":
        job_id = request.form['Apply_job']
        m = list(job_id.split(","))
        #print("job id is", job_id)
        if m[1] == "22":  # if he wants to delete job
            id_d = int(m[0])
            #print("yes delete job", id_d)
            delete_job_for_creator(int(id_d))
            #print(current_user.email, "is")
            mail = current_user.email
            return redirect(url_for("display_jobs", all_in_1="Approve", creator_email=mail))

        else:  # if he wants to view candidates
            job = m[0]
            g = display_all(job, "AP")  # to view with skills and experience
            if g:
                return render_template("disp_see_to_cre.html", candidates=g)
            else:
                flash("No Results")
                return render_template("disp_see_to_cre.html")


@app.route('/creator_disp_job/Completed/completed_application', methods=['GET', 'POST'])
def completed_application():  ##if creator wants to rate candidates, this will execute
    if request.method == "POST":
        job_id = request.form['rate_job']
        job_id2 = int(job_id)
        #print("job_id is", job_id2)
        rating_see = display_all(job_id2, "Completed")
        #print(rating_see, "rating is")
        if not rating_see:
            mail = current_user.email
            #print("mail is", mail)
            flash("No more candidates to rate")
            return redirect(url_for("display_jobs", all_in_1="Completed", creator_email=mail))
        else:
            return render_template("disp_see_to_cre.html", comp_candidates=rating_see)


@app.route('/creator_disp_job/Finalise/finalized_application', methods=['GET', 'POST'])
def final_application():  # if creator wants to view finalised candidates this wil execute
    if request.method == "POST":
        job_id = request.form['Apply_job']
        m = list(job_id.split(","))
        #print("job id is", job_id)
        conn = psycopg2.connect(
            'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35'
            '-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
        cur = conn.cursor()
        if m[1] == "22":  ####to identify whether delete or view app button is pressed (if delete, m[1]=22 else 33)
            id_d = int(m[0])
            #print("yes delete job", id_d)
            delete_job_for_creator(int(id_d))
            #print(current_user.email, "is")
            mail = current_user.email
            return redirect(url_for("display_jobs", all_in_1="Finalise", creator_email=mail))

        else:
            job = m[0]
            g = display_all(job, "Final")
            if g:
                return render_template("disp_see_to_cre.html", candidates=g)
            else:
                flash("No Results")
                return render_template("disp_see_to_cre.html")


@app.route('/creator_disp_job/AorR/pending_application', methods=['GET', 'POST'])
def pending_application():  ##if creator wants to accept/reject candidates, this will execute
    if request.method == "POST":
        job_id = request.form['Apply_job']
        m = list(job_id.split(","))
        #print("job id is", job_id)
        '''conn = psycopg2.connect(
            'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35'
            '-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv') 
        cur = conn.cursor()'''
        if m[1] == "22":  ####to identify whether delete or view app button is pressed (if delete, m[1]=22 else 33)
            id_d = int(m[0])
            #print("yes delete job", id_d)
            delete_job_for_creator(int(id_d))
            #print(current_user.email, "is")
            mail = current_user.email
            return redirect(url_for("display_jobs", all_in_1="AorR", creator_email=mail))


        else:
            job = m[0]
            g = display_all(job, "A")
            if g:
                return render_template("disp_see_to_cre.html", applications=g)
            else:
                flash("No Results")
                return render_template("disp_see_to_cre.html")


@app.route('/update/<string:jobandseek>', methods=['POST', 'GET'])  # <string:job_id><string:seeker_id>
def fetch(jobandseek):  # if the creator wants to accept the candidate
    #print("yes update")
    #print(jobandseek)
    list6 = list(jobandseek.split(','))
    #print("list6 is", list6)
    job_id = int(list6[0])
    seeker_id = int(list6[1])
    '''conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()'''
    status = "AP"
    update_status_for_creator(status, job_id, seeker_id)
    #print("table updated...")
    '''cur.execute("UPDATE applied_jobs SET status=%s WHERE job_id=%s AND seeker_id=%s", (status, job_id, seeker_id))

    conn.commit()'''
    g = display_all(job_id, "A")
    if not g:
        flash("No Results")
        return render_template("disp_see_to_cre.html")
    else:
        return render_template("disp_see_to_cre.html", applications=g)


@app.route("/delete/<string:job_id><string:seeker_id>", methods=['POST', 'GET'])
def cancel(job_id, seeker_id):  # if the creator wants to reject the candidates
    #print("yes cancel")
    '''conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv') 
    cur = conn.cursor()'''
    status = "R"
    update_status_for_creator(status, job_id, seeker_id)
    '''cur.execute("UPDATE applied_jobs SET status=%s WHERE job_id=%s AND seeker_id=%s ", (status, job_id, seeker_id))
    print("table updated...")
    conn.commit()'''
    g = display_all(job_id, "A")
    if not g:
        flash("No Results")
        return render_template("disp_see_to_cre.html")
    else:
        return render_template("disp_see_to_cre.html", applications=g)


@app.route('/update_project/<string:email>', methods=['GET', 'POST'])
def update_project(email):  # if the creator clicks update project status
    id = get_creator_id(email)
    m = get_project_status(id)
    #print(m, "m is")
    if m:
        return render_template("update_project_status.html", email_r=email, job_update=m)
    else:
        flash("No matching Results")
        return render_template('update_project_status.html')


@app.route('/update_project_status/<int:job_id>/<string:email>', methods=['GET', 'POST'])
def update_project_status(job_id, email):  # if the creator wants to update the status as complted
    up_project_status(job_id)
    return redirect(url_for("update_project", email=email))


@app.route('/creator_disp_job/Completed/rate_creator', methods=["POST", "GET"])  # this works when creator clicks rate
def rate():
    #print("ha here")
    if request.method == 'POST':
        value1 = request.form["rate_button"]
        #print(value1, "value1 is")
        value2 = list(value1.split(','))
        seeker_id = value2[0]  # request.form.get("seeker_id")
        #print(seeker_id)
        job_id = value2[1]  # request.form.get("job_id")
        #print(job_id)
        creator_rating = request.form.get("creator_rating")
        #print(creator_rating, "creator_rating is")
        # cur.execute("SELECT creator_rating FROM ratings WHERE job_id=%s and seeker_id=%s", [
        # job_id, seeker_id])
        s = creator_side_get_rating(job_id, seeker_id)  # cur.fetchone()
        #print(s)
        if s is None:
            creator_side_inser_rating(job_id, seeker_id, creator_rating)
            #print("inserted")
        else:
            creator_side_update_rating(creator_rating, job_id, seeker_id)
            #print("Table updated....")
        # cur.execute("SELECT * FROM ratings")
        a = creator_side_getall_rating  # cur.fetchone()
        #print(a)
        # myconn.commit()
        rating_see = display_all(job_id, "Completed")  # to get the remaining seeker for rating
        if not rating_see:
            mail = current_user.email
            #print("mail is", mail)
            flash("No more candidates to rate")
            return redirect(url_for("display_jobs", all_in_1="Completed", creator_email=mail))  # to go back to the
            # completed job page if no more seekers for rating
        else:
            flash("Thanks for the Rating")
            return render_template("disp_see_to_cre.html", comp_candidates=rating_see)  # to display the remaining
            # seekers for rating


@app.route("/creator_profile_edit")
def homie():
    email = current_user.email
    a = profile_in(email)
    return render_template("creator_profile_edit.html",details=a)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == "POST":
        name = request.form['name']
        #print(name)
        address = request.form['address']
        #print(address)
        email = current_user.email
        a = profile_in(email)
        print(a)
        h = profile_id(name, address, email)
        flash("profile updated successfully")
        return render_template("creator_dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)
