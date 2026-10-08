"""
Полный пример использования TopJournalSDK.

Complete example of using TopJournalSDK.
"""

import asyncio
from datetime import date

from top_journal_sdk import TopJournalSDK


async def main():
    """Полный пример использования SDK"""

    print("🚀 TopJournalSDK - Полный пример использования")
    print("=" * 60)

    async with TopJournalSDK() as sdk:
        try:
            # 1. Аутентификация
            print("\n🔐 Шаг 1: Аутентификация")
            print("-" * 30)

            # Замените на реальные учетные данные
            username = "username"
            password = "password"

            print(f"Попытка входа с логином: {username}")
            access_token = await sdk.login(username, password)
            print(f"✅ Вход успешен! Токен: {access_token[:20]}...")

            # 2. Получение информации о пользователе
            print("\n👤 Шаг 2: Информация о пользователе")
            print("-" * 30)

            user_info = await sdk.user.get_personal_info()
            print(f"Полное имя: {user_info.full_name}")
            print(f"Группа: {user_info.group_name}")
            print(f"Поток: {user_info.stream_name}")
            print(f"Топ коины: {user_info.top_coins}")
            print(f"Топ гемы: {user_info.top_gems}")
            print(f"Возраст: {user_info.age}")
            print(f"Дата рождения: {user_info.birthday}")
            print(f"Дата регистрации: {user_info.registration_date}")

            # 3. Получение оценок
            print("\n📊 Шаг 3: Оценки и успеваемость")
            print("-" * 30)

            # Средние оценки
            try:
                average_grades = await sdk.grades.get_average_grades()
                print(f"Количество средних оценок: {len(average_grades.grade_list)}")
                for i, grade in enumerate(
                    average_grades.grade_list[:5]
                ):  # Показать первые 5
                    print(f"  Оценка {i + 1}: {grade.points} (дата: {grade.date})")
            except Exception as e:
                print(f"❌ Ошибка получения средних оценок: {e}")

            # Оценки за посещаемость
            try:
                attendance_grades = await sdk.grades.get_class_attendance_grades()
                print(
                    f"Количество оценок за посещаемость: {len(attendance_grades.class_attendance_grade_list)}"
                )
                for i, grade in enumerate(
                    attendance_grades.class_attendance_grade_list[:3]
                ):
                    print(
                        f"  Посещаемость {i + 1}: {grade.status_was} ({grade.date_visit})"
                    )
            except Exception as e:
                print(f"❌ Ошибка получения оценок за посещаемость: {e}")

            # 4. Получение посещаемости
            print("\n📅 Шаг 4: Посещаемость")
            print("-" * 30)

            try:
                attendance_data = await sdk.attendance.get_attendances()
                print(
                    f"Количество записей о посещаемости: {len(attendance_data.attendance_list)}"
                )
                for i, att in enumerate(attendance_data.attendance_list[:5]):
                    print(f"  Посещаемость {i + 1}: {att.points} (дата: {att.date})")
            except Exception as e:
                print(f"❌ Ошибка получения данных о посещаемости: {e}")

            # 5. Получение домашних заданий
            print("\n🏠 Шаг 5: Домашние задания")
            print("-" * 30)

            try:
                homeworks = await sdk.homework.get_homeworks()
                print(f"Всего домашних заданий: {homeworks.total}")
                print(f"Просрочено: {homeworks.overdue}")
                print(f"Проверено: {homeworks.checked}")
                print(f"На проверке: {homeworks.pending}")
                print(f"Текущие: {homeworks.current}")
                print(f"Удалено: {homeworks.deleted}")
            except Exception as e:
                print(f"❌ Ошибка получения данных о домашних заданиях: {e}")

            # 6. Получение расписания
            print(f"\n🗓️  Шаг 6: Расписание на сегодня ({date.today()})")
            print("-" * 30)

            try:
                schedule = await sdk.schedule.get_schedule_by_date(date.today())
                print(f"Количество уроков на сегодня: {len(schedule.lesson_list)}")

                for lesson in schedule.lesson_list:
                    print(f"  Урок {lesson.lesson}: {lesson.subject_name}")
                    print(f"    Время: {lesson.started_at} - {lesson.finished_at}")
                    print(f"    Учитель: {lesson.teacher_name}")
                    print(f"    Аудитория: {lesson.room_name}")
                    print()
            except Exception as e:
                print(f"❌ Ошибка получения расписания: {e}")

            # 7. Получение отзывов
            print("\n💬 Шаг 7: Отзывы о студенте")
            print("-" * 30)

            try:
                reviews = await sdk.feedback.get_student_reviews()
                print(f"Количество отзывов: {len(reviews.review_list)}")

                for i, review in enumerate(
                    reviews.review_list[:3]
                ):  # Показать первые 3
                    print(f"  Отзыв {i + 1}:")
                    print(f"    Дата: {review.date}")
                    print(f"    Учитель: {review.teacher}")
                    print(f"    Предмет: {review.spec}")
                    print(f"    Сообщение: {review.message}")
                    print()
            except Exception as e:
                print(f"❌ Ошибка получения отзывов: {e}")

            # 8. Получение уроков для оценки
            print("\n⭐ Шаг 8: Оценка уроков")
            print("-" * 30)

            try:
                evaluation_lessons = (
                    await sdk.lesson_evaluation.get_evaluation_lessons()
                )
                print(f"Уроков для оценки: {len(evaluation_lessons.evaluation_list)}")

                for i, lesson in enumerate(
                    evaluation_lessons.evaluation_list[:3]
                ):  # Показать первые 3
                    print(f"  Урок {i + 1}:")
                    print(f"    Дата: {lesson.date_visit}")
                    print(f"    Учитель: {lesson.fio_teach}")
                    print(f"    Предмет: {lesson.spec_name}")
                    print()

            except Exception as e:
                print(f"❌ Ошибка получения уроков для оценки: {e}")

            # 9. Получение тегов для оценки
            print("\n🏷️  Шаг 9: Теги для оценки")
            print("-" * 30)

            try:
                # Получение тегов для оценки урока
                lesson_tags = await sdk.lesson_evaluation.get_evaluation_lesson_tags(
                    "evaluation_lesson"
                )
                print(f"Тегов для оценки урока: {len(lesson_tags.evaluation_tags)}")

                # Получение тегов для оценки преподавания
                teach_tags = await sdk.lesson_evaluation.get_evaluation_lesson_tags(
                    "evaluation_lesson_teach"
                )
                print(
                    f"Тегов для оценки преподавания: {len(teach_tags.evaluation_tags)}"
                )

            except Exception as e:
                print(f"❌ Ошибка получения тегов: {e}")

            # 10. Получение рейтингов
            print("\n🏆 Шаг 10: Рейтинги")
            print("-" * 30)

            try:
                # Рейтинг групп
                group_leaderboard = await sdk.leaderboard.get_group_leaderboards()
                print(
                    f"Рейтинг групп: {len(group_leaderboard.group_leaderboard_list)} человек"
                )

                # Показать топ-3
                for i, member in enumerate(
                    group_leaderboard.group_leaderboard_list[:3]
                ):
                    print(f"  {i + 1}. {member.full_name} - {member.amount} баллов")

                print()

                # Рейтинг потоков
                stream_leaderboard = await sdk.leaderboard.get_stream_leaderboards()
                print(
                    f"Рейтинг потоков: {len(stream_leaderboard.stream_leaderboard_list)} человек"
                )

                # Показать топ-3
                for i, member in enumerate(
                    stream_leaderboard.stream_leaderboard_list[:3]
                ):
                    print(f"  {i + 1}. {member.full_name} - {member.amount} баллов")

            except Exception as e:
                print(f"❌ Ошибка получения рейтингов: {e}")

            # 11. Расписание за месяц и диапазон
            print("\n🗓️  Шаг 11: Расписание за месяц и диапазон")
            print("-" * 30)

            try:
                month_schedule = await sdk.schedule.get_month_schedule(date.today())
                print(f"Уроков в месяце: {len(month_schedule.lesson_list)}")

                range_schedule = await sdk.schedule.get_range_schedule(
                    date.today(), date.today()
                )
                print(f"Уроков в диапазоне: {len(range_schedule.lesson_list)}")

                month_events = await sdk.schedule.get_month_events(date.today())
                print(f"Событий месяца: {len(month_events.month_event_list)}")
            except Exception as e:
                print(f"❌ Ошибка получения расписания: {e}")

            # 12. Список домашних заданий и теги
            print("\n📚 Шаг 12: Список домашних заданий")
            print("-" * 30)

            try:
                homework_list = await sdk.homework.get_homeworks_list()
                print(f"Заданий на странице: {len(homework_list.homework_list)}")
                if homework_list.homework_list:
                    first = homework_list.homework_list[0]
                    print(f"  Первое: {first.theme} ({first.name_spec})")

                homework_tags = await sdk.homework.get_homework_tags()
                print(f"Тегов оценки ДЗ: {len(homework_tags.homework_tag_list)}")
            except Exception as e:
                print(f"❌ Ошибка получения домашних заданий: {e}")

            # 13. Дашборд: успеваемость и баллы
            print("\n📈 Шаг 13: Дашборд")
            print("-" * 30)

            try:
                performance = await sdk.dashboard.get_academic_performance()
                print(f"Средний балл за все время: {performance.total_all_time}")

                group_points = await sdk.dashboard.get_leader_group_points()
                print(f"Позиция в группе: {group_points.student_position}")

                counters = await sdk.dashboard.get_page_counters()
                print(f"Счетчиков страниц: {len(counters.page_counter_list)}")
            except Exception as e:
                print(f"❌ Ошибка получения дашборда: {e}")

            # 14. Библиотека и новости
            print("\n📖 Шаг 14: Библиотека и новости")
            print("-" * 30)

            try:
                materials = await sdk.library.get_library_materials(material_type=1)
                print(f"Материалов библиотеки: {len(materials.library_material_list)}")

                news = await sdk.content.get_latest_news()
                print(f"Новостей: {len(news.news_list)}")
                if news.news_list:
                    print(f"  Последняя: {news.news_list[0].theme}")
            except Exception as e:
                print(f"❌ Ошибка получения библиотеки/новостей: {e}")

            # 15. Профиль и оплата
            print("\n👤 Шаг 15: Профиль и оплата")
            print("-" * 30)

            try:
                settings = await sdk.profile.get_profile_settings()
                print(f"Email профиля: {settings.email}")
                print(f"Заполненность: {settings.fill_percentage}%")

                achievements = await sdk.profile.get_student_achievements()
                print(f"Достижений: {len(achievements.student_achievement_list)}")

                payment_index = await sdk.payment.get_payment_index()
                print(f"Плательщик: {payment_index.full_name}")
            except Exception as e:
                print(f"❌ Ошибка получения профиля/оплаты: {e}")

            # 16. Портфолио и экзамены
            print("\n🏆 Шаг 16: Портфолио и экзамены")
            print("-" * 30)

            try:
                portfolios = await sdk.portfolio.get_portfolios()
                print(f"Работ в портфолио: {len(portfolios.portfolio_list)}")

                student_exams = await sdk.exams.get_student_exams()
                print(f"Экзаменов: {len(student_exams.student_exam_list)}")

                quarterly = await sdk.exams.get_quarterly_grades()
                print(f"Четвертных оценок: {len(quarterly.grades)}")
            except Exception as e:
                print(f"❌ Ошибка получения портфолио/экзаменов: {e}")

            print("\n✅ Все данные успешно получены!")

        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            print("Проверьте учетные данные и подключение к интернету")


def print_usage_instructions():
    """Печать инструкций по использованию"""
    print("\n📖 Инструкция по использованию:")
    print("-" * 40)
    print(
        "1. Замените 'your_username' и 'your_password' в коде на реальные учетные данные"
    )
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
