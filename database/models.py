import email
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
import os
from dotenv import load_dotenv
from sqlalchemy.sql.schema import ForeignKey

load_dotenv()

#local run qilinganda olib tashlang.
database_path = os.getenv("DATABASE_URL")
if database_path and database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

#local run qilinganda kamment holatidan chiqaring
#database_path = 'postgresql://{}:{}@localhost:5432/yi'.format(os.getenv("USER"), os.getenv("PASSWORD"))

db = SQLAlchemy()

def create_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI']=database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    db.create_all()

class Categories(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    courses = db.relationship('Courses', backref='categories')

    def __init__(self, name):
        self.name = name
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id': self.id,
            'name': self.name
        }

class Courses(db.Model):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey(Categories.id), nullable=False)
    title = Column(String, nullable=False)
    img = Column(String, unique=True)
    description = Column(String, nullable=True)
    individuals = db.relationship('Individuals', backref='courses')
    groups = db.relationship('Groups', backref='courses')

    def __init__(self, category_id, title, img, description):
        self.category_id = category_id
        self.title = title
        self.img = img
        self.description = description
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title,
            'img': self.img,
            'description': self.description
        }
    
class Teachers(db.Model):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    description = Column(String)
    img = Column(String)
    individuals = db.relationship('Individuals', backref='teachers')
    groups = db.relationship('Groups', backref='teachers')
    certifications = db.relationship('Certifications', backref='teachers')

    def __init__(self, first_name, last_name, description, img):
        self.first_name = first_name
        self.last_name = last_name
        self.description = description
        self.img = img
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'description': self.description,
            'img': self.img
        }

class Individuals(db.Model):
    __tablename__ = 'individuals'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(Courses.id), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teachers.id), nullable=False)
    members = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    start = Column(String, default='--')
    end = Column(String, default='--')
    duration = Column(Integer, nullable=True)
    days = Column(String, default='--')
    in_month = Column(Integer, nullable=True)
    active = Column(Boolean, default=False, nullable=False)

    def __init__(self, course_id, teacher_id, members, price, start, end, duration, days, in_month, active):
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.members = members
        self.price = price
        self.start = start
        self.end = end
        self.duration = duration
        self.days = days
        self.in_month = in_month
        self.active = active
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'teacher_id': self.teacher_id,
            'members' : self.members,
            'price': self.price,
            'start': self.start,
            'end': self.end,
            'duration': self.duration,
            'days': self.days,
            'in_month': self.in_month,
            'active': self.active
        }

class Groups(db.Model):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey(Courses.id), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teachers.id), nullable=False)
    members = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    start = Column(String, default='belgilanmagan')
    end = Column(String, default='belgilanmagan')
    duration = Column(Integer, nullable=True)
    days = Column(String, default='belgilanmagan')
    in_month = Column(Integer, nullable=True)
    active = Column(Boolean, default=False, nullable=False)

    def __init__(self, course_id, teacher_id, members, price, start, end, duration, days, in_month, active):
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.members = members
        self.price = price
        self.start = start
        self.end = end
        self.duration = duration
        self.days = days
        self.in_month = in_month
        self.active = active
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'teacher_id': self.teacher_id,
            'members' : self.members,
            'price': self.price,
            'start': self.start,
            'end': self.end,
            'duration': self.duration,
            'days': self.days,
            'in_month': self.in_month,
            'active': self.active
        }
    
class Certifications(db.Model):
    __tablename__ = 'certifications'

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey(Teachers.id), nullable=True)
    title = Column(String, nullable=False)
    given_by = Column(String)
    credential = Column(String)
    img = Column(String)

    def __init__(self, teacher_id, title, given_by, credential, img):
        self.teacher_id = teacher_id
        self.title = title
        self.given_by = given_by
        self.credential = credential
        self.img = img
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'title': self.title,
            'given_by': self.given_by,
            'credential': self.credential,
            'img': self.img
        }

class Awards(db.Model):
    __tablename__ = 'awards'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    given_by = Column(String)
    given_year = Column(String)
    credential = Column(String)
    img = Column(String)

    def __init__(self, title, given_by, given_year, credential, img):
        self.title = title
        self.given_by = given_by
        self.given_year = given_year
        self.credential = credential
        self.img = img
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'given_by': self.given_by,
            'given_year': self.given_year,
            'credential': self.credential,
            'img': self.img
        }

class News(db.Model):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    img = Column(String)
    video = Column(String)
    title = Column(String)
    subtitle = Column(String)

    def __init__(self, title, subtitle, img, video):
        self.title = title
        self.subtitle = subtitle
        self.img = img
        self.video = video

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'img': self.img,
            'video': self.video,
            'title': self.title,
            'subtitle': self.subtitle
        }

class Messages(db.Model):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    done = Column(Boolean, nullable=False ,default=False)

    def __init__(self, email, phone, title, text, done):
        self.email = email
        self.phone = phone
        self.title = title
        self.text = text
        self.done = done

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'title': self.title,
            'text': self.text,
            'done': self.done
        }
    
class Contacts(db.Model):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    phone = Column(String, default='')
    wt = Column(String, default='')
    email = Column(String, default='')
    s_links = Column(String, default='')
    address = Column(String, default='')
    ref_point = Column(String, default='')
    lat = Column(String, default='')
    lon = Column(String, default='')

    def __init__(self, phone='', wt='', email='', s_links='', address='', ref_point='', lat='', lon=''):
        self.phone = phone
        self.wt = wt
        self.email = email
        self.s_links = s_links
        self.address = address
        self.ref_point = ref_point
        self.lat = lat
        self.lon = lon
    
    def update(self):
        db.session.commit()
    
    def format(self):
        return {
            "phone":  self.phone,
            "wt": self.wt,
            "email" : self.email,
            "s_links" : self.s_links,
            "address" : self.address,
            "ref_point" : self.ref_point,
            "lat" : self.lat,
            "lon" : self.lon
        }