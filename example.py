"""
Полный пример использования TopJournalSDK.

Complete example of using TopJournalSDK.

Краткая версия для старта — в README (раздел «Быстрый старт»).
Short version to start with lives in README ("Быстрый старт" section).
"""

import asyncio
from collections.abc import Awaitable, Callable
from datetime import date

from top_journal_sdk import TopJournalSDK

StepFunc = Callable[[TopJournalSDK], Awaitable[None]]


async def run_step(title: str, step: StepFunc, sdk: TopJournalSDK) -> None:
    """Выполняет шаг демо с заголовком и перехватом ошибок."""
    print(f"\n{title}")
    print("-" * 30)
    try:
        await step(sdk)
    except Exception as exc:
        print(f"❌ Ошибка: {exc}")


async def demo_user_info(sdk: TopJournalSDK):
    """Шаг 2: информация о пользователе."""
    user_info = await sdk.user.get_personal_info()
    print(f"Полное имя: {user_info.full_name}")
    print(f"Группа: {user_info.group_name}")
    print(f"Поток: {user_info.stream_name}")
    print(f"Топ коины: {user_info.top_coins}")
    print(f"Топ гемы: {user_info.top_gems}")
    print(f"Возраст: {user_info.age}")
    print(f"Дата рождения: {user_info.birthday}")
    print(f"Дата регистрации: {user_info.registration_date}")


async def demo_grades(sdk: TopJournalSDK):
    """Шаг 3: оценки и успеваемость."""
    try:
        average_grades = await sdk.grades.get_average_grades()
        print(f"Количество средних оценок: {len(average_grades.grade_list)}")
        for i, grade in enumerate(average_grades.grade_list[:5]):  # Первые 5
            print(f"  Оценка {i + 1}: {grade.points} (дата: {grade.date})")
    except Exception as e:
        print(f"❌ Ошибка получения средних оценок: {e}")

    try:
        attendance_grades = await sdk.grades.get_class_attendance_grades()
        print(
            "Количество оценок за посещаемость: "
            f"{len(attendance_grades.class_attendance_grade_list)}"
        )
        for i, grade in enumerate(attendance_grades.class_attendance_grade_list[:3]):
            print(f"  Посещаемость {i + 1}: {grade.status_was} ({grade.date_visit})")
    except Exception as e:
        print(f"❌ Ошибка получения оценок за посещаемость: {e}")


async def demo_attendance(sdk: TopJournalSDK):
    """Шаг 4: посещаемость."""
    attendance_data = await sdk.attendance.get_attendances()
    print(f"Количество записей о посещаемости: {len(attendance_data.attendance_list)}")
    for i, att in enumerate(attendance_data.attendance_list[:5]):
        print(f"  Посещаемость {i + 1}: {att.points} (дата: {att.date})")


async def demo_homework(sdk: TopJournalSDK):
    """Шаг 5: домашние задания."""
    homeworks = await sdk.homework.get_homeworks()
    print(f"Всего домашних заданий: {homeworks.total}")
    print(f"Просрочено: {homeworks.overdue}")
    print(f"Проверено: {homeworks.checked}")
    print(f"На проверке: {homeworks.pending}")
    print(f"Текущие: {homeworks.current}")
    print(f"Удалено: {homeworks.deleted}")


async def demo_schedule(sdk: TopJournalSDK):
    """Шаг 6: расписание на сегодня."""
    schedule = await sdk.schedule.get_schedule_by_date(date.today())
    print(f"Количество уроков на сегодня: {len(schedule.lesson_list)}")

    for lesson in schedule.lesson_list:
        print(f"  Урок {lesson.lesson}: {lesson.subject_name}")
        print(f"    Время: {lesson.started_at} - {lesson.finished_at}")
        print(f"    Учитель: {lesson.teacher_name}")
        print(f"    Аудитория: {lesson.room_name}")
        print()


