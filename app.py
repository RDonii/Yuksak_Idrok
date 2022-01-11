import os
from flask import Flask, request, abort
from flask.helpers import url_for
from flask.json import jsonify
from sqlalchemy.sql.functions import func
from werkzeug.utils import redirect, secure_filename
from database.models import Categories, Courses, Teachers, Individuals, Groups, Certifications, News, Awards, Messages, create_db, db
from flask_cors import CORS
import uuid
from auth.auth import get_loged, login_required

#yordamchi funksiyalar

ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'wmv', 'avi'}
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def paginate(objects, limit, page):
    start = (page-1)*limit
    end = start+limit
    response = objects[start:end]
    return response

def allowed_img(filename):
    return '.' in filename and filename.rsplit('.')[::-1][0].lower() in ALLOWED_IMG_EXTENSIONS

def allowed_video(filename):
    return '.' in filename and filename.rsplit('.')[::-1][0].lower() in ALLOWED_VIDEO_EXTENSIONS


def create_app(test_config=None):
    UPLOAD_FOLDER = 'static/uploads'

    app = Flask(__name__)
    create_db(app)
    CORS(app)
    app.secret_key = 'you_cant_hack_anyway'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    #admin_page ga kirish uchun

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.get_json()

            username = data.get('username')
            password = data.get('password')

            if username and password:
                token = get_loged(username, password)
            else:
                abort(400, 'Parol va Username kiritilishi shart.')
            return jsonify({"token": token})

        return 'Not implemented yet'


    #kategoriya va kurslar uchun endpointlar
    
    @app.route('/categories')
    def all_categories():
        all_categories_query = Categories.query.all()
        all_categories_formated = [category.format() for category in all_categories_query]
        count = len(all_categories_formated)

        return jsonify({
            'categories': all_categories_formated,
            'count': count
        })

    @app.route('/categories', methods=["POST"])
    #login_required
    def add_category():
        data = request.get_json()
        name = data.get('name')

        if name and len(name) != 0:
            check_query = Categories.query.filter(func.lower(Categories.name)==func.lower(name)).one_or_none()
            if check_query:
                abort(422, 'Bu nomdagi kategoriya mavjud.')
            try:
                new_categoty = Categories(name)
                new_categoty.insert()
            except:
                abort(500, 'Serverda ichki xatolik.')
            return jsonify({
                'success': True
            })
        else:
            abort(400, 'Yangi kategoriyaga nom bering.')

    @app.route('/categories/<int:category_id>')
    def category_by_id(category_id):
        category = Categories.query.filter(Categories.id==category_id).one_or_none()
        if category is None:
            abort(404, 'Ushbu kategoriya mavjud emas.')

        category_name = category.name

        return jsonify({
            "name": category_name
        })

    @app.route('/categories/<int:category_id>', methods=['PATCH', 'DELETE'])
    @login_required
    def implement_category_by_id(payload, category_id):
        category = Categories.query.filter(Categories.id==category_id).one_or_none()
        if category is None:
            abort(404, 'Ushbu kategoriya mavjud emas.')
        
        if request.method == 'PATCH':
            data = request.get_json()
            name = data.get("name")

            check_query = Categories.query.filter(func.lower(Categories.name)==func.lower(name)).one_or_none()
            if check_query:
                abort(400, 'Bu nomdagi kategoriya mavjud.')

            if name and len(name) != 0:
                try:
                    category.name = name
                    category.update()
                    return jsonify({
                        'success': True
                    })
                except:
                    db.session.rollback()
                    abort(500, 'Serverda ichki xatolik.')
            else:
                abort(400, 'Yangi kategoriyaga nom bering.')

        if request.method == 'DELETE':
            courses = Courses.query.filter(Courses.category_id == category_id).all()

            try:
                #agar categoriyaga tegishli kurslar mavjud bo'lsa avval ularni o'chiradi.
                if len(courses) != 0:
                    for c in courses:
                        #agar kursga tegishli guruhlar mavjud bo'lsa avval ularni o'chiradi.
                        individuals = Individuals.query.filter(Individuals.course_id == c.id).all()
                        groups = Groups.query.filter(Groups.course_id == c.id).all()

                        try:
                            if len(individuals) != 0:
                                for i in individuals:
                                    i.delete()

                            if len(groups) != 0:
                                for g in groups:
                                    g.delete()

                            c.delete()

                            return jsonify({
                                'success': True
                            })
                        except:
                            db.session.rollback()
                            abort(500, 'Serverda ichki xatolik.')

                category.delete()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')

    @app.route('/categories/<int:category_id>/courses')
    def get_courses_by_category(category_id):
        courses_query = Courses.query.filter(Courses.category_id==category_id).all()
        courses_formated = [course.format() for course in courses_query]
        count = len(courses_formated)

        return jsonify({
            "courses": courses_formated,
            "count": count
        })
    
    @app.route('/courses', methods=["GET"])
    def all_courses():
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 8, type=int)
        all_courses_query = Courses.query.all()
        all_courses_formated = [course.format() for course in all_courses_query]
        courses_paginated = paginate(all_courses_formated, limit, page)
        count = len(all_courses_formated)

        return jsonify({
            "courses": courses_paginated,
            "page": page,
            "limit": limit,
            "count": count
        })

    @app.route('/courses', methods=["POST"])
    @login_required
    def add_courses(payload):
        category_name = request.form.get('category')
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('image')

        if category_name is None or title is None:
            abort(400, 'Kurs nomi va kategoriyasi kiritilishi shart')
        if len(category_name) == 0 or len(title) == 0:
            abort(400, "Bo'sh kurs nomi va kategoriyasi qabul qilinmaydi.")
        if file is None:
            img = ''
        elif allowed_img(file.filename):
            filename = file.filename
            filename = str(uuid.uuid4()) + '.' +filename.split('.')[::-1][0]
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = (request.base_url).replace(url_for('all_courses'), '/display/') + filename
        else:
            abort(415, 'Ruxsat etilmagan formatdagi fayl yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')

        check_query = Courses.query.filter(func.lower(Courses.title)==func.lower(title)).one_or_none()
        if check_query:
            abort(422, 'Bu nomdagi kurs mavjud.')

        category_query = Categories.query.filter(func.lower(Categories.name) == func.lower(category_name)).one_or_none()
        if category_query is None:
            abort(404, 'Mavjud kategoriyalardan birini tanlang.')
        category_id = category_query.id

        try:
            new_course = Courses(category_id, title, img, description)
            new_course.insert()
        except:
            db.session.rollback()
            abort(500, 'Serverda ichki xatolik.')
        
        return jsonify({
            'success': True
        })

    @app.route('/courses/<int:course_id>')
    def course_by_id(course_id):

        course = Courses.query.filter(Courses.id==course_id).one_or_none()
        if course is None:
            abort(404, "So`ralgan kurs bazada mavjud emas.")

        course_formated = [course.format()]

        return jsonify({
            "course": course_formated
        })

    @app.route('/courses/<int:course_id>', methods = ['PATCH', 'DELETE'])
    @login_required
    def implement_course_by_id(payload, course_id):
        course = Courses.query.filter(Courses.id==course_id).one_or_none()
        if course is None:
            abort(404, "So`ralgan kurs bazada mavjud emas.")
        
        if request.method == 'DELETE':
            #agar kursga tegishli guruhlar mavjud bo'lsa avval ularni o'chiradi.
            individuals = Individuals.query.filter(Individuals.course_id == course_id).all()
            groups = Groups.query.filter(Groups.course_id == course_id).all()

            try:
                if len(individuals) != 0:
                    for i in individuals:
                        i.delete()

                if len(groups) != 0:
                    for g in groups:
                        g.delete()

                course.delete()

                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')

        if request.method == 'PATCH':
            category_name = request.form.get('category')
            title = request.form.get('title')
            description = request.form.get('description')
            file = request.files.get('image')

            if category_name:
                category_query = Categories.query.filter(func.lower(Categories.name)==func.lower(category_name)).one_or_none()
                if category_query is None:
                    abort(404, 'Mavjud kategoriyalardan birini tanlang.')
                category_id = category_query.id
                course.category_id = category_id

            if title:
                if len(title) == 0:
                    abort(400, "Bo'sh kurs nomi qabul qilinmaydi.")
                check_query = Courses.query.filter(func.lower(Courses.title)==func.lower(title)).one_or_none()
                if check_query:
                    abort(422, 'Bu nomdagi kurs mavjud.')
                course.title = title
            
            if description:
                course.description = description

            if file:
                if allowed_img(file.filename):
                    filename = file.filename
                    filename = str(uuid.uuid4()) + '.' +filename.split('.')[::-1][0]
                    filename = secure_filename(filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    img = (request.base_url).replace(url_for('course_by_id', course_id=course_id), '/display/') + filename
                    course.img = img
                else:
                    abort(415, 'Ruxsat etilmagan formatdagi fayl yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')

            course.update()

            return jsonify({
                "seccess": True
            })

    @app.route('/individuals')
    def get_all_individual_course():
        individuals = Individuals.query.all()
        individuals_formated = [i.format() for i in individuals]
        count = len(individuals_formated)

        return jsonify({
            'individuals': individuals_formated,
            'count': count
        })

    @app.route('/courses/<int:course_id>/individuals')
    def individuals_by_course(course_id):
        course = Courses.query.filter(Courses.id==course_id).one_or_none()
        if course is None:
            abort(404, "So`ralgan kurs bazada mavjud emas.")
        individuals = Individuals.query.filter(Individuals.course_id==course_id).all()
        individuals_formated = [i.format() for i in individuals]
        count = len(individuals_formated)

        return jsonify({
            'individuals': individuals_formated,
            'count': count
        })

    @app.route('/courses/<int:course_id>/individuals', methods=['POST'])
    @login_required
    def add_individuals_to_course(payload, course_id):
        course = Courses.query.filter(Courses.id==course_id).one_or_none()
        if course is None:
            abort(404, "So`ralgan kurs bazada mavjud emas.")
        
        data = request.get_json()

        teacher_id = data.get('teacher_id')
        members = data.get('members', 0)
        price = data.get('price')
        start = data.get('start', 'belgilanmagan')
        end = data.get('end', 'belgilanmagan')
        duration = data.get('duration')
        days = data.get('days', 'belgilanmagan')
        in_month = data.get('in_month')
        active = data.get('active', False)

        if teacher_id is None:
            abort(400, 'Mavjud o`qituvchilardan birini tanlang.')
        if price is None:
            abort(400, 'Kurs narxini kiriting.')
        if duration is None:
            abort(400, 'Kurs darslari necha soatdan bo`lishini kiriting.')
        if in_month is None:
            abort(400, 'Kurs darslari bir oyda necha marta bo`lishini kiriting.')
        
        try:
            new_individual = Individuals(course_id, teacher_id, members, price, start, end, duration, days, in_month, active)
            new_individual.insert()
            return jsonify({
                'success': True
            })
        except:
            db.session.rollback()
            abort(500, 'Serverda ichki xatolik.')

    @app.route('/individuals/<int:individual_id>')
    def individuals_by_id(individual_id):
        
        individual = Individuals.query.filter(Individuals.id==individual_id).one_or_none()
        if individual == None:
            abort(404, 'So`ralgan individual kurs mavjud emas.')
        
        individual_formated = [individual.format()]
        return ({
            'individual': individual_formated
        })

    @app.route('/individuals/<int:individual_id>', methods=['PATCH', 'DELETE'])
    @login_required
    def implement_individuals_by_id(payload, individual_id):
        
        individual = Individuals.query.filter(Individuals.id==individual_id).one_or_none()
        if individual == None:
            abort(404, 'So`ralgan individual kurs mavjud emas.')
        
        if request.method == 'PATCH':
            data = request.get_json()

            teacher_id = data.get('teacher_id')
            members = data.get('members')
            price = data.get('price')
            start = data.get('start')
            end = data.get('end')
            duration = data.get('duration')
            days = data.get('days')
            in_month = data.get('in_month')
            active = data.get('active')

            try:
                if teacher_id:
                    individual.teacher_id = teacher_id
                if members:
                    individual.members = members
                if price:
                    individual.price = price
                if start:
                    individual.start = start
                if end:
                    individual.end = end
                if duration:
                    individual.duration = duration
                if days:
                    individual.days = days
                if in_month:
                    individual.in_month = in_month
                if active:
                    individual.active = active

                individual.update()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')
            
        if request.method == 'DELETE':
            try:
                individual.delete()
                return({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')    
        
    @app.route('/groups')
    def get_all_group_course():
        groups = Groups.query.all()
        groups_formated = [g.format() for g in groups]
        count = len(groups_formated)

        return jsonify({
            'groups': groups_formated,
            'count': count
        })

    @app.route('/courses/<int:course_id>/groups')
    def groups_by_course(course_id):

        course = Courses.query.filter(Courses.id==course_id).one_or_none()
        if course is None:
            abort(404, "So`ralgan kurs bazada mavjud emas.")

        groups = Groups.query.filter(Groups.course_id==course_id).all()
        groups_formated = [g.format() for g in groups]
        count = len(groups_formated)

        return jsonify({
            'groups': groups_formated,
            'count': count
        })

    @app.route('/courses/<int:course_id>/groups', methods=['POST'])
    @login_required
    def add_groups_by_course(payload, course_id):

        course = Courses.query.filter(Courses.id==course_id).one_or_none()
        if course is None:
            abort(404, "So`ralgan kurs bazada mavjud emas.")

        data = request.get_json()

        teacher_id = data.get('teacher_id')
        members = data.get('members', 0)
        price = data.get('price')
        start = data.get('start', 'belgilanmagan')
        end = data.get('end', 'belgilanmagan')
        duration = data.get('duration')
        days = data.get('days', 'belgilanmagan')
        in_month = data.get('in_month')
        active = data.get('active', False)

        if teacher_id is None:
            abort(400, 'Mavjud o`qituvchilardan birini tanlang.')
        if price is None:
            abort(400, 'Kurs narxini kiriting.')
        if duration is None:
            abort(400, 'Kurs darslari necha soatdan bo`lishini kiriting.')
        if in_month is None:
            abort(400, 'Kurs darslari bir oyda necha marta bo`lishini kiriting.')
        
        try:
            new_group = Groups(course_id, teacher_id, members, price, start, end, duration, days, in_month, active)
            new_group.insert()
            return jsonify({
                'success': True
            })
        except:
            db.session.rollback()
            abort(500, 'Serverda ichki xatolik.')                

    @app.route('/groups/<int:group_id>')
    def groups_by_id(group_id):
        group = Groups.query.filter(Groups.id==group_id).one_or_none()
        if group == None:
            abort(404, 'So`ralgan individual kurs mavjud emas.')
        
        group_formated = [group.format()]
        return ({
            'group': group_formated
        })

    @app.route('/groups/<int:group_id>', methods=['PATCH', 'DELETE'])
    @login_required
    def implement_groups_by_id(payload, group_id):
        group = Groups.query.filter(Groups.id==group_id).one_or_none()
        if group == None:
            abort(404, 'So`ralgan individual kurs mavjud emas.')

        if request.method == 'PATCH':
            data = request.get_json()

            teacher_id = data.get('teacher_id')
            members = data.get('members')
            price = data.get('price')
            start = data.get('start')
            end = data.get('end')
            duration = data.get('duration')
            days = data.get('days')
            in_month = data.get('in_month')
            active = data.get('active')

            try:
                if teacher_id:
                    group.teacher_id = teacher_id
                if members:
                    group.members = members
                if price:
                    group.price = price
                if start:
                    group.start = start
                if end:
                    group.end = end
                if duration:
                    group.duration = duration
                if days:
                    group.days = days
                if in_month:
                    group.in_month = in_month
                if active:
                    group.active = active

                group.update()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')                
            
        if request.method == 'DELETE':
            try:
                group.delete()
                return({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')                    
        
    #o'qituvchi va sertifikatlar uchun endpointlar
    @app.route('/teachers')
    def all_teachers():
        
        teachers = Teachers.query.all()
        teachers_formated = [t.format() for t in teachers]
        count = len(teachers_formated)
        return jsonify({
            'teachers': teachers_formated,
            'count': count
        })

    @app.route('/teachers', methods=["POST"])
    @login_required
    def add_teachers(payload):
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name', '')
        description = request.form.get('description', '')
        file = request.files.get('image')

        if first_name is None:
            abort(400, 'O`qituvchi ismini kiritish zarur.')
        if file is None:
            img = ''
        elif allowed_img(file.filename):
            filename = file.filename
            filename = str(uuid.uuid4()) + '.' + filename.split('.')[::-1][0]
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
            img = (request.base_url).replace(url_for('all_teachers'), '/display/') + filename
        else:
            abort(415, 'Ruxsat etilmagan formatdagi fayl yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')
        try:
            new_teacher = Teachers(first_name, last_name, description, img)
            new_teacher.insert()
            return jsonify({
                'success': True
            })
        except:
            db.session.rollback()
            abort(500, 'Serverda ichki xatolik.')                

    @app.route('/teachers/<int:teacher_id>')
    def teachers_by_id(teacher_id):
        teacher = Teachers.query.filter(Teachers.id==teacher_id).one_or_none()
        if teacher is None:
            abort(404, 'So`ralgan o`qituvchi bazada mavjud emas.')            

        teacher_formated = [teacher.format()]
        return jsonify({
            'teacher': teacher_formated
        })

    @app.route('/teachers/<int:teacher_id>', methods=["PATCH", "DELETE"])
    @login_required
    def implement_teachers_by_id(payload, teacher_id):
        teacher = Teachers.query.filter(Teachers.id==teacher_id).one_or_none()
        if teacher is None:
            abort(404, 'So`ralgan o`qituvchi bazada mavjud emas.')

        if request.method == 'PATCH':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            description = request.form.get('description')
            file = request.files.get('image')
            
            if first_name:
                teacher.first_name = first_name
            if last_name:
                teacher.last_name = last_name
            if description:
                teacher.description = description
            if file:
                if allowed_img(file.filename):
                    filename = file.filename
                    filename = str(uuid.uuid4()) + '.' + filename.split('.')[::-1][0]
                    filename = secure_filename(filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
                    img = (request.base_url).replace(url_for('teachers_by_id', teacher_id=teacher_id), '/display/') + filename
                    teacher.img = img
                else:
                    abort(415, 'Ruxsat etilmagan formatdagi fayl yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')
            try:
                teacher.update()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')                
            
        if request.method == 'DELETE':
            individuals = Individuals.query.filter(Individuals.teacher_id==teacher_id).first()
            groups = Groups.query.filter(Groups.teacher_id==teacher_id).first()
            if individuals or groups:
                abort(422, 'Avval {} dars o`tadigan guruhlar uchun yangi o`qituvchi tayinlang.'.format(teacher.first_name) )
            try:
                teacher.delete()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')

    @app.route('/teachers/<int:teacher_id>/courses')
    def courses_by_teacher(teacher_id):
        teacher = Teachers.query.filter(Teachers.id==teacher_id).one_or_none()
        if teacher is None:
            abort(404, 'So`ralgan o`qituvchi bazada mavjud emas.')

        individuals = Individuals.query.filter(Individuals.teacher_id==teacher_id).all()
        individuals_formated = [i.format() for i in individuals]
        count_individuals =len(individuals_formated)

        groups = Groups.query.filter(Groups.teacher_id==teacher_id).all()
        groups_formated = [g.format() for g in groups]
        count_groups = len(groups_formated)

        return jsonify({
            'individuals': individuals_formated,
            'count_individuals': count_individuals,
            'groups': groups_formated,
            'count_groups': count_groups
        })

    @app.route('/teachers/<int:teacher_id>/certifications')
    def certifications_by_teacher(teacher_id):
        teacher = Teachers.query.filter(Teachers.id==teacher_id).one_or_none()
        if teacher is None:
            abort(404, 'So`ralgan o`qituvchi bazada mavjud emas.')

        certifications = Certifications.query.filter(Certifications.teacher_id==teacher_id).all()
        certifications_formated = [c.format() for c in certifications]
        count = len(certifications_formated)

        return jsonify({
            'certifications': certifications_formated,
            'count': count,
        })

    @app.route('/certifications')
    def all_certifications():            
    
        certifications = Certifications.query.all()
        certifications_formated = [c.format() for c in certifications]
        count = len(certifications_formated)

        return jsonify({
            'certifications': certifications_formated,
            'count': count
        })

    @app.route('/certifications', methods = ["POST"])
    @login_required
    def add_certifications(payload):
        teacher_id = request.form.get('teacher_id')
        title = request.form.get('title')
        given_by = request.form.get('given_by', '')
        credential = request.form.get('credential', '')
        file = request.files.get('image')

        if teacher_id is None:
            abort(400, 'O`qituvchilardan birini tanlang.')
        if title is None:
            abort(400, 'Sertifikat nomini kiriting.')
        if file is None:
            img = ''
        elif allowed_img(file.filename):
            filename = file.filename
            filename = str(uuid.uuid4()) + '.' + filename.split('.')[::-1][0]
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = (request.base_url).replace(url_for('all_certifications'), '/display/') + filename
        
        try:
            new_certification = Certifications(teacher_id, title, given_by, credential, img)
            new_certification.insert()
            return jsonify({
                'success': True
            })
        except:
            db.session.rollback()
            abort(500, 'Serverda ichki xatolik.')

    @app.route('/certifications/<int:certification_id>')
    def certification_by_id(certification_id):
        certification = Certifications.query.filter(Certifications.id==certification_id).one_or_none()
        if certification is None:
            abort(404, 'So`ralgan sertifikat bazada mavjud emas.')

        certification_formated = [certification.format()]
        return jsonify({
            "certification": certification_formated
        })

    @app.route('/certifications/<int:certification_id>', methods=["PATCH", "DELETE"])
    @login_required
    def implement_certification_by_id(payload, certification_id):
        certification = Certifications.query.filter(Certifications.id==certification_id).one_or_none()
        if certification is None:
            abort(404, 'So`ralgan sertifikat bazada mavjud emas.')

        if request.method == 'PATCH':
            teacher_id = request.form.get('teacher_id')
            title = request.form.get('title')
            given_by = request.form.get('given_by')
            credential = request.form.get('credential')
            file = request.files.get('image')

            if teacher_id:
                certification.teacher_id = teacher_id
            if title:
                certification.title = title
            if given_by:
                certification.given_by = given_by
            if credential:
                certification.credential = credential
            if file:
                if allowed_img(file.filename):
                    filename = file.filename
                    filename = str(uuid.uuid4()) + '.' + filename.split('.')[::-1][0]
                    filename = secure_filename(filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    img = (request.base_url).replace(url_for('certification_by_id', certification_id=certification_id), '/display/') + filename
                    certification.img = img
                else:
                    abort(415, 'Ruxsat etilmagan formatdagi fayl yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')
            
            try:
                certification.update()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')                
            
        if request.method == 'DELETE':
            try:
                certification.delete()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')

    @app.route('/awards')
    def all_awards():              

        awards = Awards.query.all()
        awards_formated = [a.format() for a in awards]
        count = len(awards_formated)

        return jsonify({
            "awards": awards_formated,
            "count": count
        })

    @app.route('/awards', methods=["POST"])
    @login_required
    def add_awards(payload):
        title = request.form.get('title')
        given_by = request.form.get('given_by', '')
        given_year = request.form.get('given_year', '')
        credential = request.form.get('credential', '')
        file = request.files.get('image')

        if title is None:
            abort(400, 'Mukofot nomini kiriting.')
        
        if file is None:
            img = ''
        if allowed_img(file.filename):
            filename = file.filename
            filename = str(uuid.uuid4()) + '.' + filename.split('.')[::-1][0]
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = (request.base_url).replace(url_for('all_awards'), '/display/') + filename
        else:
            abort(415, 'Ruxsat etilmagan formatdagi fayl yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')
        
        try:
            new_award = Awards(title, given_by, given_year, credential, img)
            new_award.insert()
            return jsonify({
                'success': True
            })
        except:
            db.session.rollback()
            abort(500, 'Serverda ichki xatolik.')

    @app.route('/awards/<int:award_id>')
    def award_by_id(award_id):
        award = Awards.query.filter(Awards.id==award_id).one_or_none()
        if award is None:
            abort(404, 'So`ralgan mukofot bazada mavjud emas.')                    
        
        award_formated = [award.format()]
        return jsonify({
            'award': award_formated
        })

    @app.route('/awards/<int:award_id>', methods=['PATCH', 'DELETE'])
    @login_required
    def implement_award_by_id(payload, award_id):
        award = Awards.query.filter(Awards.id==award_id).one_or_none()
        if award is None:
            abort(404, 'So`ralgan mukofot bazada mavjud emas.')

        if request.method == 'PATCH':
            title = request.form.get('title')
            given_by = request.form.get('given_by')
            given_year = request.form.get('given_year')
            credential = request.form.get('credential')
            file = request.files.get('image')
            
            if title:
                award.title = title
            if given_by:
                award.given_by = given_by
            if given_year:
                award.given_year = given_year
            if credential:
                award.credential = credential
            if file:
                if allowed_img(file.filename):
                    filename = file.filename
                    filename = str(uuid.uuid4()) + '.' + filename.split('.')[::-1][0]
                    filename = secure_filename(filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    img = (request.base_url).replace(url_for('award_by_id', '/display/')) + filename
                    award.img = img
                else:
                    abort(415, 'Ruxsat etilmagan formatdagi fayl yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')
            
            try:
                award.update()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')
        
        if request.method == 'DELETE':
            try:
                award.delete()
                return jsonify({
                    'success': True
                })
            except:
                db.session.rollback()
                abort(500, 'Serverda ichki xatolik.')

    #news uchun endpointlar
    @app.route('/news')
    def news():
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 8, type=int)
        all_news = News.query.order_by(News.id).all()
        all_news_formated = [news.format() for news in all_news]
        news_paginated = paginate(all_news_formated, limit, page)
        count = len(all_news_formated)

        return jsonify({
            "news": news_paginated,
            "count": count
        })

    @app.route('/news', methods=["POST"])
    def add_news():
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        image = request.files.get('image')
        video = request.files.get('video')

        if title is None or subtitle is None:
            abort(400, 'Yangilikka sarlavha va matn kiritilishi shart')
        if len(subtitle) == 0 or len(title) == 0:
            abort(400, "Bo'sh yangilik qabul qilinmaydi.")

        if image is None:
            img = ''
        elif allowed_img(image.filename):
            i_filename = image.filename
            i_filename = str(uuid.uuid4()) + '.' +i_filename.split('.')[::-1][0]
            i_filename = secure_filename(i_filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], i_filename))
            img = (request.base_url).replace(url_for('news'), '/display/') + i_filename
        else:
            abort(415, 'Fayl ruxsat etilmagan formatda yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')

        if video is None:
            video = ''
        elif allowed_video(video.filename):
            v_filename = video.filename
            v_filename = str(uuid.uuid4()) + '.' +v_filename.split('.')[::-1][0]
            v_filename = secure_filename(v_filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], v_filename))
            video = (request.base_url).replace(url_for('news'), '/display/') + v_filename
        else:
            abort(415, 'Fayl ruxsat etilmagan formatda yuborildi. Ruxsat etilgan formatlar: {ALLOWED_VIDEO_EXTENSIONS}')

        try:
            news = News(title, subtitle, img, video)
            news.insert()
            return jsonify({
                'success': True
            })
        except:
            db.session.rollback()
            abort(500, 'Serverda ichki xatolik.')

    @app.route('/news/<int:news_id>')
    def news_by_id(news_id):
        news = News.query.get(news_id)
        if not news:
            abort(404, "So`ralgan yangiliklar bazada mavjud emas.")

        news_formated = [news.format()]
        return jsonify({
            'news': news_formated
        })

    @app.route('/news/<int:news_id>', methods=['PATCH', 'DELETE'])
    @login_required
    def implement_news_by_id(payload, news_id):
        news = News.query.get(news_id)
        if not news:
            abort(404, "So`ralgan yangiliklar bazada mavjud emas.")

        if request.method=="PATCH":
            try:
                new_img = request.files.get('image')
                new_video = request.files.get('video')
                new_title = request.form.get('title')
                new_subtitle = request.form.get('subtitle')

                if new_img:
                    if allowed_img(new_img.filename):
                        i_filename = new_img.filename
                        i_filename = str(uuid.uuid4()) + '.' +i_filename.split('.')[::-1][0]
                        i_filename = secure_filename(i_filename)
                        new_img.save(os.path.join(app.config['UPLOAD_FOLDER'], i_filename))
                        img = (request.base_url).replace(url_for('news_by_id', news_id=news_id), '/display/') + i_filename
                        news.img = img
                    else:
                        abort(415, 'Fayl ruxsat etilmagan formatda yuborildi. Ruxsat etilgan formatlar: {ALLOWED_IMG_EXTENSIONS}')
                
                if new_video:
                    if allowed_video(new_video.filename):
                        v_filename = new_video.filename
                        v_filename = str(uuid.uuid4()) + '.' +v_filename.split('.')[::-1][0]
                        v_filename = secure_filename(v_filename)
                        new_video.save(os.path.join(app.config['UPLOAD_FOLDER'], v_filename))
                        video = (request.base_url).replace(url_for('news'), '/display/') + v_filename
                        news.video = video
                    else:
                        abort(415, 'Fayl ruxsat etilmagan formatda yuborildi. Ruxsat etilgan formatlar: {ALLOWED_VIDEO_EXTENSIONS}')
                
                if new_title:
                    news.title = new_title
                if new_subtitle:
                    news.subtitle = new_subtitle

                news.update()
            
                return jsonify({
                    'success': True,
                    })                   
            except:
                db.session.rollback()
                abort(500, "Serverda ichki xatolik")

        elif request.method=="DELETE":
            try:
                news.delete()

                return jsonify({
                    'success': True,
                })
            except:
                db.session.rollback()
                abort(422, 'Bazadan o`chirishda xatolik yuz berdi.')

    #murojat xatlari uchun endpointlar
    @app.route('/message', methods=['POST'])
    def send_message():
        data = request.get_json()

        email = data.get('email')
        phone = data.get('phone')
        title = data.get('title')
        text = data.get('text')

        if not email and not phone:
            abort(400, "Siz bilan bog'lanish uchun kontakt qoldiring.")
        
        try:
            new_message = Messages(email, phone, title, text, done=False)
            new_message.insert()
        except:
            abort(500, 'Serverda ichki xatolik.')
        return jsonify({
            'succuss': True
        })

    @app.route('/messages/all')
    @login_required
    def get_all_messages(payload):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 8, type=int)
        all_messages = Messages.query.all()
        messages_formated = [m.format() for m in all_messages]
        count = len(messages_formated)
        messages = paginate(messages_formated, limit, page)
        return jsonify({
            'messages': messages,
            'count': count
        })

    @app.route('/messages/new')
    @login_required
    def get_new_messages(payload):
        new_messages = Messages.query.filter(Messages.done==False).all()
        messages_formated = [m.format() for m in new_messages]
        count = len(messages_formated)
        return jsonify({
            'messages': messages_formated,
            'count': count
        })

    @app.route('/messages/old')
    @login_required
    def get_old_messages(payload):
        old_messages = Messages.query.filter(Messages.done==True).all()
        messages_formated = [m.format() for m in old_messages]
        count = len(messages_formated)
        return jsonify({
            'messages': messages_formated,
            'count': count
        })

    @app.route('/messages/<int:message_id>')
    @login_required
    def get_message_by_id(payload, message_id):
        message = Messages.query.filter(Messages.id==message_id).one_or_none()
        if not message:
            abort(404, 'Ushbu murojaat topilmadi.')

        message_formated = [message.format()]
        return jsonify({
            'messages': message_formated
        })

    @app.route('/messages/<int:message_id>', methods=['PATCH', 'DELETE'])
    @login_required
    def implement_messages(payload, message_id):
        message = Messages.query.filter(Messages.id==message_id).one_or_none()
        if not message:
            abort(404, 'Ushbu murojaat topilmadi.')
        
        if request.method == 'PATCH':
            data = request.get_json()
            done = data.get('done')

            if not done:
                abort(400, 'Belgilanganligi bildirilmadi.')
            try:
                message.done = done
                message.update()
            except:
                abort(500, 'Serverda ichki xatolik.')
            return jsonify({
                'success': True
            })
            
        if request.method == 'DELETE':
            try:
                message.delete()
            except:
                abort(500, 'Serverda ichki xatolik.')
            return jsonify({
                'success': True
            })

    #medialarni tasvirlash uchun endpoint
    @app.route('/display/<filename>')
    def media_display(filename):
        return redirect(url_for('static', filename=('/uploads/' + filename)), code=301)

    #errorlarni front endga chiroyli yetkazib berish uchun

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 400,
            'message': error.description
        }), 400
    
    @app.errorhandler(401)
    def unauthorize(error):
        return jsonify({
            'error': 401,
            'message': error.description
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': error.description
        }), 404
    
    @app.errorhandler(415)
    def unsupported_media_type(error):
        return jsonify({
            'error': 415,
            'message': error.description
        }), 415
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'error': 422,
            'message': error.description
        }), 422
    '''
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify ({
            'error': 500,
            'message': error.description
        }), 500
    '''
    return app

app = create_app()

if __name__=='__main__':
    app.run(debug=True)