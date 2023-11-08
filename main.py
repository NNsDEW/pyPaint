import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw
import keyboard
import pyautogui  # Импортируем pyautogui

import sys
print(sys.path)


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ГЕЙСКАЯ РЕВОЛЮЦИЯ В ГЕРМАНИЙ")
        self.root.iconbitmap("ico.ico")  # Set the icon

        self.current_color = "black"
        self.current_tool = "brush"
        self.brush_size = 5

        self.canvas_width = 800
        self.canvas_height = 400

        self.canvas = tk.Canvas(self.root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.undo_stack = []

        # Create a top menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Create a "Файл" menu with "Сохранить" option
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить (Shift + S)", command=self.save_image)

        # Create a "Формат" sub-menu
        format_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Формат", menu=format_menu)
        format_menu.add_command(label="Изменить размер холста", command=self.change_canvas_size)

        # Create a "Справка" menu with "О программе" option
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about_dialog)

        # Create a "Топ секрет" menu
        secret_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Топ секрет", menu=secret_menu)
        secret_menu.add_command(label="Сообщение Филу", command=self.secret_message)

        button_frame = ttk.Frame(self.root)
        button_frame.pack()

        self.brush_button = ttk.Button(button_frame, text="Кисть", command=self.use_brush)
        self.eraser_button = ttk.Button(button_frame, text="Ластик", command=self.use_eraser)
        self.clear_button = ttk.Button(button_frame, text="Очистить слой", command=self.clear_canvas)
        self.color_button = ttk.Button(button_frame, text="Выбрать цвет", command=self.select_color)
        self.undo_button = ttk.Button(button_frame, text="Отменить", command=self.undo)

        self.brush_button.pack(side="left", fill="both", expand=True)
        self.eraser_button.pack(side="left", fill="both", expand=True)
        self.clear_button.pack(side="left", fill="both", expand=True)
        self.color_button.pack(side="left", fill="both", expand=True)
        #self.undo_button.pack(side="left", fill="both", expand=True)

        self.brush_size_label = ttk.Label(button_frame, text="Размер кисти:")
        self.brush_size_label.pack(side="left")

        self.brush_size_scale = ttk.Scale(button_frame, from_=1, to=20, orient="horizontal", command=self.change_brush_size)
        self.brush_size_scale.set(self.brush_size)
        self.brush_size_scale.pack(side="left")

        # Bind the Shift + S key combination to the save_image function
        keyboard.add_hotkey("shift+s", self.save_image)
        # Bind the Ctrl + Z key combination to the undo function using the keyboard library
        keyboard.add_hotkey("ctrl+z", self.undo)

    def change_brush_size(self, event):
        self.brush_size = self.brush_size_scale.get()

    def paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)

        if self.current_tool == "brush":
            item = self.canvas.create_oval(x1, y1, x2, y2, fill=self.current_color, outline=self.current_color)
            self.undo_stack.append(item)
        elif self.current_tool == "eraser":
            item = self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")
            self.undo_stack.append(item)

    def reset(self, event):
        pass

    def use_brush(self):
        self.current_tool = "brush"

    def use_eraser(self):
        self.current_tool = "eraser"

    def clear_canvas(self):
        self.canvas.delete("all")
        self.undo_stack.clear()

    def select_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def undo(self):
        for _ in range(10):
            if self.undo_stack:
                item = self.undo_stack.pop()
                self.canvas.delete(item)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("GIF files", "*.gif"), ("All files", "*.*")])
        if file_path:
            image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
            draw = ImageDraw.Draw(image)
            for item in self.canvas.find_all():
                x1, y1, x2, y2 = self.canvas.coords(item)
                fill_color = self.canvas.itemcget(item, "fill")
                draw.ellipse([x1, y1, x2, y2], fill=fill_color)

            if file_path.endswith(".png"):
                image.save(file_path, "PNG")
            elif file_path.endswith(".jpg"):
                image.save(file_path, "JPEG")
            elif file_path.endswith(".gif"):
                image.save(file_path, "GIF")

    def change_canvas_size(self):
        canvas_size_dialog = tk.Toplevel(self.root)
        canvas_size_dialog.title("Изменить размер холста")

        canvas_size_frame = ttk.Frame(canvas_size_dialog)
        canvas_size_frame.pack()

        width_label = ttk.Label(canvas_size_frame, text="Ширина:")
        width_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        height_label = ttk.Label(canvas_size_frame, text="Высота:")
        height_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        width_entry = ttk.Entry(canvas_size_frame)
        width_entry.grid(row=0, column=1, padx=5, pady=5)
        width_entry.insert(0, str(self.canvas_width))

        height_entry = ttk.Entry(canvas_size_frame)
        height_entry.grid(row=1, column=1, padx=5, pady=5)
        height_entry.insert(0, str(self.canvas_height))

        apply_button = ttk.Button(canvas_size_dialog, text="Применить", command=lambda: self.apply_canvas_size_dialog(width_entry, height_entry, canvas_size_dialog))
        apply_button.pack(pady=10)

    def apply_canvas_size_dialog(self, width_entry, height_entry, canvas_size_dialog):
        new_width = int(width_entry.get())
        new_height = int(height_entry.get())
        if new_width > 0 and new_height > 0:
            self.canvas.config(width=new_width, height=new_height)
            self.canvas_width = new_width
            self.canvas_height = new_height
            canvas_size_dialog.destroy()

    def show_about_dialog(self):
        messagebox.showinfo("О программе", "Филат! Поздравляю тебя с твоим 17-летием! Это замечательный момент в твоей жизни, полный возможностей и новых переживаний. Желаю тебе всегда оставаться таким же веселым, умным и творческим! И в качестве подарка, я с удовольствием представляю тебе пеинт-программу, созданную лично для тебя на языке программирования Python от Наиля. Теперь у тебя будет возможность проявить свой творческий потенциал и создавать удивительные произведения искусства. Пусть эта программа принесет тебе радость и вдохновение, а каждая кисточка будет твоим инструментом для самовыражения. С днем рождения, Филат! Пусть этот год будет полон ярких моментов и достижений!")

    def secret_message(self):
        messagebox.showinfo("Топ секрет", "Фил, ты лучший, мишка Фредд! подожди это чтоооо самонаводящиеся члены в скрап хуяник????")

if __name__ == "__main__":


    # Запускаем главное окно программы
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
