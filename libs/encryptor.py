from transformers import AutoTokenizer
from random import randint
import ast

class Encryptor:
    def __init__(self, tokenizer_path, key_file, encrypted_file):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.key_file = key_file  # Файл ключа изначально не выбран
        self.encrypted_file = encrypted_file  # Файл для расшифровки изначально не выбран

    def encrypt(self, text_original):
        """
        Метод для зашифровки.
        """
        # Инициализация ключей
        keys = []
        with open(self.key_file, 'w') as file:
            for _ in range(len(text_original)):
                file.write(str(randint(1, 100)) + "\n")
        
        with open(self.key_file, 'r') as file:
            for line in file:
                keys.append(int(line.strip()))
        
        # Процесс шифрования
        text_encoded = self.tokenizer.encode(text_original)
        assert len(text_encoded) < len(keys), (
            f"Длина текста превышает длину ключа. Длина текста: {len(text_encoded)}, Длина ключа: {len(keys)}"
        )

        # Шифрование с использованием ключей
        text_encoded_v2 = [text_encoded[i] * keys[i] for i in range(len(text_encoded))]
        text_encoded_v3 = [text_encoded_v2[i] - keys[i] * keys[0] for i in range(len(text_encoded_v2))]

        # Сохранение зашифрованного сообщения
        with open(self.encrypted_file, 'w') as file:
            file.write(str(text_encoded_v3))

        return "Сообщение успешно зашифровано и сохранено!"

    def decrypt(self):
        """
        Метод для расшифровки.
        """
        # Проверка: выбраны ли оба файла
        if not self.key_file or not self.encrypted_file:
            raise ValueError("Файл ключа или файл для расшифровки не выбран.")

        # Загрузка ключей
        keys = []
        with open(self.key_file, 'r') as file:
            for line in file:
                keys.append(int(line.strip()))

        # Загрузка зашифрованного сообщения
        with open(self.encrypted_file, 'r') as file:
            encrypted = ast.literal_eval(file.read())

        # Процесс расшифровки
        decrypted_text = ""
        for i in range(len(encrypted)):
            decrypted_value = int(encrypted[i]) + int(keys[i]) * keys[0]
            decrypted_value = int(decrypted_value) / int(keys[i])
            decrypted_text += self.tokenizer.decode(int(decrypted_value))

        return decrypted_text

    def set_encrypted_file(self, filepath):
        """
        Метод для установки нового пути к зашифрованному файлу.
        """
        self.encrypted_file = filepath

    def set_key_file(self, filepath):
        """
        Метод для установки нового пути к ключу для отшифровки файла.
        """
        self.key_file = filepath

    def set_tokenizer_path(self, tokenizer_path):
        """
        Метод для установки нового пути к токенайзеру и обновления токенайзера.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        return f"Путь к токенайзеру успешно обновлен на: {tokenizer_path}"
