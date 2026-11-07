# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

``` bash
Today's Schedule
==============================
08:00  Buddy      Morning walk
12:15  Whiskers   Medication
18:00  Buddy      Evening feeding
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

============================ test session starts =============================
platform darwin -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0
rootdir: /Users/alexandraramlogan/Documents/Fall 2026/CEN5025/CodePath/ai110-module2show-pawpal-starter
plugins: anyio-4.16.0
collected 3 items                                                            

tests/test_app.py .                                                    [ 33%]
tests/test_pawpal.py ..                                                [100%]

============================= 3 passed in 0.57s ==============================

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Schedule.createSchedule()` | Selects tasks by priority (high first), preferred time, then duration. Selected tasks are placed in preferred-time order; flexible tasks come last. |
| Filtering | `Schedule.createSchedule()`, `Task.isDueOn()` | Excludes completed tasks and tasks not due on the schedule date. Tasks exceeding the remaining time budget or ending at or after midnight are recorded as skipped. |
| Conflict handling | `Schedule.createSchedule()` | Places tasks sequentially, starting no earlier than the preferred time or the end of the previous task. Conflicts can delay tasks beyond their preferred time. |
| Recurring tasks | `Task.isDueOn()` | Daily tasks are due every day. Weekly tasks with a due date are due on the same weekday; one-time tasks with a due date are due on that date. Without a due date, either is treated as due every day. Completion does not reset automatically. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Update your name in the "Name" field. 
2. Add your pet name and species under "Add a Pet" 
3. Under "Add a Task" select your pet, and add details to the task including preferred time, estimated duration, and priority level of the task 
4. Under "Build your schedule", enter how many minutes you have available for the day
5. Select "Generate schedule" to create a schedule for the day 

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

![PawPal+ app screenshot](figures/demo_screenshot.png)