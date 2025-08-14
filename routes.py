from flask import current_app as app
from flask import render_template, url_for, request, redirect, session , send_file
from models import db, User, Section, Book, Admin , Request_book ,Feedback
from datetime import datetime, timedelta
import matplotlib .pyplot as plt
import matplotlib
from collections import Counter
matplotlib.use("Agg")
from sqlalchemy import text


@app.route('/')
def index():
    return render_template('user_login.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


@app.route('/admin_login', methods=['POST'])
def admin_login_POST():
    username = request.form.get("username")
    password = request.form.get("password")
    admin = Admin.query.filter_by(username=username).first()

    if not username or not password:
        return redirect(url_for("admin_login"))
    
    if not admin or not admin.check_password(password):
        return redirect(url_for("admin_login"))
    
    session["user_id"] = admin.id

    return redirect(url_for("admin_dashboard"))


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    parameter = request.args.get('parameter')  
    query = request.args.get('query')

    if parameter == 'Title' and query:  
        sections = Section.query.filter(Section.title.ilike(f'%{query}%')).all() 
    else:
        sections = Section.query.all()
    
    return render_template('admin_dashboard.html', admin=Admin.query.get(session['user_id']), sections=sections)


@app.route('/admin_dashboard/update_section/<int:id>', methods=['GET', 'POST'])
def update_section(id):
    if 'user_id' not in session:
        return redirect(url_for(admin_login))
    section = Section.query.get(id)
    if request.method == 'POST':
        section.title = request.form['title']
        section.image = request.form['image']
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_dashboard.html', section=section)

@app.route('/admin_dashboard/remove_section/<int:id>', methods=['POST'])
def remove_section(id):
    if 'user_id' not in session:
        return redirect(url_for(admin_login))
    
    if  request.method == "POST":
        section = Section.query.get(id)

        if section:
            Book.query.filter_by(section_id=id).delete()
            
        db.session.delete(section)
        db.session.commit()

    return redirect(url_for('admin_dashboard'))
    
@app.route('/admin/add_section', methods=['POST'])
def add_section():
    if 'user_id' not in session:
        return redirect(url_for(admin_login))
    title = request.form.get('title')
    image = request.form.get('image')

    new_section = Section(title=title, image=image)

    db.session.add(new_section)
    db.session.commit()

    return redirect(url_for('admin_dashboard'))


@app.route('/books',methods=['GET','POST'])
def show_books():
    books=Book.query.all()
    if 'user_id' not in session:
        return redirect(url_for(admin_login))
    return render_template('books.html',admin=User.query.get(session['user_id']),books=books)


@app.route('/books/view_books/<int:id>',methods=['GET','POST'])
def view_books(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login')) 
    section = Section.query.get(id)
    parameter = request.args.get('parameter')  
    query = request.args.get('query')

    if parameter == 'Title' and query:  
        books = Book.query.filter(Book.name.ilike(f'%{query}%')).all() 
    elif parameter == 'Author' and query: 
        books = Book.query.filter(Book.author.ilike(f'%{query}%')).all()
    else:
        books = Book.query.filter_by(section_id=id).all() 

    return render_template('books.html',books=books,section=section,section_id=id)

@app.route('/add_book/<int:section_id>',methods=['POST','GET'])
def add_book(section_id):
    if 'user_id' not in session:
        return redirect(url_for(admin_login))
    if request.method == 'POST':
        name=request.form.get('name')
        author=request.form.get('author')
        file=request.form.get('file')
        image=request.form.get('image')

    if not name or not author or not file:
        return redirect(url_for('view_books',id=section_id))

    new_book=Book(name=name,author=author,file=file,image=image , section_id = section_id)

    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('view_books' ,id=section_id))

@app.route('/books/remove_book/<int:id>', methods=['POST'])
def remove_book(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        book = Book.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()

    return redirect(url_for('view_books', id=book.section_id))


@app.route('/books/edit_book/<int:id>',methods=['GET','POST'])
def edit_book(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    book = Book.query.get(id)
    
    if not book:
        return  redirect(url_for('books'))
    
    if request.method =='POST':
        
        book.name=request.form.get('name')
        book.author=request.form.get('author')
        book.file=request.form.get('file')
        book.image=request.form.get('image')


        db.session.commit()

        return redirect(url_for('view_books' , id=book.section_id))
    
    return render_template('books.html', section_id=book.section_id , book=book)

@app.route('/books/view_pdf/<int:id>',methods=['GET'])
def view_pdf(id):

    book = Book.query.get(id)

    book_file= book.file 


    return send_file(book_file, mimetype='application/pdf')

# ********************************************************************************************************

@app.route('/user_login')
def user_login():
    return render_template('user_login.html')


@app.route('/user_login',methods=['POST'])
def user_login_POST():
    username=request.form.get("username")
    password=request.form.get("password")
    user=User.query.filter_by(username=username).first()

    if not username or not password:
        return redirect(url_for("user_login"))
    
    if not user or not user.check_password(password):
        return redirect(url_for("user_login"))
    
    session["user_id"]=user.id
    return redirect(url_for("user_dashboard"))

@app.route('/user_dashboard',methods=['POST','GET'])
def  user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    
    books = Book.query.all()
    feedback = Feedback.query.all()
    print(feedback)

    parameter = request.args.get('parameter')  
    query = request.args.get('query')

    if parameter == 'Title' and query:  
        sections = Section.query.filter(Section.title.ilike(f'%{query}%')).all() 
    else:
        sections = Section.query.all() 
   
    return render_template("user_dashboard.html",user=User.query.get(session['user_id']),Section=sections , books= books , feedback=feedback)


@app.route('/user_books', methods=['GET','POST'])
def user_books():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    sections = Section.query.all()
    books = Book.query.all()
    # feedbacks = Feedback.query.all()

    return render_template('books.html', user=User.query.get(session['user_id']), sections=sections, books=books)


@app.route('/user_books/show_user_books/<int:id>', methods=['POST','GET'])
def show_user_books(id):
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    sections = Section.query.get(id)

    parameter = request.args.get('parameter')  
    query = request.args.get('query')

    if parameter == 'Title' and query:  
        books = Book.query.filter(Book.name.ilike(f'%{query}%')).all() 
    elif parameter == 'Author' and query: 
        books = Book.query.filter(Book.author.ilike(f'%{query}%')).all()
    else:
        books = Book.query.filter_by(section_id=id).all() 


    return render_template('user_books.html', sections=sections, books=books , section_id=id)

@app.route('/books/user_request_book/<int:book_id>', methods = ['POST', 'GET'])
def user_request_book(book_id):
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    
    user_id = session['user_id']
    
    if Request_book.query.filter_by(user_id=session['user_id'], book_status='accepted').count() >= 5:

        return redirect(url_for('user_dashboard'))
    
    if Request_book.query.filter_by(user_id=user_id , book_id=book_id , book_status = "accepted").first():
        return redirect(url_for('user_dashboard'))
    
    newRequest = Request_book(user_id = user_id , book_id=book_id)

    db.session.add(newRequest)
    db.session.commit()

    book = Book.query.get(book_id)
    return redirect(url_for('show_user_books', id=book.section_id))

@app.route('/admin/view_request')
def view_request():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
     
    book_requests = Request_book.query.filter_by(book_status='pending').all()
    
    return render_template('request.html', book_requests=book_requests, User = User, Book=Book)



@app.route('/admin/accept_request/<int:request_id>', methods=['POST' , 'GET'])
def accept_request(request_id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    request_book = Request_book.query.get(request_id)
    if not request_book:
        return redirect(url_for('view_request'))

    if request.method == 'POST':
        # Update request status to accepted
        request_book.book_status = 'accepted'

        # Get user and book associated with the request
        user = User.query.get(request_book.user_id)
        book = Book.query.get(request_book.book_id)

        if user and book:
            user.books_issued.append(book)
            request_book.return_date = datetime.now() + timedelta(days=7)

            # Commit changes to the database
            db.session.commit()

    return redirect(url_for('view_request'))

@app.route('/admin/reject_request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    request_book = Request_book.query.get(request_id)
    if not request_book:
        return redirect(url_for('view_request'))

    request_book.book_status = 'rejected'
    db.session.commit()

    return redirect(url_for('view_request'))



@app.route('/submit_feedback',methods=['POST'])
def submit_feedback():
    if request.method =='POST':
        book_id=request.form['book_id']
        feedback_comment=request.form['feedback']

        user_id=session.get('user_id')

        feedback=Feedback(book_id=book_id,user_id=user_id,feedback=feedback_comment)
        db.session.add(feedback)
        db.session.commit()

        return redirect(url_for('library'))


# @app.route('/submit_feedback', methods=['POST'])
# def submit_feedback():
#     if request.method == 'POST':
#         book_id = request.form.get('book_id')
#         feedback = request.form.get('feedback')
#         user_id = session.get('user_id')

#         return redirect(url_for('library'))


@app.route('/library')
def library():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    my_books = user.books_issued
    for book in  my_books:
        request = Request_book.query.filter_by(user_id=user_id, book_id=book.id, book_status='accepted').first()
        if request and request.return_date and request.return_date < datetime.now():
        
            user.books_issued.remove(book)
    return render_template('my_books.html',  my_books= my_books)

@app.route('/my_books/show_pdf/<int:id>',methods=['GET'])
def show_pdf(id):

    book = Book.query.get(id)
    if book is None:
        return redirect(url_for('library'))

    book_file= book.file 

    return send_file(book_file, mimetype='application/pdf')


@app.route('/new_registeration')
def new_registeration():
    return render_template('new_user_registeration.html')

@app.route('/new_registeration', methods=['POST'])
def new_registeration_post():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        used_username = User.query.filter_by(username = username).first()
        if used_username:
            return redirect(url_for(new_registeration))
    
        used_email = User.query.filter_by(email=email).first()
        if used_email:
            return redirect(url_for(new_registeration))
    
        new_reader = User(username = username, password = password,  email=email, registration_date = datetime.now())

        db.session.add(new_reader)
        db.session.commit()

        return redirect(url_for('user_login'))
    
    return render_template('new_user_registeration.html')


@app.route('/return_book/<int:id>',methods=['GET','POST'])
def return_book(id):
    if 'user_id' not in session:
        return  redirect(url_for('user_login'))
    
    user_id=session['user_id']

    request_book=Request_book.query.filter_by(user_id=user_id,book_id=id,book_status='accepted').first()

    if not request_book:
        return redirect(url_for('library'))
    
    request_book.book_status='returned'


    user=User.query.get(user_id)
    book=Book.query.get(id)
    user.books_issued.remove(book)

    db.session.commit()

    return redirect(url_for('library'))

@app.route('/info')
def info():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    readers = User.query.all()

    return render_template("info.html", readers=readers)

@app.route('/info/revoke/<int:reader_id>/<int:book_id>',methods=[ "POST" ] )
def revoke(reader_id,book_id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        user = User.query.get(reader_id)
        book = Book.query.get(book_id)
    if user and book:
        if book in user.books_issued:
            user.books_issued.remove(book)
            db.session.commit()

    return redirect(url_for('info'))
    

@app.route('/admin_stats')
def admin_stats():

    total_books_issued=len(Request_book.query.filter_by(book_status="accepted").all())
    total_books_rejected=len(Request_book.query.filter_by(book_status="rejected").all())
    total_pending_books=len(Request_book.query.filter_by(book_status="pending").all())

    book_requests = Request_book.query.all()
    
    status_counts = Counter(request.book_status for request in book_requests)

    statuses = list(status_counts.keys())
    counts = list(status_counts.values())

    plt.clf()
    
    plt.bar(statuses, counts, color="skyblue")
    plt.title('Book Request Status')
    plt.xlabel('Status')
    plt.ylabel('Number of Requests')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/book_request_status.png')

    return render_template("admin_stats.html",total_books_issued=total_books_issued,total_books_rejected=total_books_rejected,total_pending_books=total_pending_books)
