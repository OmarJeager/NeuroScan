import tkinter as tk
from tkinter import messagebox

# ADHD Test Questions
questions = [
    "1. How often do you have trouble wrapping up the final details of a project?",
    "2. How often do you have difficulty getting things in order when you have to do a task that requires organization?",
    "3. How often do you have problems remembering appointments or obligations?",
    "4. When you have a task that requires a lot of thought, how often do you avoid or delay getting started?",
    "5. How often do you fidget or squirm with your hands or feet when you have to sit down for a long time?",
    "6. How often do you feel overly active and compelled to do things, like you were driven by a motor?"
]

# Possible answers
answers = [
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"]
]

# Scoring weights for each answer
scoring = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Often": 3,
    "Very Often": 4
}

# Global variables
current_question = 0
user_responses = []

# Function to handle the next question
def next_question():
    global current_question, user_responses

    # Get the selected answer
    selected_answer = answer_var.get()
    if not selected_answer:
        messagebox.showwarning("Warning", "Please select an answer!")
        return  # Stop if no answer is selected

    # Save the response
    user_responses.append(selected_answer)

    # Move to the next question
    current_question += 1

    if current_question < len(questions):
        question_label.config(text=questions[current_question])
        for i, option in enumerate(answers[current_question]):
            radio_buttons[i].config(text=option, value=option)
        answer_var.set(None)  # Clear selection
    else:
        show_result()

# Function to calculate and display the result
def show_result():
    global user_responses

    # Calculate the total score
    total_score = sum(scoring[response] for response in user_responses if response in scoring)

    # Determine the result
    if total_score <= 10:
        result = "Low likelihood of ADHD."
    elif total_score <= 20:
        result = "Moderate likelihood of ADHD."
    else:
        result = "High likelihood of ADHD."

    # Show the result
    messagebox.showinfo("ADHD Test Result", f"Your total score is {total_score}. {result}")

    # Reset the test
    reset_test()

# Function to reset the test
def reset_test():
    global current_question, user_responses
    current_question = 0
    user_responses = []
    question_label.config(text=questions[current_question])
    for i, option in enumerate(answers[current_question]):
        radio_buttons[i].config(text=option, value=option)
    answer_var.set(None)

# Create the main window
root = tk.Tk()
root.title("ADHD Test App")
root.geometry("500x300")

# Question label
question_label = tk.Label(root, text=questions[current_question], wraplength=400, justify="left")
question_label.pack(pady=20)

# Radio buttons for answers
answer_var = tk.StringVar()
radio_buttons = []
for i in range(len(answers[current_question])):
    rb = tk.Radiobutton(root, text=answers[current_question][i], variable=answer_var, value=answers[current_question][i])
    rb.pack(anchor="w")
    radio_buttons.append(rb)

# Next button
next_button = tk.Button(root, text="Next", command=next_question)
next_button.pack(pady=20)

# Start the main loop
root.mainloop()