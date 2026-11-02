from datetime import date, time
from enum import Enum


class Priority(Enum):
	LOW = "LOW"
	MEDIUM = "MEDIUM"
	HIGH = "HIGH"


class Owner:
	def __init__(self, name: str, preferences: list[str] | None = None):
		self.name = name
		self.preferences = preferences if preferences is not None else []
		self._pets: list[Pet] = []

	def addPet(self, pet: "Pet") -> None:
		pass

	def updateName(self, name: str) -> None:
		pass

	def getPets(self) -> list["Pet"]:
		pass


class Pet:
	def __init__(self, name: str, species: str):
		self.name = name
		self.species = species
		self._tasks: list[Task] = []

	def addTask(self, task: "Task") -> None:
		pass

	def updateName(self, name: str) -> None:
		pass

	def updateTask(self, task: "Task") -> None:
		pass

	def getTasks(self) -> list["Task"]:
		pass


class Task:
	def __init__(
		self,
		title: str,
		description: str,
		priority: Priority,
		durationMinutes: int,
	):
		self.title = title
		self.description = description
		self.priority = priority
		self.durationMinutes = durationMinutes

	def updateDetails(
		self,
		title: str,
		description: str,
		priority: Priority,
		durationMinutes: int,
	) -> None:
		pass


class Schedule:
	def __init__(self, date: date):
		self.date = date
		self.entries: list[ScheduledTask] = []

	def createSchedule(self, owner: Owner, availableMinutes: int) -> None:
		pass

	def getTasksForDay(self) -> list["ScheduledTask"]:
		pass


class ScheduledTask:
	def __init__(self, task: Task, startTime: time, endTime: time, reason: str):
		self.task = task
		self.startTime = startTime
		self.endTime = endTime
		self.reason = reason
