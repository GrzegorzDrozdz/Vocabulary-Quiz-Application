import random
import tkinter as tk
import matplotlib.pyplot as plt
import Levenshtein
from tkinter import filedialog

def load_words(file_path):
    word_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            english, translation = line.strip().split('-')
            word_dict[english] = translation
    return word_dict

def save_words(file_path, words_dict):
    with open(file_path, 'w', encoding='utf-8') as file:
        for english, translation in words_dict.items():
            file.write(f"{english}-{translation}\n")

def standardization_Levenshtein(w1, w2):
    l = Levenshtein.distance(w1, w2)
    standardization = l / max(len(w1), len(w2))
    return standardization

class Quiz:
    def __init__(self, master, words):
        self.master = master
        self.words = words
        self.total_count = len(words)
        self.easy_words = {}
        self.medium_words = {}
        self.hard_words = {}
        self.keys_list = list(words.keys())
        self.create_widgets()

    def create_widgets(self):
        self.label_question = tk.Label(self.master, text="", font=('Arial', 20, 'bold'))
        self.entry_answer = tk.Entry(self.master,font=('Arial', 18))
        self.result_label = tk.Label(self.master, text="", font=('Arial', 18,'bold'))
        self.button_check_answer = tk.Button(self.master, text="Sprawdź odpowiedź", command=self.check_answer)

        self.label_question.pack(pady=10)
        self.entry_answer.pack(pady=10)
        self.button_check_answer.pack(pady=10)
        self.result_label.pack(pady=10)

        self.next_question()

    def next_question(self):
        if not self.keys_list:
            self.show_results()
            return

        english = random.choice(self.keys_list)
        translation = self.words[english]
        self.current_english = english

        self.label_question.config(text=f"Przetłumacz słowo '{english}':")
        self.result_label.config(text="")
        self.entry_answer.delete(0, tk.END)

    def check_answer(self):
        answer = self.entry_answer.get().strip().lower()
        translation = self.words[self.current_english].lower()

        if answer == translation:
            self.result_label.config(text="Poprawna odpowiedź!", fg="green")
            self.easy_words[self.current_english] = translation
        elif standardization_Levenshtein(answer, translation) <= 0.25:
            self.result_label.config(text="Mały błąd!", fg="orange")
            self.medium_words[self.current_english] = translation
        else:
            self.result_label.config(text="Nieprawidłowa odpowiedź", fg="red")
            self.hard_words[self.current_english] = translation

        if self.current_english in self.keys_list:
            self.keys_list.remove(self.current_english)

        self.master.after(2000, self.clear_result)
        self.master.after(2000, self.next_question)

    def clear_result(self):
        self.result_label.config(text="")

    def show_results(self):
        save_words('easy_words.txt', self.easy_words)
        save_words('medium_words.txt', self.medium_words)
        save_words('hard_words.txt', self.hard_words)

        labels = ['Poprawne', 'Literówka', 'Błędne']
        sizes = [len(self.easy_words), len(self.medium_words), len(self.hard_words)]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.show()

        self.master.destroy()

def choose_file():
    file_path = filedialog.askopenfilename(title="Wybierz plik ze słówkami", filetypes=[("Pliki tekstowe", "*.txt")])

    if file_path:
        words = load_words(file_path)
        return words
    else:
        return {}

root = tk.Tk()
root.lift()
words_dict = choose_file()
root.title("Quiz App")
quiz_app = Quiz(root, words_dict)
root.mainloop()
