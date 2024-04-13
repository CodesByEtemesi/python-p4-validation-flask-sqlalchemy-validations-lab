from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @staticmethod
    def validate_name(_, name):
        if not name:
            raise ValueError("Author must have a name.")

    @staticmethod
    def validate_phone_number(_, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError("Phone number must be exactly ten digits.")

    @staticmethod
    def validate_unique_name(_, name):
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            raise ValueError("An author with this name already exists.")

    @db.validates('name')
    def validate_name(self, key, name):
        self.validate_name(key, name)
        self.validate_unique_name(key, name)
        return name

    @db.validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        self.validate_phone_number(key, phone_number)
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @staticmethod
    def validate_title(_, title):
        if not any(keyword in title for keyword in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Title must be sufficiently clickbait-y.")

    @staticmethod
    def validate_content(_, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")

    @staticmethod
    def validate_summary(_, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")

    @staticmethod
    def validate_category(_, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either Fiction or Non-Fiction.")

    @db.validates('title')
    def validate_title(self, key, title):
        self.validate_title(key, title)
        return title

    @db.validates('content')
    def validate_content(self, key, content):
        self.validate_content(key, content)
        return content

    @db.validates('summary')
    def validate_summary(self, key, summary):
        self.validate_summary(key, summary)
        return summary

    @db.validates('category')
    def validate_category(self, key, category):
        self.validate_category(key, category)
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
