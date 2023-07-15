import datetime
import os

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, ValidationError
from sqlalchemy import DateTime
from sqlalchemy.sql import func

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Initializing flask application
app = Flask(__name__)

# Add SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASE_DIR, "db.sqlite3"
)

db = SQLAlchemy(app)

# Add Marshmallow
ma = Marshmallow(app)

app.app_context().push()


# Create the API model (SQLAlchemy)
class BookMarkModel(db.Model):
    __tablename__ = "bookmark"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    url = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __init__(self, title, url, description, created_at, updated_at):
        self.title = title
        self.url = url
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at


db.create_all()
db.session.commit()


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


# Create schema with object validation (marshmallow)
class BookMarkSchema(ma.Schema):
    title = fields.String(
        metadata={"required": True, "allow_none": False, "validate": must_not_be_blank}
    )
    url = fields.URL(
        metadata={
            "relative": True,
            "require_tld": True,
            "error": "invalid url representation",
        }
    )
    description = fields.String(metadata={"required": False, "allow_none": True})
    created_at = fields.DateTime(metadata={"required": False, "allow_none": True})
    updated_at = fields.DateTime(metadata={"required": False, "allow_none": True})

    class Meta:
        fields = ("id", "title", "description", "url", "created_at", "updated_at")


bookMarkSchema = BookMarkSchema()
bookMarksSchema = BookMarkSchema(many=True)

# API ROUTES


# Get all bookmarks
@app.route("/bookmarks/", methods=["GET"])
def book_marks():
    all_bookmarks = BookMarkModel.query.all()
    return jsonify(bookMarksSchema.dump(all_bookmarks))


# CREATE a bookmark
@app.route("/bookmark/", methods=["POST"])
def create_bookmark():
    title = request.json["title"]
    description = request.json["description"]
    url = request.json["url"]

    # Validate the data from request before serialization
    error = bookMarkSchema.validate(
        {"title": title, "description": description, "url": url}
    )
    if error:
        return jsonify(error)

    book_mark = BookMarkModel(
        title=title,
        description=description,
        url=url,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    try:
        json_input = request.get_json()
        result = bookMarkSchema.load(json_input)
    except ValidationError as err:
        return {"errors": err.messages}, 422

    db.session.add(book_mark)
    db.session.commit()
    return result, 201


# READ a particular bookmark
@app.route("/bookmark/<int:id>/", methods=["GET"])
def read_bookmark(id):
    book_mark = db.session.get(BookMarkModel, id)

    try:
        result = bookMarkSchema.dump(book_mark)
    except ValidationError as err:
        return err.messages, 422
    return result


# UPDATE a particular bookmark
@app.route("/bookmark/<int:id>/", methods=["PUT"])
def update_bookmark(id):
    title = request.json["title"]
    description = request.json["description"]
    url = request.json["url"]

    book_mark = BookMarkModel.query.get(id)
    book_mark.title = title
    book_mark.description = description
    book_mark.url = url

    # Validate the data from request before serialization
    error = bookMarkSchema.validate(
        {"title": title, "description": description, "url": url}
    )
    if error:
        return jsonify(error)
    try:
        result = bookMarkSchema.dump(book_mark)
    except ValidationError as err:
        return err.messages, 422

    db.session.add(book_mark)
    db.session.commit()
    return result


# DELETE a particular bookmark
@app.route("/bookmark/<int:id>/", methods=["DELETE"])
def delete_bookmark(id):
    book_mark = BookMarkModel.query.get(id)
    db.session.delete(book_mark)
    db.session.commit()
    return jsonify({"success": "True"})


# Serve the application
if __name__ == "__main__":
    app.run(debug=True)
