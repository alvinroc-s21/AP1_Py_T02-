import time
import random
from exam_logic import pass_exam

def examiner_worker(name, queue, students, questions, shared_questions, stats):
    while True:
        try:
            idx = queue.get_nowait()
        except:
            break

        students[idx]["status"] = "Сдает"
        students[idx]["start"] = time.time()

        time.sleep(random.uniform(len(name) - 1, len(name) + 1))

        result = pass_exam(students[idx], questions, shared_questions)

        students[idx]["end"] = time.time()
        students[idx]["status"] = "Сдал" if result else "Провалил"

        stats[name]["total"] += 1
        if not result:
            stats[name]["failed"] += 1

        stats[name]["time"] += students[idx]["end"] - students[idx]["start"]


