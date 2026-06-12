import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
from PIL import Image, ImageTk
import numpy as np


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор изображений OpenCV")
        self.root.geometry("1100x700")

        # Оригинальное и текущее изображения (в формате OpenCV / BGR)
        self.orig_img = None
        self.current_img = None

        self.create_widgets()

    def create_widgets(self):
        # --- Левая панель управления ---
        control_panel = ttk.LabelFrame(self.root, text=" Управление ", padding=10)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Блок загрузки
        ttk.Label(control_panel, text="1. Источник:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        ttk.Button(control_panel, text="Загрузить JPG/PNG", command=self.load_file).pack(fill=tk.X, pady=2)
        ttk.Button(control_panel, text="Снимок с веб-камеры", command=self.make_snapshot).pack(fill=tk.X, pady=2)

        ttk.Separator(control_panel, orient='horizontal').pack(fill=tk.X, pady=10)

        # Блок каналов
        ttk.Label(control_panel, text="2. Цветовой канал:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        self.channel_var = tk.StringVar(value="Оригинал")
        for ch in ["Оригинал", "Красный", "Зеленый", "Синий"]:
            ttk.Radiobutton(control_panel, text=ch, value=ch, variable=self.channel_var,
                            command=self.apply_filters).pack(anchor=tk.W)

        ttk.Separator(control_panel, orient='horizontal').pack(fill=tk.X, pady=10)

        # Блок изменения размера
        ttk.Label(control_panel, text="3. Изменить размер:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        size_frame = ttk.Frame(control_panel)
        size_frame.pack(fill=tk.X)
        ttk.Label(size_frame, text="Ш:").pack(side=tk.LEFT)
        self.width_entry = ttk.Entry(size_frame, width=6)
        self.width_entry.pack(side=tk.LEFT, padx=2)
        ttk.Label(size_frame, text="В:").pack(side=tk.LEFT)
        self.height_entry = ttk.Entry(size_frame, width=6)
        self.height_entry.pack(side=tk.LEFT, padx=2)
        ttk.Button(control_panel, text="Применить размер", command=self.resize_image).pack(fill=tk.X, pady=5)

        ttk.Separator(control_panel, orient='horizontal').pack(fill=tk.X, pady=10)

        # Блок яркости
        ttk.Label(control_panel, text="4. Понизить яркость:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        bright_frame = ttk.Frame(control_panel)
        bright_frame.pack(fill=tk.X)
        ttk.Label(bright_frame, text="Значение:").pack(side=tk.LEFT)
        self.bright_entry = ttk.Entry(bright_frame, width=6)
        self.bright_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, text="Уменьшить яркость", command=self.decrease_brightness).pack(fill=tk.X, pady=5)

        ttk.Separator(control_panel, orient='horizontal').pack(fill=tk.X, pady=10)

        # Блок рисования прямоугольника
        ttk.Label(control_panel, text="5. Синий прямоугольник:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        rect_frame = ttk.Frame(control_panel)
        rect_frame.pack(fill=tk.X)
        ttk.Label(rect_frame, text="X1:").grid(row=0, column=0)
        self.x1_entry = ttk.Entry(rect_frame, width=5)
        self.x1_entry.grid(row=0, column=1, padx=2)
        ttk.Label(rect_frame, text="Y1:").grid(row=0, column=2)
        self.y1_entry = ttk.Entry(rect_frame, width=5)
        self.y1_entry.grid(row=0, column=3, padx=2)

        ttk.Label(rect_frame, text="X2:").grid(row=1, column=0, pady=5)
        self.x2_entry = ttk.Entry(rect_frame, width=5)
        self.x2_entry.grid(row=1, column=1, padx=2, pady=5)
        ttk.Label(rect_frame, text="Y2:").grid(row=1, column=2, pady=5)
        self.y2_entry = ttk.Entry(rect_frame, width=5)
        self.y2_entry.grid(row=1, column=3, padx=2, pady=5)

        ttk.Button(control_panel, text="Нарисовать", command=self.draw_rectangle).pack(fill=tk.X, pady=5)

        ttk.Button(control_panel, text="Сбросить изменения", command=self.reset_image).pack(fill=tk.X, pady=20)

        # --- Правая панель просмотра ---
        self.preview_panel = ttk.LabelFrame(self.root, text=" Просмотр изображения ", padding=10)
        self.preview_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.image_label = ttk.Label(self.preview_panel, text="Изображение не загружено")
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # --- Нижняя строка состояния (Отклик приложения) ---
        self.status_var = tk.StringVar(value="Статус: Ожидание действий пользователя...")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # 1. Загрузка файла
    def load_file(self):
        from tkinter import filedialog
        import numpy as np
        import cv2

        # 1. Открываем диалоговое окно выбора файла
        file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )

        # Если пользователь закрыл окно и не выбрал файл
        if not file_path:
            return

        try:
            # 2. Читаем файл через numpy (чтобы не было проблем с русскими буквами в пути)
            bytes_img = np.fromfile(file_path, dtype=np.uint8)
            img = cv2.imdecode(bytes_img, cv2.IMREAD_COLOR)

            # 3. Проверяем, что картинка успешно прочиталась
            if img is None:
                self.set_status("Ошибка: файл поврежден или не поддерживается")
                return

            # 4. Сохраняем картинку в переменные класса (ДОБАВИЛИ ORIG_IMG)
            self.orig_img = img.copy()     # Чистый оригинал для сброса фильтров
            self.current_img = img         # Текущее рабочее изображение
            self.display_img = img.copy()  # Изображение для вывода на экран

            # 5. Вызываем метод отрисовки
            self.update_view()
            self.set_status(f"Файл успешно загружен: {file_path.split('/')[-1]}")

        except Exception as e:
            self.set_status(f"Ошибка при открытии: {str(e)}")

    # 2. Снимок с веб-камеры
    def make_snapshot(self):
        self.set_status("Попытка подключения к веб-камере...")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            error_msg = (
                "Не удалось подключиться к веб-камере.\n\n"
                "Возможные пути решения проблемы:\n"
                "1. Проверьте физическое подключение камеры к USB-порту.\n"
                "2. Убедитесь, что камера не используется другим приложением (Zoom, Skype, браузер).\n"
                "3. В настройках конфиденциальности ОС разрешите приложениям доступ к камере.\n"
                "4. Проверьте/обновите драйверы веб-камеры в диспетчере устройств."
            )
            messagebox.showerror("Ошибка камеры", error_msg)
            self.set_status("Ошибка: Веб-камера недоступна.")
            return

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            messagebox.showerror("Ошибка", "Не удалось захватить кадр с камеры.")
            self.set_status("Ошибка: Кадр не захвачен.")
            return

        self.orig_img = frame
        self.current_img = frame.copy()
        self.channel_var.set("Оригинал")
        self.update_view()
        self.set_status("Снимок с веб-камеры успешно сделан.")

    # 3. Выбор цветового канала
    def apply_filters(self):
        if self.current_img is None:
            self.set_status("Предупреждение: Сначала загрузите изображение.")
            return
        self.update_view()
        self.set_status(f"Отображен канал: {self.channel_var.get()}")

    # 4. Изменение размера
    def resize_image(self):
        if self.current_img is None:
            messagebox.showwarning("Внимание", "Изображение не загружено.")
            return

        try:
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            if w <= 0 or h <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Ширина и высота должны быть целыми положительными числами!")
            self.set_status("Ошибка: Некорректный ввод размеров.")
            return

        # Защита от зависаний (ограничение на слишком гигантский размер)
        if w > 5000 or h > 5000:
            messagebox.showwarning("Внимание", "Размер слишком велик! Максимум 5000x5000.")
            return

        self.current_img = cv2.resize(self.current_img, (w, h), interpolation=cv2.INTER_AREA)
        self.update_view()
        self.set_status(f"Размер изменен на {w}x{h}.")

    # 5. Понижение яркости
    def decrease_brightness(self):
        if self.current_img is None:
            messagebox.showwarning("Внимание", "Изображение не загружено.")
            return

        try:
            val = int(self.bright_entry.get())
            if val < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Значение яркости должно быть целым неотрицательным числом!")
            self.set_status("Ошибка: Некорректное значение яркости.")
            return

        # Безопасное вычитание с обрезанием по нижней границе (0), чтобы не уйти в круговой сдвиг байтов
        hsv = cv2.cvtColor(self.current_img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # Защита от переполнения типов (uint8) через numpy clip
        v = np.clip(v.astype(int) - val, 0, 255).astype(np.uint8)

        final_hsv = cv2.merge((h, s, v))
        self.current_img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        self.update_view()
        self.set_status(f"Яркость уменьшена на {val}.")

    # 6. Рисование прямоугольника
    def draw_rectangle(self):
        if self.current_img is None:
            messagebox.showwarning("Внимание", "Изображение не загружено.")
            return

        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Координаты прямоугольника должны быть целыми числами!")
            self.set_status("Ошибка: Некорректные координаты.")
            return

        img_h, img_w = self.current_img.shape[:2]

        # Проверка выхода за границы картинки
        if not (0 <= x1 < img_w and 0 <= x2 <= img_w and 0 <= y1 < img_h and 0 <= y2 <= img_h):
            messagebox.showwarning("Внимание", f"Координаты выходят за рамки изображения (Макс: {img_w}x{img_h})")
            self.set_status("Ошибка: Выход координат за границы.")
            return

        # В OpenCV цвет BGR. Синий цвет = (255, 0, 0). Толщина линии = 2 пикселя
        cv2.rectangle(self.current_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        self.update_view()
        self.set_status(f"Нарисован синий прямоугольник: ({x1}, {y1}) -> ({x2}, {y2}).")

    # Сброс к первоначальному фото
    def reset_image(self):
        # 1. Проверяем, загружен ли вообще оригинал
        if self.orig_img is None:
            self.set_status("Ошибка: нет исходного изображения для сброса")
            return

        # 2. Исправляем опечатку и копируем оригинал
        self.current_img = self.orig_img.copy()

        # 3. Сбрасываем фильтр в интерфейсе (если у вас Combobox)
        if hasattr(self, 'channel_var'):
            self.channel_var.set("Оригинал")

        # 4. Обновляем экран
        self.update_view()
        self.set_status("Изображение сброшено к оригиналу")

    # Обновление изображения в окне (с подгонкой под размеры экрана без изменения самой матрицы данных)
    def update_view(self):
        if self.current_img is None:
            return

        # 1. Выделяем нужный канал на лету для демонстрации
        display_img = self.current_img.copy()
        channel = self.channel_var.get()

        if channel != "Оригинал":
            # Разделяем каналы только если выбран конкретный цвет
            b, g, r = cv2.split(display_img)
            zeros = np.zeros_like(b)

            if channel == "Красный":
                display_img = cv2.merge([zeros, zeros, r])
            elif channel == "Зеленый":
                display_img = cv2.merge([zeros, g, zeros])
            elif channel == "Синий":
                display_img = cv2.merge([b, zeros, zeros])

        # 2. Конвертируем BGR (OpenCV) в RGB (Pillow/Tkinter)
        rgb_img = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)

        # 3. Умное масштабирование превью, чтобы большая картинка не ломала интерфейс
        max_w, max_h = 750, 600
        pil_img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

        # 4. Вывод в интерфейс
        tk_img = ImageTk.PhotoImage(image=pil_img)
        self.image_label.configure(image=tk_img, text="")
        self.image_label.image = tk_img  # сохраняем ссылку, чтобы сборщик мусора её не удалил


    def set_status(self, text):
        self.status_var.set(f"Статус: {text}")


if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
