import psycopg2
from seeker import Seeker
from creator import Creator

database_link = 'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv'


def save_seeker_details(username, email, password):
    connection = psycopg2.connect('postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO seeker_details ( name, email, password) VALUES (%s, %s, %s)',
                       (username, email, password))
        connection.commit()
        cursor.execute("select seeker_id from seeker_details where email ='%s'" % email)
        get1 = cursor.fetchall()
        return get1


def save_creator_details(username, email, password):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    add1 = "insert into creator_details(  email , password , name ) values('%s','%s','%s')" % \
           (email, password, username)
    curr.execute(add1)
    con.commit()
    curr.execute("select creator_id from creator_details where email ='%s'" % email)
    get1 = curr.fetchall()
    return get1


def update_creator_details(creator_id, mobile, address):
    con2 = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur2 = con2.cursor()
    add3 = "update creator_details set mobile_number='%s',address='%s' where creator_id='%d'" %\
           (mobile, address, int(creator_id[0]))
    cur2.execute(add3)
    con2.commit()
    con2.close()


def check_seeker_email(email):
    connection = psycopg2.connect('postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    with connection.cursor() as cursor:
        cursor.execute("SELECT FROM seeker_details where email = '%s'" %email)
        records = cursor.fetchall()
        if not records:
            return True
        else:
            False


def check_creator_email(email):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    add = "Select * from creator_details where email='%s'" %email
    curr.execute(add)
    records = curr.fetchall()
    if not records:
        return True
    else:
        False


def save_seeker_education(seeker_id, college, degree, field, start_year, end_year):
    connection = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO seeker_education ( seeker_id, college_name, degree, field, start_year, end_year) VALUES (%s, %s, %s, %s, %s, %s)",
                        (int(seeker_id), college, degree, field, start_year, end_year))
        connection.commit()
        connection.close()


def get_seeker_id_from_mail(email):
    connection = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    with connection.cursor() as cursor:
        cursor.execute("select seeker_id from seeker_details where email ='%s'" % email)
        seeker_id = cursor.fetchall()
        if seeker_id:
            return seeker_id[0][0]


def get_seeker(email):
    connection = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM seeker_details WHERE  email='%s'" % email)
        user_data = cursor.fetchone()
        return Seeker(user_data[4], user_data[1], user_data[2]) if user_data else None


def get_creator(email):
    connection = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM creator_details WHERE  email='%s'" % email)
        user_data = cursor.fetchone()
        return Creator(user_data[4], user_data[1], user_data[2]) if user_data else None


