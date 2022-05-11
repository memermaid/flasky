from app import db

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    color = db.Column(db.String)

# class Cat:
#     def __init__(self, id, name, age, color):
#         self.id = id
#         self.name = name
#         self.age = age
#         self.color = color