async def demo_feedback(sdk: TopJournalSDK):
    """Шаг 7: отзывы о студенте."""
    reviews = await sdk.feedback.get_student_reviews()
    print(f"Количество отзывов: {len(reviews.review_list)}")

    for i, review in enumerate(reviews.review_list[:3]):  # Показать первые 3
        print(f"  Отзыв {i + 1}:")
        print(f"    Дата: {review.date}")
        print(f"    Учитель: {review.teacher}")
        print(f"    Предмет: {review.spec}")
        print(f"    Сообщение: {review.message}")
        print()


async def demo_evaluation_lessons(sdk: TopJournalSDK):
    """Шаг 8: уроки для оценки."""
    evaluation_lessons = await sdk.lesson_evaluation.get_evaluation_lessons()
    print(f"Уроков для оценки: {len(evaluation_lessons.evaluation_list)}")

    for i, lesson in enumerate(evaluation_lessons.evaluation_list[:3]):
        print(f"  Урок {i + 1}:")
        print(f"    Дата: {lesson.date_visit}")
        print(f"    Учитель: {lesson.fio_teach}")
        print(f"    Предмет: {lesson.spec_name}")
        print()


async def demo_evaluation_tags(sdk: TopJournalSDK):
    """Шаг 9: теги для оценки."""
    lesson_tags = await sdk.lesson_evaluation.get_evaluation_lesson_tags("evaluation_lesson")
    print(f"Тегов для оценки урока: {len(lesson_tags.evaluation_tags)}")

    teach_tags = await sdk.lesson_evaluation.get_evaluation_lesson_tags("evaluation_lesson_teach")
    print(f"Тегов для оценки преподавания: {len(teach_tags.evaluation_tags)}")


async def demo_leaderboards(sdk: TopJournalSDK):
    """Шаг 10: рейтинги."""
    group_leaderboard = await sdk.leaderboard.get_group_leaderboards()
    print(f"Рейтинг групп: {len(group_leaderboard.group_leaderboard_list)} человек")

    for i, member in enumerate(group_leaderboard.group_leaderboard_list[:3]):
        print(f"  {i + 1}. {member.full_name} - {member.amount} баллов")

    print()

    stream_leaderboard = await sdk.leaderboard.get_stream_leaderboards()
    print(f"Рейтинг потоков: {len(stream_leaderboard.stream_leaderboard_list)} человек")

    for i, member in enumerate(stream_leaderboard.stream_leaderboard_list[:3]):
        print(f"  {i + 1}. {member.full_name} - {member.amount} баллов")


async def demo_month_schedule(sdk: TopJournalSDK):
    """Шаг 11: расписание за месяц и диапазон."""
    month_schedule = await sdk.schedule.get_month_schedule(date.today())
    print(f"Уроков в месяце: {len(month_schedule.lesson_list)}")

    range_schedule = await sdk.schedule.get_range_schedule(date.today(), date.today())
    print(f"Уроков в диапазоне: {len(range_schedule.lesson_list)}")

    month_events = await sdk.schedule.get_month_events(date.today())
    print(f"Событий месяца: {len(month_events.month_event_list)}")


async def demo_homework_list(sdk: TopJournalSDK):
    """Шаг 12: список домашних заданий."""
    homework_list = await sdk.homework.get_homeworks_list()
    print(f"Заданий на странице: {len(homework_list.homework_list)}")
    if homework_list.homework_list:
        first = homework_list.homework_list[0]
        print(f"  Первое: {first.theme} ({first.name_spec})")

    homework_tags = await sdk.homework.get_homework_tags()
    print(f"Тегов оценки ДЗ: {len(homework_tags.homework_tag_list)}")


async def demo_dashboard(sdk: TopJournalSDK):
    """Шаг 13: дашборд."""
    performance = await sdk.dashboard.get_academic_performance()
    print(f"Средний балл за все время: {performance.total_all_time}")

    group_points = await sdk.dashboard.get_leader_group_points()
    print(f"Позиция в группе: {group_points.student_position}")

    counters = await sdk.dashboard.get_page_counters()
    print(f"Счетчиков страниц: {len(counters.page_counter_list)}")


