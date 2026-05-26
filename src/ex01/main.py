from multiprocessing import Process, Queue, Manager, Lock
import time
import os

from read_files import read_students, read_examiners, read_questions
from workers import examiner_worker
from monitor import monitor, print_final


if __name__ == "__main__":
    examiners = read_examiners()
    students = read_students()
    questions = read_questions()

    manager = Manager()
    lock = Lock()

    shared_students = manager.list([
        manager.dict({"name": s.name, "gender": s.gender, "status": "Очередь", "start": 0, "end": 0})
        for s in students
    ])

    shared_questions = manager.list([
        manager.dict({"text": q.text, "success": 0})
        for q in questions
    ])

    stats = manager.dict({
        ex.name: manager.dict({"total": 0, "failed": 0, "time": 0.0})
        for ex in examiners
    })

    queue = Queue()
    for i in range(len(shared_students)):
        queue.put(i)

    start_time = time.time()

    monitor_process = Process(target=monitor, args=(shared_students, start_time))
    monitor_process.start()

    workers = []
    for ex in examiners:
        p = Process(
            target=examiner_worker,
            args=(ex.name, queue, shared_students, questions, shared_questions, stats)
        )
        workers.append(p)
        p.start()

    for p in workers:
        p.join()

    monitor_process.join()

    os.system('cls' if os.name == 'nt' else 'clear')

    print_final(shared_students, stats, shared_questions, start_time)