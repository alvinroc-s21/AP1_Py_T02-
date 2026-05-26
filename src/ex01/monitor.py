import time
from prettytable import PrettyTable

def monitor(students, start_time):
    first = True

    while True:
        table = PrettyTable()
        table.field_names = ["Студент", "Статус"]

        order = {"Очередь": 0, "Сдает": 1, "Сдал": 2, "Провалил": 3}
        sorted_students = sorted(students, key=lambda x: order[x["status"]])

        for s in sorted_students:
            table.add_row([s["name"], s["status"]])

        output = str(table)

        remaining = sum(1 for s in students if s["status"] in ["Очередь", "Сдает"])
        output += f"\n\nОсталось: {remaining}/{len(students)}"
        output += f"\nВремя: {time.time() - start_time:.2f} сек"

        if first:
            print(output)
            first = False
        else:
            lines = output.count("\n") + 1
            print(f"\033[{lines}A", end="")
            print(output)

        if remaining == 0:
            break

        time.sleep(0.2)

def print_final(students, stats, questions, start_time):

    table = PrettyTable()
    table.field_names = ["Студент", "Статус"]

    sorted_students = sorted(students, key=lambda s: 0 if s["status"] == "Сдал" else 1)

    for s in sorted_students:
        table.add_row([s["name"], s["status"]])

    print(table)

    table_ex = PrettyTable()
    table_ex.field_names = ["Экзаменатор", "Всего", "Завалил", "Время"]

    for ex in stats:
        table_ex.add_row([ex, stats[ex]["total"], stats[ex]["failed"], f"{stats[ex]['time']:.2f}"])

    print(table_ex)

    total_time = time.time() - start_time
    print(f"\nОбщее время: {total_time:.2f} сек")

    times = [
        (s["name"], s["end"] - s["start"])
        for s in students
        if s["status"] == "Сдал" and s["end"] > 0
    ]

    if times:
        min_time = min(t[1] for t in times)
        best_students = [t[0] for t in times if t[1] == min_time]
    else:
        best_students = []

    print("Лучшие студенты:", ", ".join(best_students) if best_students else "нет")

    ratios = {
        ex: (stats[ex]["failed"] / stats[ex]["total"] if stats[ex]["total"] else float("inf"))
        for ex in stats
    }

    min_ratio = min(ratios.values())
    best_ex = [ex for ex in ratios if ratios[ex] == min_ratio]

    print("Лучшие экзаменаторы:", ", ".join(best_ex))

    failed = [s for s in students if s["status"] == "Провалил"]
    expelled = min(failed, key=lambda s: s["end"])["name"] if failed else "нет"

    print("Отчислят:", expelled)

    if questions:
        max_success = max(q["success"] for q in questions)
        best_q = [q["text"] for q in questions if q["success"] == max_success]
    else:
        best_q = []

    print("Лучшие вопросы:", ", ".join(best_q))

    passed = sum(1 for s in students if s["status"] == "Сдал")
    percent = passed / len(students)

    print(f"\nСдали: {passed}/{len(students)} ({percent * 100:.1f}%)")
    print("Экзамен удался" if percent > 0.85 else "Экзамен не удался")