class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        self.assigned_subjects = set()


def get_subjects():
    return {
        'Математика',
        'Фізика',
        'Хімія',
        'Інформатика',
        'Біологія'
    }


def get_teachers():
    return [
        Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com', {'Математика', 'Фізика'}),
        Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com', {'Хімія'}),
        Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com', {'Інформатика', 'Математика'}),
        Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}),
        Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}),
        Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com', {'Біологія'}),
    ]


def create_schedule(subjects, teachers):
    uncovered_subjects = subjects.copy()
    schedule = []

    while uncovered_subjects:
        best_teacher = None
        best_subjects = set()

        for teacher in teachers:
            available_subjects = teacher.can_teach_subjects & uncovered_subjects

            if not available_subjects:
                continue

            if (
                len(available_subjects) > len(best_subjects)
                or (
                    len(available_subjects) == len(best_subjects)
                    and best_teacher is not None
                    and teacher.age < best_teacher.age
                )
            ):
                best_teacher = teacher
                best_subjects = available_subjects

        if best_teacher is None:
            return None

        best_teacher.assigned_subjects = best_subjects
        schedule.append(best_teacher)

        uncovered_subjects -= best_subjects
        teachers.remove(best_teacher)

    return schedule


def print_schedule(schedule):
    if schedule:
        print("Розклад занять:")

        for teacher in schedule:
            print(
                f"{teacher.first_name} {teacher.last_name}, "
                f"{teacher.age} років, email: {teacher.email}"
            )
            print(
                f"   Викладає предмети: "
                f"{', '.join(sorted(teacher.assigned_subjects))}\n"
            )
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")


if __name__ == '__main__':
    subjects = get_subjects()
    teachers = get_teachers()

    schedule = create_schedule(subjects, teachers)

    print_schedule(schedule)