import tkinter as tk
from tkinter import messagebox
import re

class Parser:
    def __init__(self):
        self.tokens = []
        self.pos = 0

    def parse(self, equation):
        self.tokens = self.tokenize(equation)
        self.pos = 0
        return self.expression()

    def tokenize(self, equation):
        # Tokenize equation into numbers, operators, and parentheses
        return re.findall(r'\w+|[-+*/()]', equation)

    def consume(self, expected_token):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == expected_token:
            self.pos += 1
        else:
            raise SyntaxError("Expected '{}'".format(expected_token))

    def factor(self):
        if self.tokens[self.pos] == '(':
            self.consume('(')
            result = self.expression()
            self.consume(')')
            return result
        else:
            try:
                result = float(self.tokens[self.pos])
                self.pos += 1
                return result
            except ValueError:
                raise SyntaxError("Invalid number")

    def term(self):
        result = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('*', '/'):
            op = self.tokens[self.pos]
            self.pos += 1
            operand = self.factor()
            if op == '*':
                result *= operand
            else:
                result /= operand
        return result

    def expression(self):
        result = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('+', '-'):
            op = self.tokens[self.pos]
            self.pos += 1
            operand = self.term()
            if op == '+':
                result += operand
            else:
                result -= operand
        return result

class ParserApp:
    def __init__(self, master):
        self.master = master
        master.title("Parser GUI")

        self.parser = Parser()

        self.input_label = tk.Label(master, text="Enter an equation:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5)

        self.input_entry = tk.Entry(master)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        self.parse_button = tk.Button(master, text="Parse", command=self.parse_equation)
        self.parse_button.grid(row=0, column=2, padx=5, pady=5)

        self.output_label = tk.Label(master, text="Output:")
        self.output_label.grid(row=1, column=0, padx=5, pady=5)

        self.output_text = tk.Text(master, height=5, width=30)
        self.output_text.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.grammar_label = tk.Label(master, text="Grammar used:")
        self.grammar_label.grid(row=2, column=0, padx=5, pady=5)

        self.grammar_text = tk.Text(master, height=5, width=30)
        self.grammar_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

    def parse_equation(self):
        equation = self.input_entry.get()
        try:
            result = self.parser.parse(equation)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, str(result))
            self.grammar_text.delete(1.0, tk.END)
            self.grammar_text.insert(tk.END, "Modified grammar used")
        except SyntaxError as e:
            messagebox.showerror("Syntax Error", str(e))

def main():
    root = tk.Tk()
    app = ParserApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
