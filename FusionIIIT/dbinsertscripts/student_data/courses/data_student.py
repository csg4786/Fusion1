import xlrd
import sys
import os
import django
sys.path.append(r'/home/fusion/Fusion/FusionIIIT/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Fusion.settings'
django.setup()


from django.contrib.auth.models import User
from applications.academic_information.models import Student,Course, Curriculum
from applications.academic_procedures.models import Register
from applications.globals.models import DepartmentInfo, Designation, ExtraInfo, HoldsDesignation

filenames = print (os.listdir('/home/fusion/Fusion/FusionIIIT/dbinsertscripts/student_data/btech'))
for filename in filenames:

    excel = xlrd.open_workbook(
            os.path.join(
                os.path.dirname(__file__),
                'btech', filename))
    z = excel.sheet_by_index(0)

    not_inserted_index = []

    course_name = str(z.cell(7, 2).value)
    course_code = str(z.cell(6, 2).value)
    instructor = str(z.cell(8, 2).value)


    #Extracting branch from filename
    first = filename[0:3]
    if(first == "CS"):
        branch = "CSE"
    elif(first == "EC"):
        branch = "ECE"
    elif(first = "ME"):
        branch = "ME"
    else:
        branch = "Common"


    #Extracting branch and sem from filename
    second = filename[2:3]
    if(second == '1'):
        sem = 1
        batch = 2019
    elif(second == '2'):
        sem = 3
        batch = 2018
    elif(second == '3'):
        sem = 5
        batch = 2017
    else:
        sem = 7
        batch = 2016


    programme = 'B.Tech'
    credits = 2

    try: 
        course_obj = Course.objects.filter(course_name = course_name).get(course_details = instructor)
    except :
        course_obj = Course(
            course_name = course_name,
            course_details = instructor)
        course_obj.save()
    try:
        curriculum_obj = Curriculum.objects.filter(course_code = course_code).filter(batch = batch).filter(programme = programme).get(branch=branch)
    except:
        curriculum_obj = Curriculum(
            course_code = course_code,
            course_id = course_obj,
            credits = credits,
            course_type = 'Professional Core',
            programme = programme,
            branch = branch,
            batch = batch,
            sem = sem,
            floated = True)
        curriculum_obj.save()


    for i in range(10, 130):
        try:
            print(i)
            roll_no = int(z.cell(i, 1).value)
            username = str(roll_no)
            print(username)

            dep = str(z.cell(i, 3).value)
            password= "hello123"
            try:
                user = User.objects.get(username = username)
                print(1)
            except:
                print(2)
                user = User.objects.create_user(username,password=password)
                user.save()
            print(user)
            try:
                holds_desg = HoldsDesignation.objects.get(user = user)
            except:
                holds_desg = HoldsDesignation(
                    user = user,
                    working = user,
                    designation = Designation.objects.get(name = "student")
                )
            try:
                ext = ExtraInfo.objects.get(user = user)
            except:
                ext = ExtraInfo(
                id = roll_no,
                user = user,
                sex = 'M',
                user_type = 'student',
                department = DepartmentInfo.objects.get(name = branch)
                )
                ext.save()
            try:
                st = Student.objects.get(id = ext)
            except:
                st = Student(
                    id = ext,
                    programme = programme,
                    batch = batch,
                    cpi = 9.5,
                    category = "GEN",
                    specialization = None,
                    room_no = "A-302",
                    hall_no = "4",
                )
                st.save()
            if batch == 2018 :
                print (curriculum_obj)
                print (st)
                count = Register.objects.all().count()
                register_obj_create = Register(
                    register_id = count + 1,
                    curr_id = curriculum_obj,
                    year = batch,
                    student_id = st,
                    semester = sem)
                register_obj_create.save()
            else :
                continue
            print(str(i) + "done")
        except Exception as e:
            print(e)
            print(i)
            not_inserted_index.append(i)
    print(not_inserted_index)
