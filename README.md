# IT-Top Journal SDK (journaltop)

A Python SDK for interacting with the IT-Top educational platform journal API. This library provides async methods for authentication, schedule retrieval, and homework statistics.

## Description

`journaltop` is an asynchronous Python client library that simplifies interaction with the IT-Top journal system. It handles authentication, API communication, and data parsing into strongly-typed Pydantic models.

### Features

- 🔐 JWT-based authentication
- 📅 Schedule data retrieval and parsing
- 📊 Homework statistics tracking
- ✅ Full type hints and Pydantic validation
- 🚀 Async/await support with httpx
- 📝 Comprehensive logging

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd journaltop

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Requirements

- Python 3.10+
- httpx
- pydantic

## Quick Start

```python
import asyncio
import httpx
from journaltop import Client

async def main():
    async with httpx.AsyncClient() as client:
        # Initialize client
        app = Client(client)
        
        # Login and get JWT token
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
        
        # Get homework statistics
        hw_stats = await app.get_homework_stats(token=token)
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
stats = await app.get_homework_stats(token=token)

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

### Data Models

#### Schedule Model

```python
class Lesson:
    date: date
    lesson: int                # Lesson number (1-8)
    started_at: time
    finished_at: time
    teacher_name: str
    subject_name: str
    room_name: str

class Schedule:
    lessons: List[Lesson]
    
    def lesson(number: int) -> Optional[Lesson]
```

#### Homework Stats Model

```python
class HomeworkStats:
    counters: List[HomeworkCounter]
    
    # Properties
    overdue: int      # Counter type 0
    checked: int      # Counter type 1
    pending: int      # Counter type 2
    current: int      # Counter type 3
    total: int        # Counter type 4
    deleted: int      # Counter type 5
```

### Logging

The SDK includes comprehensive logging. Configure it in your application:

```python
from journaltop.utils.logger import setup_logging
import logging

# Setup logging (logs will be in ./journaltop/logging/logs/)
setup_logging(level=logging.DEBUG)

# Logs are automatically created:
# - app.log: Standard logs
# - app-verbose.log: Detailed logs with full context
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