def creator_forgot_password(email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("SELECT email from creator_details WHERE email=%s",[email])
    a=cur.fetchone()
    return a


def creator_update_token(token,date,email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("UPDATE creator_details SET token=%s,expiretime=%s WHERE email=%s",(token,date,email))
    cur.execute("SELECT * from creator_details")
    sql=cur.fetchall()
    myconn.commit()


def creator_select_result(token):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("SELECT token,expiretime,email from creator_details WHERE token=%s",[token])
    d=cur.fetchone()
    return d


def creator_update_password(password,s):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("UPDATE creator_details SET password=%s WHERE email=%s",(password,s[2]))
    myconn.commit()


def seeker_forgot_password(email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("SELECT email FROM seeker_details WHERE email= %s", [email])
    a = cur.fetchone()
    return a


def seeker_update_token(token,date,email):
    myconn = psycopg2.connect(
      "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("UPDATE seeker_details SET token= %s, expiretime= %s WHERE email= %s", (token, date, email))
    cur.execute("SELECT * FROM seeker_details ")
    sql = cur.fetchall()
    myconn.commit()


def seeker_select_result(token):
    myconn = psycopg2.connect(
       "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("SELECT token, expiretime,email FROM seeker_details WHERE token= %s ", [token])
    r = cur.fetchone()
    return r


def seeker_update_password(password,t):
    myconn = psycopg2.connect(
      "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("UPDATE seeker_details SET password = %s WHERE email= %s", (password, t[2]))
    myconn.commit()


def get_seeker_data(email):
    connection = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM seeker_details WHERE  email='%s'" % email)
        user_data = cursor.fetchone()
        connection.close()
        return user_data


def save_seeker_address(seeker_id, address):
    connection = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    with connection.cursor() as cursor:
        cursor.execute("insert into seeker_location (seeker_id,location) values('%d','%s')" %(seeker_id, address))
        connection.commit()


def save_seeker_mobile(seeker_id, mobile):
    con2 = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur2 = con2.cursor()
    add3 = "update seeker_details set mobile_number='%s' where seeker_id='%d'" %\
           (mobile, int(seeker_id))
    cur2.execute(add3)
    con2.commit()
    con2.close()


def get_seeker_mobile(seeker_id):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    curr.execute(
        "Select  mobile_number from seeker_details where seeker_id='%d'" % int(seeker_id))
    s_mobile = curr.fetchall()
    return s_mobile[0][0]


def get_seeker_address(seeker_id):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    curr.execute(
        "Select  location from seeker_location where seeker_id='%d'" % int(seeker_id))
    s_address = curr.fetchall()
    return s_address[0][0]


def recommend_list_database1(id_of_seeker):
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("select skills from seeker_skils where seeker_id=%d" % (int(id_of_seeker)))
    data = cur.fetchall()

    cur.execute("select location from seeker_location where seeker_id=%d" % (int(id_of_seeker)))
    seeker_location = cur.fetchone()

    cur.execute("select * from posted_jobs")
    data1 = cur.fetchall()

    cur.execute("select * from applied_jobs where seeker_id=%d" % (int(id_of_seeker)))
    status_check = cur.fetchall()
    conn.commit()
    return data, seeker_location, data1, status_check


def recommend_list_database2(job_ids_of_display):
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    value = []
    for x in job_ids_of_display:
        cur.execute("select * from posted_jobs where job_id=%d" % (x))
        data = cur.fetchall()
        value.append(data)
    conn.commit()
    return value


def recommend_list_database3(job_id, id_of_seeker):
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute(
        "insert into applied_jobs(job_id,seeker_id,status) values(%d,%d,'%s')" % (int(job_id), int(id_of_seeker), 'A'))
    conn.commit()


def create_new_job(creator_mail, job_name, job_description, skills_required, salary, location, vacancy, experience,
                   contact_details, scale, time_limit):
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()

    cur.execute("select creator_id from creator_details where email ='%s'" % creator_mail)
    creator_id = cur.fetchone()
    creator_id = creator_id[0]

    cur.execute("select max(job_id) from posted_jobs")
    data = cur.fetchone()
    job_id = (int(data[0]) + 1)

    job_description = " ".join(job_description.split())
    skills_required = " ".join(skills_required.split())

    cur.execute(
        "insert into posted_jobs(job_id,creator_id,job_name,job_description,skills_required,salary,location,vacancy,experience,time_limit,contact_details,scale) values(%d,%d,'%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s')"
        % (job_id, creator_id, job_name, job_description, skills_required, salary, location, vacancy, experience,
           time_limit, contact_details, scale))
    conn.commit()


def edit_create_new_job(job_id):  # integrate this (job_id)
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("select * from posted_jobs where job_id='%s'" % (job_id))
    data1 = cur.fetchall()
    conn.commit()
    for data in data1:
        job_name = data[2]
        job_description = data[3]
        skills_required = data[4]
        salary = data[5]
        location = data[6]
        vacancy = data[7]
        experience = data[8]
        time_limit = data[9]
        contact_details = data[10]
        scale = data[11]

        return job_name, job_description, skills_required, salary, location, vacancy, experience, time_limit, contact_details, scale

    # (job_id,creator_id,job_name,job_description,skills_required,salary,
    # location,vacancy,experience,time_limit,contact_details,scale) values(%d,%d,'%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s')"
    #                    %(job_id,creator_id,job_name,job_description,skills_required,salary,location,vacancy,experience,time_limit,contact_details,scale))


def edit_create_new_job2(creator_mail, job_name, job_description, skills_required, salary, location, vacancy,
                         experience, contact_details, scale, time_limit):

    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()

    # cur.execute("select creator_id from creator_details where email ='%s'" % creator_mail)
    # creator_id = cur.fetchone()
    # creator_id=creator_id[0]

    # cur.execute("select max(job_id) from posted_jobs")
    # data=cur.fetchone()
    print(skills_required)
    job_id = 105# integrate this
    job_description = " ".join(job_description.split())
    skills_required = " ".join(skills_required.split())

    cur.execute(
        "update posted_jobs set job_name='%s',job_description='%s',skills_required='%s',salary='%s',location='%s',vacancy=%d,experience='%s',time_limit='%s',contact_details='%s',scale='%s' where job_id='%s'"
        % (job_name, job_description, skills_required, salary, location, int(vacancy), experience, time_limit,
           contact_details, scale, job_id))
    conn.commit()


def get_skill(s_id):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    curr.execute("Select  skills from Seeker_skils where seeker_id='%d'" % int(s_id))  # to get the skills using seeker_id
    s_skill = curr.fetchall()
    return s_skill


def add_skill(s_id,skill):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    try:
        curr.execute("insert into Seeker_Skils (seeker_id , skills ) values('%d','%s')" % (int(s_id), str(skill)))
        con.commit()
        return 0
    except Exception as e:
        error = "This skill already exists"
        return error


def remove_skill(s_id,skill):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    #for name in skill:
    print(skill)
    remove = "delete from Seeker_skils where skills ='%s' and seeker_id = '%d'" % (skill,s_id)
    curr.execute(remove)
    con.commit()


def adding_experience(s_id,experience):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    print(s_id,experience)
    try:
        print(1)
        curr.execute("insert into Seeker_Experience (seeker_id , experience ) values('%d','%s')" % (int(s_id), str(experience)))
        print(2)
        con.commit()
        print(3)
        return 0
    except Exception as e:
        print(e)
        error = "This experience already exists"
        return error


def removing_experience(s_id,experience):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    #for name in skill:
    print(experience)
    remove = "delete from Seeker_Experience where experience ='%s' and seeker_id = '%d'" % (experience,s_id)
    curr.execute(remove)
    con.commit()


def get_experience(s_id):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    curr.execute("Select  experience from Seeker_Experience where seeker_id='%d'" % int(s_id))  # to get the skills using seeker_id
    s_exp = curr.fetchall()
    print(s_exp)
    return s_exp


def get_seeker_education(seeker_id):
    con = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    curr = con.cursor()
    curr.execute(
        "Select * from seeker_education where seeker_id='%d'" % int(seeker_id))
    s_education = curr.fetchall()
    return s_education


def update_seeker_profile(seeker_id, address, username):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("update seeker_details set name='%s' where seeker_id='%d'" %(username, int(seeker_id)))
    cur.execute("update seeker_location set location='%s' where seeker_id='%d'" %(address, int(seeker_id)))
    myconn.commit()


def my_current_job_db(post_email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    idd = cur.fetchall()[0]
    cur.execute(
        "select * from posted_jobs where job_id in(select job_id from applied_jobs where seeker_id='%d' and status='Final' and status_of_the_project is null)" % (
        idd[0]))
    get2 = cur.fetchall()

    return get2


def rejected_jobs_db(post_email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    idd = cur.fetchall()[0]
    cur.execute(
        "select * from posted_jobs where job_id  in(select job_id from applied_jobs where seeker_id='%d' and status='R')" % (
        idd[0]))
    get3 = cur.fetchall()

    return get3


def applied_jobs_db(post_email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    idd = cur.fetchall()[0]
    cur.execute(
        "select * from posted_jobs where job_id  in(select job_id from applied_jobs where seeker_id='%d' and status='A')" % (
        idd[0]))
    get4 = cur.fetchall()

    return get4


def applied_job_cancel_db(job_id, post_email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    idd = cur.fetchall()[0]
    cur.execute("delete from applied_jobs where job_id=%d and seeker_id=%d" % (int(job_id), idd[0]))
    myconn.commit()


def approve_jobs_db(post_email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    idd = cur.fetchall()[0]
    cur.execute(
        "select * from posted_jobs where job_id  in(select job_id from applied_jobs where seeker_id='%d' and status='AP')" % (
        idd[0]))
    get5 = cur.fetchall()
    myconn.commit()
    return get5


def approve_job_cancel_db(job_id, post_email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    idd = cur.fetchall()[0]
    cur.execute("delete from applied_jobs where job_id=%d and seeker_id=%d" % (int(job_id), idd[0]))
    myconn.commit()


def approve_job_approve_db(job_id, post_email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    idd = cur.fetchall()[0]
    cur.execute(
        "UPDATE applied_jobs set status='%s' where job_id=%d and seeker_id=%d " % ('Final', int(job_id), idd[0]))
    myconn.commit()


def completed_job1_db(post_email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    seeker_id = cur.fetchall()[0]

    cur.execute(
        "select * from posted_jobs where job_id in(select job_id from applied_jobs where seeker_id='%d' and status_of_the_project='Completed')" % (
            seeker_id))
    get6 = cur.fetchall()

    cur.execute("select job_id from ratings where creator_rating IS NULL and seeker_id='%d'" % (seeker_id))
    idd = cur.fetchall()
    print(idd)

    get_value = []
    for x in get6:
        if str(x[0]) in str(idd):
            get_value.append(x)
            print(x[0])
        else:
            continue
    get6 = get_value
    myconn.commit()
    return get6


def completed_job2_db(job_id, creator_rating, post_email):  # job_id,seeker_id,creator_ratings,
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select seeker_id from seeker_details where email ='%s'" % post_email)
    seeker_id = cur.fetchall()[0]

    cur.execute("SELECT creator_rating FROM ratings WHERE job_id=%s and seeker_id=%s", [
        job_id, seeker_id])
    s = cur.fetchone()

    if s == None:
        cur.execute("INSERT INTO ratings(job_id,seeker_id,creator_rating) values(%s,%s,%s)",
                    (job_id, seeker_id, creator_rating))
        myconn.commit()
        print("inserted")
    else:
        cur.execute("UPDATE ratings SET creator_rating=%s WHERE job_id=%s and seeker_id=%s",
                    (creator_rating, job_id, seeker_id))
        print("Table updated....")

    myconn.commit()



    
def get_creator_id(creator_email):  # to get the creator_id based on email
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()

    add = "Select  creator_id from creator_details where email='%s'" % creator_email  # to get the seeker_id using email
    cur.execute(add)
    records = cur.fetchall()[0]
    # print(records)
    r_id = records[0]
    return r_id


def get_jobs_based_on_status(creator_id,
                             status):  # get the job_list for creator based on his id and status(A/AP/Final/Completed)
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute(
        "select a.* from posted_jobs a where a.creator_id='%d' and a.job_id in(select job_id from applied_jobs where "
        "status='%s' and status_of_the_project IS NULL )" % (creator_id, status))
    pending = cur.fetchall()
    return pending


def get_all_job_for_creator(creator_id):  # get the job_list for creator based on his id and
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute(
        "select a.* from posted_jobs a where a.creator_id='%d' " % (creator_id))
    pending = cur.fetchall()
    #print(pending)
    return pending


def get_seeker_id_based_on_status(job_id, status):  # this is useful when creator wants to view the candidates(at that
    # time,we can get the seeker_id based on jobid and status(A/AP/Final))
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("select seeker_id from applied_jobs where job_id='%d' and status='%s'" % (int(job_id), status))
    output = cur.fetchall()
    return output


def get_seeker_basic_details(seeker_id):  # to get the basic details of seeker based on his id
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("select email, mobile_number, name from seeker_details where seeker_id= '%d'" % (int(seeker_id)))
    a = cur.fetchall()
    return a


def get_seeker_skill(seeker_id):  # to get the skills of seeker based on his id
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("select skills from seeker_skils where seeker_id= '%d'" % (int(seeker_id)))
    b = (cur.fetchall())
    return b


def get_seeker_exp(seeker_id):  # to get the experience of seeker based on his id
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("select experience from seeker_experience where seeker_id= '%d'" % (int(seeker_id)))
    c = cur.fetchall()
    return c


def delete_job_for_creator(job_id):  # if the creator wants to delete the job
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("delete from  ratings where job_id='%d'" % int(job_id))
    conn.commit()
    cur.execute("delete from applied_jobs where job_id='%d'" % int(job_id))
    conn.commit()
    cur.execute("delete from  posted_jobs where job_id='%d'" % int(job_id))
    conn.commit()


def update_status_for_creator(status, job_id, seeker_id):  # if the creator wants to accept update his project status(this is
    # allowed only if staus is Final for atleast one candidate)
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("UPDATE applied_jobs SET status='%s' WHERE job_id='%d' AND seeker_id='%d'" %(status, int(job_id), int(seeker_id)))
    #print("table updated...")
    conn.commit()


def get_jobs_based_on_status_of_proj(creator_id, status):  # to show the completed jobs for creator
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute(
        "select a.* from posted_jobs a where a.creator_id='%d' and a.job_id in(select job_id from applied_jobs "
        "where status_of_the_project='%s')" % (creator_id, status))
    pending = cur.fetchall()
    pending = (pending)
    #print(pending)
    list1 = []
    for k in pending:
        m = list(k)
        #print(m)
        cur.execute("select count(seeker_id) from applied_jobs where job_id='%d' and status='Final'" % (int(k[0])))
        h = cur.fetchall()
        #print(h)
        cur.execute("select count(seeker_id) from ratings where job_id='%d' and seeker_rating is not null" % (int(k[0])))
        j = cur.fetchall()
        #print(j)
        if h != j:
            #print("yes")
            m.append("yes")
        list1.append(m)
    #print(list1)
    return list1


def creator_side_get_rating(job_id, seeker_id):
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("SELECT creator_rating FROM ratings WHERE job_id=%s and seeker_id=%s", [
        job_id, seeker_id])
    s = cur.fetchone()
    return s


def creator_side_inser_rating(job_id, seeker_id, creator_rating):
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("INSERT INTO ratings(job_id,seeker_id,seeker_rating) values(%s,%s,%s)",
                (job_id, seeker_id, creator_rating))
    conn.commit()


def creator_side_update_rating(creator_rating, job_id, seeker_id): # this is not needed actually (but if we are
    # allowing a creator to rate a seeker for the 2nd time, this is needed)
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("UPDATE ratings SET seeker_rating=%s WHERE job_id=%s and seeker_id=%s",
                (creator_rating, job_id, seeker_id))
    conn.commit()


def creator_side_getall_rating():
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ratings")
    a = cur.fetchone()
    return a


def get_seeker_for_rating(
        seeker_id2,job_id):  # this is to get the seeker_details checking whether seeker_id exists in ratings table(
    # whether seeker_rating is there or not)
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("select a.seeker_id,a.email,a.mobile_number,a.name from seeker_details a where seeker_id='%d' and "
                "seeker_id not in(select seeker_id from ratings where job_id='%d' and seeker_rating is not null) " % (seeker_id2,job_id))
    a = cur.fetchall()
    return a


def get_seeker_id_for_rating(job):  # to get the seeker_id if both creator and seeker are agreed for work(if status
    # is Final) and status  of the project updated as completed
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242'
        '.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute(
        "select seeker_id from applied_jobs where job_id='%d'and status='Final' and status_of_the_project='Completed'" % (
            int(job)))
    a = cur.fetchall()
    return a


def profile_in(email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("SELECT name,address,mobile_number FROM creator_details WHERE  email=%s", [email])
    a = cur.fetchone()
    #print(a)
    myconn.commit()
    return a


def profile_id(name, address, email):
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("UPDATE creator_details SET name=%s,address =%s WHERE email=%s ", (name, address, email))
    #print("table updated")
    cur.execute("SELECT * FROM creator_details")
    p = cur.fetchall()
    #print(p)
    myconn.commit()
    return p

def create_new_job(creator_mail, job_name, job_description, skills_required, salary, location, vacancy, experience,
                   contact_details, scale, time_limit):
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()

    cur.execute("select creator_id from creator_details where email ='%s'" % creator_mail)
    creator_id = cur.fetchone()
    creator_id = creator_id[0]

    cur.execute("select max(job_id) from posted_jobs")
    data = cur.fetchone()
    '''try:
     job_id = (int(data[0]) + 1)
    except:
        job_id=1'''

    job_description = " ".join(job_description.split())
    skills_required = " ".join(skills_required.split())

    cur.execute(
        "insert into posted_jobs(creator_id,job_name,job_description,skills_required,salary,location,vacancy,experience,time_limit,contact_details,scale) values(%d,'%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s')"
        % ( creator_id, job_name, job_description, skills_required, salary, location, vacancy, experience,
           time_limit, contact_details, scale))
    conn.commit()


def edit_create_new_job(job_id):  # integrate this (job_id)
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()
    cur.execute("select * from posted_jobs where job_id='%s'" % (job_id))
    data1 = cur.fetchall()
    conn.commit()
    for data in data1:
        job_name = data[2]
        job_description = data[3]
        skills_required = data[4]
        salary = data[5]
        location = data[6]
        vacancy = data[7]
        experience = data[8]
        time_limit = data[9]
        contact_details = data[10]
        scale = data[11]

        return job_name, job_description, skills_required, salary, location, vacancy, experience, time_limit, contact_details, scale

    # (job_id,creator_id,job_name,job_description,skills_required,salary,
    # location,vacancy,experience,time_limit,contact_details,scale) values(%d,%d,'%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s')"
    #                    %(job_id,creator_id,job_name,job_description,skills_required,salary,location,vacancy,experience,time_limit,contact_details,scale))


def edit_create_new_job2(creator_mail, job_id2, job_name, job_description, skills_required, salary, location, vacancy,
                         experience, contact_details, scale, time_limit):
    job_id = job_id2  # integrate this
    conn = psycopg2.connect(
        'postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv')
    cur = conn.cursor()

    # cur.execute("select creator_id from creator_details where email ='%s'" % creator_mail)
    # creator_id = cur.fetchone()
    # creator_id=creator_id[0]

    # cur.execute("select max(job_id) from posted_jobs")
    # data=cur.fetchone()
    #print(skills_required)
    job_description = " ".join(job_description.split())
    skills_required = " ".join(skills_required.split())

    cur.execute(
        "update posted_jobs set job_name='%s',job_description='%s',skills_required='%s',salary='%s',location='%s',vacancy=%d,experience='%s',time_limit='%s',contact_details='%s',scale='%s' where job_id='%s'"
        % (job_name, job_description, skills_required, salary, location, int(vacancy), experience, time_limit,
           contact_details, scale, job_id))
    conn.commit()


def get_project_status(creator_id):  # to get the status of the project if the creator wants to update the status
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242"
        ".compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select a.job_name,a.job_description,a.job_id from posted_jobs a where a.creator_id='%d' and a.job_id "
                "in(select b.job_id from applied_jobs b where b.status_of_the_project IS NULL)" % creator_id)
    f = cur.fetchall()
    #print(f)
    for t in f:
        cur.execute("select status from applied_jobs where job_id='%d'" % (int(t[2])))  # using this we are checking
        # whether status is Final for atleast one candidate if not, then that project status cannot be completed
        g = cur.fetchall()
        #print(g[0], g)
        if ('Final',) not in g:
            f.remove(t)
    #print(f)
    return f


def up_project_status(j_id):  # to update the project as completed for creator
    #print(j_id)
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("update applied_jobs set status_of_the_project='Completed' where job_id='%d'" % (j_id))
    myconn.commit()


def get_job_id(cre_id):  # to get the job_id based on creator_id
    myconn = psycopg2.connect(
        "postgres://bijylgibfwwhqv:953577e1fae84feb07ad8df06b81d42b0b8002a6ab9a6838e10eaf19075614c7@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d3gqb6tqvfmfdv")
    cur = myconn.cursor()
    cur.execute("select job_id from posted_jobs where creator_id='%d'" % (cre_id))
    r = cur.fetchall()[0]
    #print(r)
    return r