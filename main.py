from datetime import time

from pawpal_system import Frequency, Owner, Pet, Priority, Schedule, Task


def main():
    owner = Owner(name="Alex")

    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Whiskers", species="Cat")
    owner.addPet(dog)
    owner.addPet(cat)

    dog.addTask(Task(title="Morning walk", time=time(7, 30), priority=Priority.HIGH,
                     durationMinutes=30, frequency=Frequency.DAILY))
    dog.addTask(Task(title="Evening feeding", time=time(18, 0), priority=Priority.HIGH,
                     durationMinutes=10, frequency=Frequency.DAILY))
    cat.addTask(Task(title="Medication", time=time(12, 15), priority=Priority.MEDIUM,
                     durationMinutes=5, frequency=Frequency.DAILY))

    schedule = Schedule(owner)
    schedule.createSchedule(availableMinutes=120)

    print("Today's Schedule")
    print("=" * 30)
    for entry in schedule.getTasksForDay():
        print(f"{entry.startTime:%H:%M}  {entry.pet.name:<10} {entry.task.title}")


if __name__ == "__main__":
    main()
