import streamlit as st
import json
from datetime import datetime

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

st.set_page_config(page_title="To-Do List", page_icon="📌", layout="wide")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

menu = st.sidebar.selectbox("Menu", ["Add Task", "View Tasks", "Progress"])

st.title("📌 To-Do List App")

if menu == "Add Task":
    st.subheader("➕ Add a New Task")
    description = st.text_input("Task Description:")
    due_date = st.date_input("Due Date:", min_value=datetime.today())

    if st.button("Add Task"):
        if description:
            new_task = {"description": description, "due_date": str(due_date), "completed": False}
            st.session_state.tasks.append(new_task)
            save_tasks(st.session_state.tasks)
            st.success("Task added successfully!")
        else:
            st.warning("Please enter a task description.")

elif menu == "View Tasks":
    st.subheader("📋 Your Tasks")

    if st.session_state.tasks:
        for i, task in enumerate(sorted(st.session_state.tasks, key=lambda x: x["due_date"])):
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            
            completed = col1.checkbox(
                f"{task['description']} (Due: {task['due_date']})",
                value=task["completed"],
                key=f"task_{i}"
            )
            
            if col2.button("Edit", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.rerun()
            
            if col3.button("Delete", key=f"delete_{i}"):
                del st.session_state.tasks[i]
                save_tasks(st.session_state.tasks)
                st.rerun()
            
            task["completed"] = completed
        
        save_tasks(st.session_state.tasks)
    else:
        st.write("No tasks added yet.")

    if "edit_index" in st.session_state:
        i = st.session_state.edit_index
        st.subheader("✏️ Edit Task")
        edited_desc = st.text_input("Task Description:", st.session_state.tasks[i]["description"])
        edited_due_date = st.date_input("Due Date:", value=datetime.strptime(st.session_state.tasks[i]["due_date"], "%Y-%m-%d"))
        
        if st.button("Save Changes"):
            st.session_state.tasks[i] = {"description": edited_desc, "due_date": str(edited_due_date), "completed": st.session_state.tasks[i]["completed"]}
            save_tasks(st.session_state.tasks)
            del st.session_state.edit_index
            st.rerun()

elif menu == "Progress":
    st.subheader("📊 Task Progress")
    
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for task in st.session_state.tasks if task["completed"])
    
    progress = (completed_tasks / total_tasks * 100) if total_tasks else 0
    st.progress(int(progress))
    st.write(f"Progress: {int(progress)}%")
