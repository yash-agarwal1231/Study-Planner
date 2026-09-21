import streamlit as st
from pymongo import MongoClient

st.markdown(
    """
    <style>
    /* Change overall background color */
    .stApp {
        background-color: #FFF3E0;
        color: #ffffff;
    }
    
    /* Style custom buttons */
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        border: none;
    }
    </style>
    """
) 

# -------------------------------
# Connect to MongoDB
# -------------------------------

client = MongoClient(st.secrets["MONGO_URI"])

db = client["study_planner"]

tasks_collection = db["tasks"]


# -------------------------------
# App title
# -------------------------------

st.title("📚 My Study Planner")
st.subheader("Plan your studies and keep track of your tasks.")


# -------------------------------
# Get user's name
# -------------------------------
st.info(
    "ℹ️ There is no password authentication yet. "
    "Your username is your identity and is **Case-Sensitive.**"
)
name = st.text_input("👤 Enter your name")

if name:

    st.success(f"Welcome, {name}! 👋")


    # -------------------------------
    # Add a new task
    # -------------------------------

    st.subheader("➕ Add a Task")

    subject = st.text_input("📚 Subject")
    task = st.text_input("📝 What do you need to study?")
    deadline = st.date_input("📅 Deadline")

    if st.button("Add Task"):

        if subject and task:

            new_task = {
                "user": name,
                "subject": subject,
                "task": task,
                "deadline": str(deadline),
                "completed": False
            }

            tasks_collection.insert_one(new_task)

            st.success("✅ Task added successfully!")

        else:
            st.warning("⚠️ Please enter both the subject and task.")


    # -------------------------------
    # Display user's tasks
    # -------------------------------

    st.subheader("📋 Your Tasks")

    # Find only tasks belonging to the current user
    tasks = list(tasks_collection.find({"user": name}))

    if tasks:

        for item in tasks:

            if item["completed"]:

                st.write(
                    f"~~📚 {item['subject']} — "
                    f"{item['task']} — "
                    f"Due: {item['deadline']}~~"
                )

            else:

                st.write(
                    f"📚 **{item['subject']}** — "
                    f"{item['task']} — "
                    f"Due: {item['deadline']}"
                )

            col1, col2 = st.columns(2)

            with col1:

                if not item["completed"]:

                    if st.button(
                        "✅ Complete",
                        key=f"complete_{item['_id']}"
                    ):

                        tasks_collection.update_one(
                            {"_id": item["_id"]},
                            {"$set": {"completed": True}}
                        )

                        st.rerun()

            with col2:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{item['_id']}"
                ):

                    tasks_collection.delete_one(
                        {"_id": item["_id"]}
                    )

                    st.rerun()

    else:

        st.info("No tasks added yet.")
