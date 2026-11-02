from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
	task = Task("Feed the dog")
	original_status = task.completed

	task.markComplete()

	assert task.completed != original_status


def test_adding_task_increases_pet_task_count():
	pet = Pet("Buddy", "Dog")
	original_count = len(pet.getTasks())

	pet.addTask(Task("Feed the dog"))

	assert len(pet.getTasks()) == original_count + 1
