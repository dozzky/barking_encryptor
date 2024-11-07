import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox, Button, Label, Scrollbar, filedialog
import os
from libs.encryptor import Encryptor

# Функция для работы с интерфейсом
def encrypt_text():
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        try:
            message = encryptor.encrypt(text)
            text_to_display = message + f"\n Ключ находится в {key_file_path} \n Зашифрованный текст в {encrypted_file_path}"
            result_text.set(text_to_display)
        except ValueError as e:
            messagebox.showwarning("Ошибка", str(e))
    else:
        messagebox.showwarning("Ошибка", "Введите текст для шифрования.")

def decrypt_text():
    try:
        # Выполняем расшифровку
        decrypted_message = encryptor.decrypt()
        
        # Создаем новое окно для отображения результата
        result_window = Toplevel(root)
        result_window.title("Результат расшифровки")
        result_window.geometry("1200x800")
        
        # Виджет для отображения расшифрованного текста
        result_text_widget = tk.Text(result_window, wrap=tk.WORD)
        result_text_widget.insert(tk.END, decrypted_message)
        result_text_widget.config(state=tk.DISABLED)  # Запретить редактирование
        result_text_widget.pack(expand=True, fill=tk.BOTH)
        
        # Добавление полосы прокрутки
        scrollbar = tk.Scrollbar(result_window, command=result_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_text_widget.config(yscrollcommand=scrollbar.set)
        
    except ValueError as e:
        messagebox.showwarning("Ошибка", str(e))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось расшифровать сообщение: {e}")

def custom_file_dialog(file_type, callback):
    # Создаем окно Toplevel
    dialog = Toplevel(root)
    dialog.title(f"Выберите файл {file_type}")
    dialog.geometry("800x600")  # Устанавливаем размер окна

    # Текущая директория
    current_directory = os.getcwd()
    selected_file = None

    # Функция для обновления списка файлов и папок
    def update_file_list(directory):
        file_list.delete(0, tk.END)
        try:
            for entry in os.listdir(directory):
                file_list.insert(tk.END, entry)
        except PermissionError:
            pass

    # Функция для обработки выбора файла
    def select_file():
        nonlocal selected_file
        selected_file = os.path.join(current_directory, file_list.get(file_list.curselection()))
        if os.path.isfile(selected_file):
            callback(selected_file)
            dialog.destroy()

    # Функция для обработки перехода в папку
    def change_directory():
        nonlocal current_directory
        selected_folder = file_list.get(file_list.curselection())
        new_path = os.path.join(current_directory, selected_folder)
        if os.path.isdir(new_path):
            current_directory = new_path
            update_file_list(current_directory)

    # Виджеты для отображения списка файлов
    label = Label(dialog, text="Выберите файл:")
    label.pack(pady=5)
    
    scrollbar = Scrollbar(dialog)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    file_list = Listbox(dialog, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
    file_list.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    
    scrollbar.config(command=file_list.yview)

    # Кнопки
    select_button = Button(dialog, text="Выбрать", command=select_file)
    select_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    cancel_button = Button(dialog, text="Отмена", command=dialog.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Обновляем список файлов и папок в начальной директории
    update_file_list(current_directory)

    # Связываем двойной клик с переходом в папку
    file_list.bind("<Double-Button-1>", lambda event: change_directory())

    dialog.mainloop()

# Обработка выбора файла для расшифровки
def choose_encrypted_file():
    custom_file_dialog("для расшифровки", lambda filepath: set_file("encrypted", filepath))

# Обработка выбора файла ключа
def choose_key_file():
    custom_file_dialog("ключа", lambda filepath: set_file("key", filepath))

# Обработка выбора пути к токенайзеру
def choose_tokenizer_path():
    tokenizer_path = filedialog.askdirectory(title="Выберите папку токенизатору")
    if tokenizer_path:
        encryptor.set_tokenizer_path(tokenizer_path)
        result_text.set(f"Путь к токенайзеру выбран:\n{tokenizer_path}")

# Функция для установки файла и обновления результата
def set_file(file_type, filepath):
    if file_type == "encrypted":
        encryptor.set_encrypted_file(filepath)
        result_text.set(f"Файл для расшифровки выбран:\n{filepath}")
    elif file_type == "key":
        encryptor.set_key_file(filepath)
        result_text.set(f"Файл ключа выбран:\n{filepath}")

# Инициализация окна
root = tk.Tk()
root.title("Barking ver. 0.3")

# Пути к файлам
tokenizer_path = 'libs/tokenizer'
key_file_path = 'files/key.txt'
encrypted_file_path = 'files/encrypted.txt'
encryptor = Encryptor(tokenizer_path, key_file_path, encrypted_file_path)

# Поле для ввода текста
text_label = tk.Label(root, text="Введите текст для шифрования:", highlightthickness = 5)
text_label.pack()
text_entry = tk.Text(root, height=10, width=80)
text_entry.pack()

# Контейнер для кнопок шифрования и расшифровки
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# Кнопки шифрования и расшифровки
encrypt_button = tk.Button(frame_buttons, text="Зашифровать", command=encrypt_text)
encrypt_button.pack(side=tk.LEFT, padx=5)

decrypt_button = tk.Button(frame_buttons, text="Расшифровать", command=decrypt_text)
decrypt_button.pack(side=tk.LEFT, padx=5)

# Контейнер для кнопок выбора файлов
frame_file_buttons = tk.Frame(root)
frame_file_buttons.pack(pady=10)

# Кнопки для выбора файла, ключа и пути к токенизатору
choose_file_button = tk.Button(frame_file_buttons, text="Выбрать файл для расшифровки", command=choose_encrypted_file)
choose_file_button.pack(side=tk.LEFT, padx=5)

choose_key_button = tk.Button(frame_file_buttons, text="Выбрать файл ключа", command=choose_key_file)
choose_key_button.pack(side=tk.LEFT, padx=5)

choose_tokenizer_button = tk.Button(frame_file_buttons, text="Выбрать путь к токенизатору", command=choose_tokenizer_path)
choose_tokenizer_button.pack(side=tk.LEFT, padx=5)

# Поле для вывода результата шифрования или расшифровки
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400, justify="left")
result_label.pack()

# Запуск интерфейса
root.mainloop()