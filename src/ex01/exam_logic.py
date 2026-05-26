import random

def choose_word(words, gender):
    phi = 1.618
    weights = []
    remaining = 1.0

    for _ in range(len(words)):
        w = remaining / phi
        weights.append(w)
        remaining -= w

    weights[-1] += remaining

    if gender == "Ж":
        weights.reverse()

    return random.choices(words, weights=weights)[0]

def choose_correct_answers(words):
    correct = set()
    for word in words:
        correct.add(word)
        if random.random() > 1 / 3:
            break
    return correct

def evaluate(student, questions, shared_questions):
    correct = 0
    wrong = 0

    selected = random.sample(range(len(questions)), 3)

    for q_idx in selected:
        q = questions[q_idx]
        answer = choose_word(q.words, student["gender"])
        correct_answers = choose_correct_answers(q.words)

        if answer in correct_answers:
            correct += 1
            shared_questions[q_idx]["success"] += 1
        else:
            wrong += 1

    return correct, wrong

def final_decision(correct, wrong):
    mood = random.random()
    if mood < 1 / 8:
        return False
    elif mood < 3 / 8:
        return True
    return correct > wrong

def pass_exam(student, questions, shared_questions):
    correct, wrong = evaluate(student, questions, shared_questions)
    return final_decision(correct, wrong)