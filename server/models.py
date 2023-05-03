from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if name == '':
            raise ValueError("Author must haave a name")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10:
            raise ValueError("Phone number is not 10 digits")
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'



class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    
    #### Refactored Validation for Title ####
    # @validates('title')
    # def validate_title(self, key, title):
    #     clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
    #     if not any(substring in title for substring in clickbait):
    #         raise ValueError("No clickbait found")
    #     return title
    
    @validates("title")
    def validate_title(self, key, title):
        if title == '' and ("Won't Believe" not in title) or ("Secret" not in title) or ("Top" not in title) or ("Guess" not in title):
            raise ValueError("Each post must have a title")
        return title
    
    #### Why won't seperate validations work for summary? ####
    # @validates("summary")
    # def validate_content(self, key, summary):
    #     if len(summary) >= 250:
    #         raise ValueError("Summary can not be more than 250 characters")
    #     return summary

    @validates("content")
    def validate_content(self, key, value):
        if key == 'content':
            if len(value) <= 250:
               raise ValueError("Content must be at least 250 characters")
        # if key == 'summary':
        #     if len(value) >= 250:
        #         raise ValueError("Summary can not be more than 250 characters")
            
        return value
    
    @validates("summary")
    def validate_content(self, key, summary):
        if len(summary) >= 250:
            raise ValueError("Summary can not be more than 250 characters")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
