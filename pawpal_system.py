from __future__ import annotations

from datetime import date, datetime, time, timedelta
from enum import Enum


class Priority(Enum):
	LOW = 1
	MEDIUM = 2
	HIGH = 3


class Frequency(Enum):
	ONCE = "ONCE"
	DAILY = "DAILY"
	WEEKLY = "WEEKLY"


class Task:
	"""A single care activity."""

	def __init__(
		self,
		title: str,
		description: str = "",
		priority: Priority = Priority.MEDIUM,
		durationMinutes: int = 15,
		time: time | None = None,
		frequency: Frequency = Frequency.ONCE,
		dueDate: date | None = None,
	):
		if durationMinutes <= 0:
			raise ValueError("durationMinutes must be positive")
		self.title = title
		self.description = description
		self.priority = priority
		self.durationMinutes = durationMinutes
		self.time = time  # preferred start time, None means flexible
		self.frequency = frequency
		self.dueDate = dueDate  # anchor date for ONCE/WEEKLY tasks
		self.completed = False

	def updateDetails(
		self,
		title: str | None = None,
		description: str | None = None,
		priority: Priority | None = None,
		durationMinutes: int | None = None,
		time: time | None = None,
		frequency: Frequency | None = None,
	) -> None:
		if durationMinutes is not None and durationMinutes <= 0:
			raise ValueError("durationMinutes must be positive")
		if title is not None:
			self.title = title
		if description is not None:
			self.description = description
		if priority is not None:
			self.priority = priority
		if durationMinutes is not None:
			self.durationMinutes = durationMinutes
		if time is not None:
			self.time = time
		if frequency is not None:
			self.frequency = frequency

	def markComplete(self) -> None:
		self.completed = True

	def markIncomplete(self) -> None:
		self.completed = False

	def isDueOn(self, day: date) -> bool:
		if self.frequency is Frequency.DAILY:
			return True
		if self.dueDate is None:
			return True
		if self.frequency is Frequency.WEEKLY:
			return self.dueDate.weekday() == day.weekday()
		return self.dueDate == day

	def __repr__(self) -> str:
		return f"Task({self.title!r}, {self.priority.name}, {self.durationMinutes}m)"


class Pet:
	"""Stores pet details and its tasks."""

	def __init__(self, name: str, species: str):
		self.name = name
		self.species = species
		self._tasks: list[Task] = []

	def addTask(self, task: Task) -> None:
		if task not in self._tasks:
			self._tasks.append(task)

	def removeTask(self, task: Task) -> None:
		self._tasks.remove(task)

	def updateName(self, name: str) -> None:
		self.name = name

	def updateTask(self, task: Task, **changes) -> None:
		if task not in self._tasks:
			raise ValueError("Task does not belong to this pet")
		task.updateDetails(**changes)

	def getTasks(self, includeCompleted: bool = True) -> list[Task]:
		if includeCompleted:
			return list(self._tasks)
		return [t for t in self._tasks if not t.completed]

	def __repr__(self) -> str:
		return f"Pet({self.name!r}, {self.species!r})"


class Owner:
	"""Manages multiple pets and exposes all of their tasks."""

	def __init__(self, name: str, preferences: list[str] | None = None):
		self.name = name
		self.preferences = preferences if preferences is not None else []
		self._pets: list[Pet] = []

	def addPet(self, pet: Pet) -> None:
		if pet not in self._pets:
			self._pets.append(pet)

	def removePet(self, pet: Pet) -> None:
		self._pets.remove(pet)

	def updateName(self, name: str) -> None:
		self.name = name

	def getPets(self) -> list[Pet]:
		return list(self._pets)

	def getAllTasks(self, includeCompleted: bool = True) -> list[tuple[Pet, Task]]:
		return [
			(pet, task)
			for pet in self._pets
			for task in pet.getTasks(includeCompleted)
		]


class ScheduledTask:
	"""A task placed at a concrete time slot, with the reason it was chosen."""

	def __init__(self, pet: Pet, task: Task, startTime: time, endTime: time, reason: str):
		self.pet = pet
		self.task = task
		self.startTime = startTime
		self.endTime = endTime
		self.reason = reason

	def __repr__(self) -> str:
		return (
			f"{self.startTime:%H:%M}-{self.endTime:%H:%M} "
			f"{self.task.title} ({self.pet.name})"
		)


class Schedule:
	"""The brain: retrieves, organizes, and manages tasks across all pets."""

	def __init__(self, owner: Owner, day: date | None = None):
		self.owner = owner
		self.date = day if day is not None else date.today()
		self.entries: list[ScheduledTask] = []
		self.skipped: list[tuple[Pet, Task, str]] = []

	def createSchedule(
		self,
		availableMinutes: int,
		startTime: time = time(8, 0),
	) -> list[ScheduledTask]:
		"""Pick due, incomplete tasks by priority and fit them into the time budget."""
		self.entries = []
		self.skipped = []

		candidates = [
			(pet, task)
			for pet, task in self.owner.getAllTasks(includeCompleted=False)
			if task.isDueOn(self.date)
		]
		candidates.sort(
			key=lambda pt: (
				-pt[1].priority.value,
				pt[1].time or time.max,
				pt[1].durationMinutes,
			)
		)

		# Choose what fits by priority, then lay the chosen tasks out chronologically.
		chosen = []
		remaining = availableMinutes
		for pet, task in candidates:
			if task.durationMinutes > remaining:
				self.skipped.append((pet, task, "Not enough time left in the day"))
				continue
			remaining -= task.durationMinutes
			chosen.append((pet, task))
		chosen.sort(key=lambda pt: (pt[1].time or time.max, -pt[1].priority.value))

		cursor = datetime.combine(self.date, startTime)
		for pet, task in chosen:
			if task.time is not None:
				cursor = max(cursor, datetime.combine(self.date, task.time))
			end = cursor + timedelta(minutes=task.durationMinutes)
			if end.date() != self.date:
				self.skipped.append((pet, task, "Would run past midnight"))
				continue
			self.entries.append(
				ScheduledTask(pet, task, cursor.time(), end.time(), self._explain(task))
			)
			remaining -= task.durationMinutes
			cursor = end

		self.entries.sort(key=lambda e: e.startTime)
		return self.entries

	def getTasksForDay(self) -> list[ScheduledTask]:
		return sorted(self.entries, key=lambda e: e.startTime)

	def getTasksForPet(self, pet: Pet) -> list[ScheduledTask]:
		return [e for e in self.getTasksForDay() if e.pet is pet]

	def markTaskComplete(self, entry: ScheduledTask) -> None:
		entry.task.markComplete()

	def totalMinutes(self) -> int:
		return sum(e.task.durationMinutes for e in self.entries)

	def explain(self) -> str:
		lines = [f"Plan for {self.owner.name} on {self.date:%Y-%m-%d}:"]
		for e in self.getTasksForDay():
			lines.append(f"  {e.startTime:%H:%M} - {e.task.title} ({e.pet.name}): {e.reason}")
		for pet, task, why in self.skipped:
			lines.append(f"  skipped - {task.title} ({pet.name}): {why}")
		return "\n".join(lines)

	@staticmethod
	def _explain(task: Task) -> str:
		reason = f"{task.priority.name.lower()} priority, {task.durationMinutes} min"
		if task.time is not None:
			reason += f", preferred at {task.time:%H:%M}"
		return reason + f", {task.frequency.name.lower()}"
