import tkinter as tk
from tkinter import messagebox, ttk
import random
import datetime
import pyperclip


class PasswordGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Generator v1.0")
        self.window.geometry("500x550")

        # 先初始化默认参数
        self.setup_defaults()

        # 再创建界面组件
        self.create_widgets()

    def setup_defaults(self):
        """初始化默认配置"""
        self.special_presets = {
            '常用符号': '!@#$%^&*',
            '安全符号': '!$%&*?@',
            '全符号': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }

    def create_widgets(self):
        """创建图形界面组件"""
        # 密码长度设置
        ttk.Label(self.window, text="密码长度:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5)
        self.length_var = tk.StringVar(value='12')
        ttk.Entry(self.window, textvariable=self.length_var, width=5).grid(row=0, column=1, sticky='w')

        # 字符类型选择
        self.char_options = {
            'lower': tk.IntVar(value=1),
            'upper': tk.IntVar(value=1),
            'numbers': tk.IntVar(value=1),
            'special_preset': tk.IntVar(value=1),
            'special_custom': tk.IntVar(value=0)
        }

        # 选项复选框
        row = 1
        for name, text in [('lower', "小写字母"), ('upper', "大写字母"),
                           ('numbers', "数字"), ('special_preset', "特殊字符")]:
            ttk.Checkbutton(self.window, text=text, variable=self.char_options[name]).grid(row=row, column=0,
                                                                                           sticky='w')
            row += 1

        # 特殊字符模式选择
        self.special_mode = tk.StringVar(value='preset')
        self.special_frame = ttk.LabelFrame(self.window, text="特殊字符选项")
        self.special_frame.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky='ew')

        ttk.Radiobutton(self.special_frame, text="预设集合", variable=self.special_mode, value='preset').pack(
            side='left', padx=5)
        self.preset_var = tk.StringVar(value='常用符号')
        self.preset_menu = ttk.Combobox(self.special_frame, textvariable=self.preset_var,
                                        values=list(self.special_presets.keys()), width=12)
        self.preset_menu.pack(side='left', padx=5)

        ttk.Radiobutton(self.special_frame, text="自定义", variable=self.special_mode, value='custom').pack(side='left',
                                                                                                            padx=5)
        self.custom_special_var = tk.StringVar()
        ttk.Entry(self.special_frame, textvariable=self.custom_special_var, width=15).pack(side='left', padx=5)

        # 生成按钮
        ttk.Button(self.window, text="生成密码", command=self.generate).grid(row=5, column=0, pady=10, columnspan=2)

        # 密码显示区
        self.password_var = tk.StringVar()
        ttk.Entry(self.window, textvariable=self.password_var, width=35, font=('Arial', 12)).grid(row=6, column=0,
                                                                                                  columnspan=2)

        # 操作按钮
        button_frame = ttk.Frame(self.window)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="复制密码", command=self.copy_password).pack(side='left', padx=5)
        ttk.Button(button_frame, text="保存密码", command=self.save_password).pack(side='left', padx=5)

        # 备注区
        ttk.Label(self.window, text="备注说明:").grid(row=8, column=0, sticky='e', padx=5)
        self.note_var = tk.StringVar()
        ttk.Entry(self.window, textvariable=self.note_var, width=30).grid(row=8, column=1, sticky='w')

    def validate_input(self):
        """验证输入有效性"""
        try:
            length = int(self.length_var.get())
            if not (4 <= length <= 50):
                raise ValueError
            return True
        except ValueError:
            messagebox.showerror("错误", "密码长度应为4到50之间的整数")
            return False

    def build_character_set(self):
        """构建字符池"""
        char_pool = []

        if self.char_options['lower'].get():
            char_pool += list('abcdefghijklmnopqrstuvwxyz')
        if self.char_options['upper'].get():
            char_pool += list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if self.char_options['numbers'].get():
            char_pool += list('0123456789')

        # 处理特殊字符
        if self.char_options['special_preset'].get() or self.char_options['special_custom'].get():
            if self.special_mode.get() == 'preset':
                special_chars = self.special_presets.get(self.preset_var.get(), '')
            else:
                special_chars = self.custom_special_var.get().strip()

            if special_chars:
                char_pool += list(special_chars)

        if not char_pool:
            messagebox.showerror("错误", "至少需要选择一种字符类型")
            return None
        return char_pool

    def generate(self):
        """生成密码核心逻辑"""
        if not self.validate_input():
            return

        char_pool = self.build_character_set()
        if not char_pool:
            return

        length = int(self.length_var.get())
        password = []

        # 确保至少包含一个已选字符类型
        if self.char_options['lower'].get():
            password.append(random.choice('abcdefghijklmnopqrstuvwxyz'))
        if self.char_options['upper'].get():
            password.append(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        if self.char_options['numbers'].get():
            password.append(random.choice('0123456789'))
        if self.char_options['special_preset'].get() or self.char_options['special_custom'].get():
            special_source = self.special_presets[
                self.preset_var.get()] if self.special_mode.get() == 'preset' else self.custom_special_var.get()
            password.append(random.choice(special_source.strip()))

        # 补充剩余字符
        remaining = length - len(password)
        password += random.choices(char_pool, k=remaining)
        random.shuffle(password)  # 打乱顺序

        self.password_var.set(''.join(password))

    def copy_password(self):
        """复制密码到剪贴板"""
        if not self.password_var.get():
            messagebox.showwarning("警告", "请先生成密码")
            return
        pyperclip.copy(self.password_var.get())
        messagebox.showinfo("成功", "密码已复制到剪贴板")

    def save_password(self):
        """保存密码记录"""
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("警告", "没有可保存的密码")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = self.note_var.get().strip()
        record = f"""
[{timestamp}]
备注: {note if note else '无'}
密码: {password}
{'-' * 40}"""

        try:
            with open('passwords.txt', 'a', encoding='utf-8') as f:
                f.write(record)
            messagebox.showinfo("成功", "密码保存成功")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")


if __name__ == "__main__":
    app = PasswordGenerator()
    app.window.mainloop()
