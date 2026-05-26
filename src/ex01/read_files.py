from models import Student, Examiner, Question

def read_examiners():
    with open("examiners.txt", encoding="utf-8") as f:
        data = f.read().split()
    return [Examiner(data[i], data[i + 1]) for i in range(0, len(data), 2)]

def read_students():
    with open("students.txt", encoding="utf-8") as f:
        data = f.read().split()
    return [Student(data[i], data[i + 1]) for i in range(0, len(data), 2)]

def read_questions():
    questions = []
    with open("questions.txt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(Question(line))
    return questions
