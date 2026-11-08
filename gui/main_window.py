import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from core.file_detector import detect_file_type
from core.router import select_route
from core.word_processor import process_word_file


class DocumentApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Document Processing App')
        self.root.geometry('760x620')
        self.root.minsize(550, 480)
        self.selected_file = ''
        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=18)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='Document Processing App',
                  font=('Arial', 17, 'bold')).pack(pady=(0, 14))
        ttk.Button(frame, text='Upload File', command=self.upload_file).pack()
        self.file_label = ttk.Label(frame, text='No file selected', wraplength=690)
        self.file_label.pack(pady=9)
        ttk.Label(frame, text='Select Output Type:').pack(pady=(8, 4))
        self.output_var = tk.StringVar(value='Word')
        ttk.Combobox(frame, textvariable=self.output_var, values=['Word', 'Excel'],
                     state='readonly', width=17).pack()
        ttk.Label(frame, text='Instruction:').pack(pady=(14, 4))
        self.instruction_text = tk.Text(frame, height=5, wrap='word')
        self.instruction_text.pack(fill='x')
        ttk.Button(frame, text='Process', command=self.process_file).pack(pady=16)
        ttk.Label(frame, text='Status / Result:').pack(anchor='w')
        result_frame = ttk.Frame(frame)
        result_frame.pack(fill='both', expand=True, pady=(5, 0))
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side='right', fill='y')
        self.result_box = tk.Text(result_frame, height=10, state='disabled',
                                  wrap='word', yscrollcommand=scrollbar.set)
        self.result_box.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.result_box.yview)

    def upload_file(self):
        path = filedialog.askopenfilename(
            title='Select a file',
            filetypes=[('Supported files', '*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.pdf *.docx *.xlsx'),
                       ('All files', '*.*')])
        if path:
            self.selected_file = path
            self.file_label.config(text=path)

    def process_file(self):
        if not self.selected_file:
            messagebox.showwarning('Missing file', 'Please select a file first.')
            return
        if not Path(self.selected_file).is_file():
            messagebox.showerror('Missing file', 'The selected file no longer exists.')
            return
        output = self.output_var.get()
        instruction = self.instruction_text.get('1.0', 'end').strip()
        input_type = detect_file_type(self.selected_file)
        route = select_route(input_type, output)
        try:
            if route == 'edit_word':
                result = process_word_file(self.selected_file, instruction,
                                           str(Path(__file__).resolve().parents[1] / 'output'))
            else:
                result = (f'Input type: {input_type}\nOutput type: {output}\n'
                          f'Instruction: {instruction or "No instruction provided"}\n'
                          f'Selected route: {route}\n'
                          'Status: This processing route is not implemented yet.')
        except Exception as exc:
            result = f'Processing failed: {type(exc).__name__}: {exc}'
        self.set_result(result)

    def set_result(self, text):
        self.result_box.config(state='normal')
        self.result_box.delete('1.0', 'end')
        self.result_box.insert('1.0', text)
        self.result_box.config(state='disabled')


def run_app():
    root = tk.Tk()
    DocumentApp(root)
    root.mainloop()