async def demo_library_news(sdk: TopJournalSDK):
    """Шаг 14: библиотека и новости."""
    materials = await sdk.library.get_library_materials(material_type=1)
    print(f"Материалов библиотеки: {len(materials.library_material_list)}")

    news = await sdk.content.get_latest_news()
    print(f"Новостей: {len(news.news_list)}")
    if news.news_list:
        print(f"  Последняя: {news.news_list[0].theme}")


async def demo_profile_payment(sdk: TopJournalSDK):
    """Шаг 15: профиль и оплата."""
    settings = await sdk.profile.get_profile_settings()
    print(f"Email профиля: {settings.email}")
    print(f"Заполненность: {settings.fill_percentage}%")

    achievements = await sdk.profile.get_student_achievements()
    print(f"Достижений: {len(achievements.student_achievement_list)}")

    payment_index = await sdk.payment.get_payment_index()
    print(f"Плательщик: {payment_index.full_name}")


async def demo_portfolio_exams(sdk: TopJournalSDK):
    """Шаг 16: портфолио и экзамены."""
    portfolios = await sdk.portfolio.get_portfolios()
    print(f"Работ в портфолио: {len(portfolios.portfolio_list)}")

    student_exams = await sdk.exams.get_student_exams()
    print(f"Экзаменов: {len(student_exams.student_exam_list)}")

    quarterly = await sdk.exams.get_quarterly_grades()
    print(f"Четвертных оценок: {len(quarterly.grades)}")


async def main():
    """Полный пример использования SDK"""

    print("🚀 TopJournalSDK - Полный пример использования")
    print("=" * 60)

    async with TopJournalSDK() as sdk:
        try:
            print("\n🔐 Шаг 1: Аутентификация")
            print("-" * 30)

            # Замените на реальные учетные данные
            username = "username"
            password = "password"

            print(f"Попытка входа с логином: {username}")
            access_token = await sdk.login(username, password)
            print(f"✅ Вход успешен! Токен: {access_token[:20]}...")

            steps: list[tuple[str, StepFunc]] = [
                ("👤 Шаг 2: Информация о пользователе", demo_user_info),
                ("📊 Шаг 3: Оценки и успеваемость", demo_grades),
                ("📅 Шаг 4: Посещаемость", demo_attendance),
                ("🏠 Шаг 5: Домашние задания", demo_homework),
                (f"🗓️  Шаг 6: Расписание на сегодня ({date.today()})", demo_schedule),
                ("💬 Шаг 7: Отзывы о студенте", demo_feedback),
                ("⭐ Шаг 8: Оценка уроков", demo_evaluation_lessons),
                ("🏷️  Шаг 9: Теги для оценки", demo_evaluation_tags),
                ("🏆 Шаг 10: Рейтинги", demo_leaderboards),
                ("🗓️  Шаг 11: Расписание за месяц и диапазон", demo_month_schedule),
                ("📚 Шаг 12: Список домашних заданий", demo_homework_list),
                ("📈 Шаг 13: Дашборд", demo_dashboard),
                ("📖 Шаг 14: Библиотека и новости", demo_library_news),
                ("👤 Шаг 15: Профиль и оплата", demo_profile_payment),
                ("🏆 Шаг 16: Портфолио и экзамены", demo_portfolio_exams),
            ]
            for title, step in steps:
                await run_step(title, step, sdk)

            print("\n✅ Все данные успешно получены!")

        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            print("Проверьте учетные данные и подключение к интернету")


def print_usage_instructions():
    """Печать инструкций по использованию"""
    print("\n📖 Инструкция по использованию:")
    print("-" * 40)
    print("1. Замените 'your_username' и 'your_password' в коде на реальные учетные данные")
    print("2. Запустите скрипт: python example.py")
    print("3. SDK автоматически авторизуется и получит все доступные данные")
    print("4. Все данные будут выведены в консоль с подробными пояснениями")
    print("\n🔒 Безопасность:")
    print("- Токен авторизации хранится только в памяти")
    print("- Все запросы проходят по HTTPS")
    print("- SDK автоматически управляет жизненным циклом сессии")


if __name__ == "__main__":
    print_usage_instructions()
    print("\n" + "=" * 60)
    asyncio.run(main())
