# IT-Top Journal SDK (journaltop)

A Python SDK for interacting with the IT-Top educational platform journal API. This library provides async methods for authentication, schedule retrieval, and homework statistics.

## Description

`journaltop` is an asynchronous Python library that simplifies interaction with the IT-Top journal system. It handles authentication, API communication, and data parsing into strongly-typed Pydantic models.

### Features

- 🔐 JWT-based authentication
- ✅ Full type hints and Pydantic validation
- 🚀 Async/await support with httpx
- 📝 Comprehensive logging

## Installation `not work!`

```bash
# Add library to dependencies
uv add journaltop

# Without uv
pip install journaltop
```

### Requirements

- Python 3.13+
- asyncio
- httpx


## Quick Start

```python
import asyncio
import httpx
from journaltop import Client

async def main():
    async with httpx.AsyncClient() as client:
        # Initialize client
        app = Client(client)
        
        # Login and get JWT token (DONT SHARE THIS TOKEN!)
        token = await app.login(
            username="your_username",
            password="your_password"
        )
        
        # Get today's schedule
        schedule = await app.get_schedule(token=token, date=None, timeout=2.0)
        
        # Access schedule data
        first_lesson = schedule.lesson(1)
        if first_lesson:
            print(f"First lesson: {first_lesson.subject_name}")
            print(f"Teacher: {first_lesson.teacher_name}")
            print(f"Time: {first_lesson.started_at} - {first_lesson.finished_at}")
            print(f"Room: {first_lesson.room_name}")
        
        # Get homework data
        hw_stats = await app.get_homework(token=token)
        print(f"Total homework: {hw_stats.total}")
        print(f"Overdue: {hw_stats.overdue}")
        print(f"Checked: {hw_stats.checked}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Usage

### Authentication

```python
from journaltop import Client

async with httpx.AsyncClient() as client:
    app = Client(client)
    token = await app.login(username="username", password="password")
```

### Schedule Management

```python
# Get schedule for today
schedule = await app.get_schedule(token=token, date=None, timeout=2.0)

# Get schedule for specific date
schedule = await app.get_schedule(token=token, date="2025-11-01", timeout=2.0)

# Access lesson by number
lesson = schedule.lesson(2)
print(f"{lesson.subject_name} at {lesson.started_at}")

# Iterate through all lessons
for lesson_data in schedule.lessons:
    print(f"Lesson {lesson_data.lesson}: {lesson_data.subject_name}")
```

### Homework Statistics

```python
# Get homework statistics
stats = await app.get_homework(token=token)

# Access stats properties
print(f"Total: {stats.total}")           # Total homework count
print(f"Current: {stats.current}")       # Current homework
print(f"Overdue: {stats.overdue}")       # Overdue homework
print(f"Checked: {stats.checked}")       # Checked homework
print(f"Pending: {stats.pending}")       # Pending review
print(f"Deleted: {stats.deleted}")       # Deleted by teacher

# Or use the method
overdue_count = stats.get_counter(0)  # By counter type number
```



### Logging

The SDK includes comprehensive logging. Configure it in your application:

```python
from journaltop.logging.logger import setup_logging
import logging

# Setup logging
setup_logging(level=logging.DEBUG)

```

### Error Handling

```python
from journaltop.errors import journal_exceptions

try:
    token = await app.login(username="user", password="pass")
except journal_exceptions.JournalAuthError as e:
    print(f"Authentication failed: {e}")
except journal_exceptions.InvalidJWTError:
    print("Invalid or expired token")
except journal_exceptions.JournalRequestTimeoutError:
    print("Request timed out")
except journal_exceptions.JournalInternalServerError as e:
    print(f"Server error: {e}")
```

## Support

For issues, questions, or contributions, please open an issue in the repository issue tracker.

## Authors and Acknowledgment

Developed for the IT-Top educational platform community.

## License

[GNU Public License](lICENSE)

## Project Status

Active development. Core features are implemented and stable. Additional features and improvements are ongoing.
