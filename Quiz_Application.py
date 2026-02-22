import json
import random
import time
import tkinter as tk
from tkinter import messagebox

class QuizGUI:
    def __init__(self, root, question_file):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("600x400")

        self.questions = self.load_questions(question_file)
        random.shuffle(self.questions)

        self.score = 0
        self.current_question_index = 0
        self.start_time = time.time()

        self.question_label = tk.Label(root, text="", wraplength=500, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", width=40, font=("Arial", 12),
                            command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.load_question()

    def load_questions(self, file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "questions.json file not found!")
            self.root.destroy()

    def load_question(self):
        if self.current_question_index >= len(self.questions):
            self.show_result()
            return

        question_data = self.questions[self.current_question_index]
        self.question_label.config(text=question_data["question"])

        self.options = question_data["options"][:]
        self.correct_answer = self.options[question_data["answer"] - 1]

        random.shuffle(self.options)

        for i in range(4):
            self.buttons[i].config(text=self.options[i])

    def check_answer(self, index):
        selected_option = self.options[index]

        if selected_option == self.correct_answer:
            self.score += 1
            self.current_question_index += 1
            self.load_question()
        else:
            messagebox.showinfo("Wrong Answer", "Wrong answer! Quiz Over.")
            self.show_result()

    def show_result(self):
        end_time = time.time()
        total_time = round(end_time - self.start_time, 2)

        messagebox.showinfo(
            "Final Result",
            f"Score: {self.score}/{len(self.questions)}\n"
            f"Total Time: {total_time} seconds"
        )
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGUI(root, "questions.json")
    root.mainloop()