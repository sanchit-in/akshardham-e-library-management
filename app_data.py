from flask import current_app as app
from models import db, User, Book, Section, Admin
from datetime import datetime

# def delete_feedback():
#     feedback = Feedback.query.all()
#     print("Total feedback records:", len(feedback))
#     for f in feedback:
#         print("Deleting feedback:", f.id)
#         db.session.delete(f)
#     db.session.commit()
#     print("Feedback deletion completed.")

def data():
        # Setting up admin
        admin = Admin.query.filter_by(username="admin").first()
        if not admin:
            admin = Admin(username='admin', password='pass')
            db.session.add(admin)
            db.session.commit()

        # Setting up sections
        # sections = [
        #     Section(title="fiction", image="static/covers/fiction.jpg"),
        #     Section(title="non-fiction", image="static/covers/non-fiction.jpg")
        # ]
        # for section in sections:
        #     db.session.add(section)
        # db.session.commit()

        # Setting up books
        books = [
            Book(name="Python Programming", section_id=2, author="John Doe", file="static/pdfs/book.pdf", image="static/covers/python.jpg"),
            Book(name="Machine Learning for Beginners", section_id=2, author="Emily Johnson", file="static/pdfs/book.pdf", image="static/covers/ml.jpg")
        ]
        for book in books:
            db.session.add(book)
        db.session.commit()

        # Setting up users
        users = [
            User(username='reader1', password='pass1', name='test1', email='test1@gmail.com', registration_date=datetime.now()),
            User(username='reader2', password='pass2', name='test2', email='test2@gmail.com', registration_date=datetime.now())
        ]
        for user in users:
            existing_user = User.query.filter_by(email=user.email).first()
            if not existing_user:
                db.session.add(user)
        db.session.commit()
