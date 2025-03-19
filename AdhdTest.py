import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import time
import threading

class ADHDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADHD Management App")
        self.root.geometry("800x600")

        # Header Section
        self.header_frame = tk.Frame(root)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        self.start_test_button = tk.Button(self.header_frame, text="Start ADHD Test", command=self.start_adhd_test)
        self.start_test_button.grid(row=0, column=0, padx=5)

        self.export_button = tk.Button(self.header_frame, text="Export Data", command=self.export_data)
        self.export_button.grid(row=0, column=1, padx=5)

        # Main container for organizing sections
        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Task List Section
        self.task_frame = tk.LabelFrame(self.main_frame, text="Task List", padx=10, pady=10)
        self.task_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.task_list = []
        self.task_display = tk.Listbox(self.task_frame, selectmode=tk.MULTIPLE, height=5)
        self.task_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.add_task_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=1, column=0, pady=5)

        # Habit Tracker Section
        self.habit_frame = tk.LabelFrame(self.main_frame, text="Daily Habits", padx=10, pady=10)
        self.habit_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.habit_entry = tk.Entry(self.habit_frame)
        self.habit_entry.grid(row=0, column=0, pady=5, sticky="ew", padx=5)
        self.add_habit_button = tk.Button(self.habit_frame, text="Add Habit", command=self.add_habit)
        self.add_habit_button.grid(row=1, column=0, pady=5)
        self.habit_list = tk.Listbox(self.habit_frame, selectmode=tk.MULTIPLE, height=5)
        self.habit_list.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Pomodoro Timer Section
        self.timer_frame = tk.LabelFrame(self.main_frame, text="Pomodoro Timer", padx=10, pady=10)
        self.timer_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.timer_label = tk.Label(self.timer_frame, text="Timer: 00:00", font=("Arial", 24))
        self.timer_label.grid(row=0, column=0)

        self.timer_entry = tk.Entry(self.timer_frame, width=10)
        self.timer_entry.insert(0, "25")  # Default timer duration
        self.timer_entry.grid(row=1, column=0, pady=5)

        self.start_timer_button = tk.Button(self.timer_frame, text="Start Timer", command=self.start_timer)
        self.start_timer_button.grid(row=2, column=0, pady=5)

        # Notes Section
        self.notes_frame = tk.LabelFrame(self.main_frame, text="Notes", padx=10, pady=10)
        self.notes_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        self.notes_text = tk.Text(self.notes_frame, height=5, width=50)
        self.notes_text.grid(row=0, column=0, sticky="nsew")
        self.save_notes_button = tk.Button(self.notes_frame, text="Save Notes", command=self.save_notes)
        self.save_notes_button.grid(row=1, column=0, pady=5)

    def add_task(self):
        task = simpledialog.askstring("Task", "Enter a new task:")
        if task:
            self.task_list.append(task)
            self.task_display.insert(tk.END, task)

    def start_timer(self):
        try:
            minutes = int(self.timer_entry.get())
            if minutes <= 0:
                raise ValueError("Timer duration must be greater than 0.")
            self.timer_thread = threading.Thread(target=self.pomodoro_countdown, args=(minutes * 60,))
            self.timer_thread.daemon = True  # Make the thread a daemon so it exits when the main program exits
            self.timer_thread.start()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def pomodoro_countdown(self, seconds):
        while seconds:
            mins, secs = divmod(seconds, 60)
            time_str = f"{mins:02}:{secs:02}"
            self.root.after(0, self.update_timer_label, time_str)
            time.sleep(1)
            seconds -= 1
        self.root.after(0, self.timer_finished)

    def update_timer_label(self, time_str):
        self.timer_label.config(text=f"Timer: {time_str}")

    def timer_finished(self):
        messagebox.showinfo("Timer", "Time's up! Take a break.")

    def save_notes(self):
        notes = self.notes_text.get("1.0", tk.END).strip()
        with open("notes.txt", "w") as file:
            file.write(notes)
        messagebox.showinfo("Notes", "Notes saved successfully!")

    def add_habit(self):
        habit = self.habit_entry.get()
        if habit:
            self.habit_list.insert(tk.END, habit)
            self.habit_entry.delete(0, tk.END)

    def start_adhd_test(self):
        self.adhd_test_window = tk.Toplevel(self.root)
        self.adhd_test_window.title("ADHD Test")
        self.adhd_test_window.geometry("600x400")

        self.current_question = 0
        self.user_responses = []

        self.question_label = tk.Label(self.adhd_test_window, text=questions[self.current_question], wraplength=400, justify="left")
        self.question_label.pack(pady=20)

        self.answer_var = tk.StringVar()
        self.radio_buttons = []
        for i in range(len(answers[self.current_question])):
            rb = tk.Radiobutton(self.adhd_test_window, text=answers[self.current_question][i], variable=self.answer_var, value=answers[self.current_question][i])
            rb.pack(anchor="w")
            self.radio_buttons.append(rb)

        self.next_button = tk.Button(self.adhd_test_window, text="Next", command=self.next_question)
        self.next_button.pack(pady=20)

    def next_question(self):
        selected_answer = self.answer_var.get()
        if not selected_answer:
            messagebox.showwarning("Warning", "Please select an answer!")
            return

        self.user_responses.append(selected_answer)
        self.current_question += 1

        if self.current_question < len(questions):
            self.question_label.config(text=questions[self.current_question])
            for i, option in enumerate(answers[self.current_question]):
                self.radio_buttons[i].config(text=option, value=option)
            self.answer_var.set(None)
        else:
            self.show_result()

    def show_result(self):
        total_score = sum(scoring[response] for response in self.user_responses if response in scoring)

        if total_score <= 10:
            result = "Low likelihood of ADHD."
        elif total_score <= 20:
            result = "Moderate likelihood of ADHD."
        else:
            result = "High likelihood of ADHD."

        messagebox.showinfo("ADHD Test Result", f"Your total score is {total_score}. {result}")
        self.adhd_test_window.destroy()

    def export_data(self):
        # Get all tasks
        all_tasks = [self.task_display.get(i) for i in range(self.task_display.size())]

        # Get all habits
        all_habits = [self.habit_list.get(i) for i in range(self.habit_list.size())]

        # Get notes
        notes = self.notes_text.get("1.0", tk.END).strip()

        # Get test results if available
        if hasattr(self, 'user_responses') and self.user_responses:
            total_score = sum(scoring[response] for response in self.user_responses if response in scoring)
            if total_score <= 10:
                result = "Low likelihood of ADHD."
            elif total_score <= 20:
                result = "Moderate likelihood of ADHD."
            else:
                result = "High likelihood of ADHD."
            test_results = f"ADHD Test Score: {total_score}\n{result}"
        else:
            test_results = "No ADHD test results available."

        # Combine all data
        export_data = (
            "===== Tasks =====\n" + "\n".join(all_tasks) + "\n\n" +
            "===== Habits =====\n" + "\n".join(all_habits) + "\n\n" +
            "===== Notes =====\n" + notes + "\n\n" +
            "===== Test Results =====\n" + test_results
        )

        # Save to file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(export_data)
            messagebox.showinfo("Export Successful", "Data exported successfully!")

# ADHD Test Questions
questions = [
    "1. How often do you have trouble wrapping up the final details of a project?",
    "2. How often do you have difficulty getting things in order when you have to do a task that requires organization?",
    "3. How often do you have problems remembering appointments or obligations?",
    "4. When you have a task that requires a lot of thought, how often do you avoid or delay getting started?",
    "5. How often do you fidget or squirm with your hands or feet when you have to sit down for a long time?",
    "6. How often do you feel overly active and compelled to do things, like you were driven by a motor?",
    "7. How often do you make careless mistakes when working on a boring or difficult project?",
    "8. How often do you forget to return calls, pay bills, or keep appointments?"
]

# ADHD Test Answer Choices
answers = [
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"],
    ["Never", "Rarely", "Sometimes", "Often", "Very Often"]
]

# ADHD Test Scoring
scoring = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Often": 3,
    "Very Often": 4
}

if __name__ == "__main__":
    root = tk.Tk()
    app = ADHDApp(root)
    root.mainloop()
