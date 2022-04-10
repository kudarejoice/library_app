from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {
        'title': 'Pride and Prejudice',
        'author_name': 'Jane Austen',
        'isbn_number': '9780140430721',
        'genre': 'Romance'
        }

@api.route('/book', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author_name = request.json['author_name']
    isbn_number = request.json['isbn_number']
    genre = request.json['genre']
    user_token = current_user_token.token

    print(f'Book Added: {current_user_token.token}')

    book = Book(title, author_name, isbn_number, genre, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/book', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_book = current_user_token.token
    books = Book.query.filter_by(user_token = a_book).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/book/<id>', methods = ['GET'])
@token_required
def get_book_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        search = Book.query.get(id)
        response = book_schema.dump(search)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401


@api.route('/book/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    search = Book.query.get(id) 
    search.title = request.json['title']
    search.author_name = request.json['author_name']
    search.isbn_number = request.json['isbn_number']
    search.genre = request.json['genre']
    search.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(search)
    return jsonify(response)

@api.route('/book/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    book.user_token = current_user_token.token
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)
