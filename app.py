from datetime import time

import streamlit as st

from pawpal_system import Frequency, Owner, Pet, Priority, Schedule, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Streamlit reruns this script on every interaction, so the Owner lives in session_state.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
owner: Owner = st.session_state.owner

st.subheader("Owner")
new_name = st.text_input("Owner name", value=owner.name)
if new_name.strip() and new_name != owner.name:
    owner.updateName(new_name.strip())

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.error("Pet name is required.")
        elif any(p.name.lower() == pet_name.strip().lower() for p in owner.getPets()):
            st.warning(f"You already have a pet named {pet_name.strip()}.")
        else:
            owner.addPet(Pet(pet_name.strip(), species))
            st.success(f"Added {pet_name.strip()}!")

pets = owner.getPets()
if pets:
    st.write("Your pets:", ", ".join(f"{p.name} ({p.species})" for p in pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
if pets:
    with st.form("add_task_form", clear_on_submit=True):
        target = st.selectbox("Pet", [p.name for p in pets])
        task_title = st.text_input("Task title", value="Morning walk")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", [p.name.lower() for p in Priority], index=2)
        with col3:
            frequency = st.selectbox("Frequency", [f.name.lower() for f in Frequency], index=1)
        with col4:
            preferred = st.time_input("Preferred time", value=time(8, 0))
        if st.form_submit_button("Add task"):
            if not task_title.strip():
                st.error("Task title is required.")
            else:
                pet = next(p for p in pets if p.name == target)
                pet.addTask(
                    Task(
                        title=task_title.strip(),
                        priority=Priority[priority.upper()],
                        durationMinutes=int(duration),
                        time=preferred,
                        frequency=Frequency[frequency.upper()],
                    )
                )
                st.success(f"Added '{task_title.strip()}' for {target}.")
else:
    st.info("Add a pet before adding tasks.")

all_tasks = owner.getAllTasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "task": t.title,
                "time": t.time.strftime("%H:%M") if t.time else "flexible",
                "duration (min)": t.durationMinutes,
                "priority": t.priority.name.lower(),
                "frequency": t.frequency.name.lower(),
                "done": t.completed,
            }
            for pet, t in all_tasks
        ]
    )
else:
    st.info("No tasks yet.")

st.divider()

st.subheader("Build Schedule")
available = st.number_input("Minutes available today", min_value=1, max_value=1440, value=120)
if st.button("Generate schedule"):
    schedule = Schedule(owner)
    schedule.createSchedule(availableMinutes=int(available))
    if not schedule.entries and not schedule.skipped:
        st.warning("Nothing to schedule. Add some tasks first.")
    else:
        st.table(
            [
                {
                    "start": e.startTime.strftime("%H:%M"),
                    "end": e.endTime.strftime("%H:%M"),
                    "pet": e.pet.name,
                    "task": e.task.title,
                    "why": e.reason,
                }
                for e in schedule.getTasksForDay()
            ]
        )
        for pet, task, why in schedule.skipped:
            st.warning(f"Skipped '{task.title}' ({pet.name}): {why}")
