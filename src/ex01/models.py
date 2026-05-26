class Student:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Examiner:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Question:
    def __init__(self, text):
        self.text = text
        self.words = text.split()