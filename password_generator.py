import tkinter as tk
from tkinter import messagebox, ttk
import random
import datetime
import pyperclip


class PasswordGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("密码生成器 v2.0")
        self.window.geometry("500x600")
        self.window.configure(bg='#f0f0f0')
        self.window.option_add('*Font', ('Microsoft YaHei', 10))

        self.setup_defaults()
        self.create_widgets()

    def setup_defaults(self):
        """初始化默认配置"""
        self.special_presets = {
            '常用符号': '!@#$%^&*',
            '安全符号': '!$%&*?@',
            '全符号': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }

    def create_widgets(self):
        """创建图形界面组件（最终调整版）"""
        # 样式配置
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('Header.TLabel',
                        font=('Microsoft YaHei', 14, 'bold'),
                        foreground='#333')
        # 新按钮样式配置
        style.configure('New.TButton',
                        foreground='white',
                        background='#0078D4',  # 深蓝色
                        padding=10,
                        font=('Microsoft YaHei', 10, 'bold'),
                        bordercolor='#005A9E',
                        lightcolor='#0078D4',
                        darkcolor='#005A9E')
        style.map('New.TButton',
                  background=[('active', '#005A9E'), ('disabled', '#A0A0A0')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        # 主容器
        main_frame = ttk.Frame(self.window)
        main_frame.pack(padx=20, pady=15, fill='both', expand=True)

        # 标题
        ttk.Label(main_frame,
                  text="密码生成器",
                  style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=15)

        # ==== 密码长度设置 ====
        length_frame = ttk.Frame(main_frame)
        length_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)

        # 长度标签和输入框
        ttk.Label(length_frame, text="密码长度:").pack(side='left', padx=(0, 5))
        self.length_var = tk.StringVar(value='12')
        self.length_entry = ttk.Entry(
            length_frame,
            textvariable=self.length_var,
            width=8,
            validate="key",
            validatecommand=(length_frame.register(self.validate_length_input), '%P')
        )
        self.length_entry.pack(side='left')

        # 输入提示标签
        self.length_tip = ttk.Label(length_frame, text="", foreground='red')
        self.length_tip.pack(side='left', padx=5)

        # 生成按钮（使用新样式）
        ttk.Button(length_frame, text="生 成", command=self.generate).pack(side='right', padx=5)

        # ==== 字符类型设置 ====
        char_group = ttk.Labelframe(main_frame,
                                    text=" 字符类型 ",
                                    padding=(15, 10))
        char_group.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)

        self.char_options = {
            'lower': tk.IntVar(value=1),
            'upper': tk.IntVar(value=1),
            'numbers': tk.IntVar(value=1),
            'special_preset': tk.IntVar(value=1)
        }

        check_buttons = [
            ('lower', "小写字母 (a-z)"),
            ('upper', "大写字母 (A-Z)"),
            ('numbers', "数字 (0-9)"),
            ('special_preset', "特殊字符"),
        ]

        for idx, (name, text) in enumerate(check_buttons):
            cb = ttk.Checkbutton(char_group,
                                 text=text,
                                 variable=self.char_options[name])
            cb.grid(row=idx // 2, column=idx % 2, sticky='w', padx=5, pady=5)

        # ==== 特殊字符设置 ====
        special_group = ttk.Labelframe(main_frame,
                                       text=" 特殊字符设置 ",
                                       padding=(15, 10))
        special_group.grid(row=3, column=0, columnspan=2, sticky='ew', pady=10)

        self.special_mode = tk.StringVar(value='preset')
        rb_frame = ttk.Frame(special_group)
        rb_frame.pack(fill='x', expand=True)

        ttk.Radiobutton(rb_frame,
                        text="使用预设:",
                        variable=self.special_mode,
                        value='preset').pack(side='left', padx=5)

        self.preset_var = tk.StringVar(value='常用符号')
        self.preset_menu = ttk.Combobox(
            rb_frame,
            textvariable=self.preset_var,
            values=list(self.special_presets.keys()),
            width=15,
            state="readonly"
        )
        self.preset_menu.pack(side='left', padx=5)

        ttk.Radiobutton(rb_frame,
                        text="自定义:",
                        variable=self.special_mode,
                        value='custom').pack(side='left', padx=10)

        self.custom_special_var = tk.StringVar()
        ttk.Entry(rb_frame,
                  textvariable=self.custom_special_var,
                  width=18).pack(side='left')

        # ==== 密码显示区 ====（缩短输入框长度至16字符）
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=15)

        ttk.Label(password_frame, text="密码：").pack(side='left')
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=('Consolas', 12),
            state='readonly',
            width=16  # 调小后的尺寸
        )
        password_entry.pack(side='left', fill='x', expand=True, padx=5)

        # 复制按钮（使用新样式）
        ttk.Button(password_frame, text="复 制", command=self.copy_password, ).pack(side='left', padx=5)

        # ==== 备注与保存 ====（缩短输入框长度至16字符）
        note_frame = ttk.Frame(main_frame)
        note_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=10)

        ttk.Label(note_frame, text="备注：").pack(side='left')
        self.note_var = tk.StringVar()
        ttk.Entry(note_frame,
                  textvariable=self.note_var,
                  width=16  # 调小后的尺寸
                  ).pack(side='left', fill='x', expand=True, padx=5)

        # 保存按钮（使用新样式）
        ttk.Button(note_frame, text="保 存", command=self.save_password).pack(side='left', padx=5)

        # 列自适应配置
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 初始化输入验证
        self.validate_length_input('12')  # 初始有效状态

    def validate_length_input(self, new_value):
        """实时验证密码长度输入"""
        max_length = 2  # 最大允许输入位数（4-50的取值范围）

        if len(new_value) > max_length:
            return False

        # 允许空输入用于删除操作
        if new_value == "":
            self.length_tip.config(text="可输入4-50", foreground='gray')
            return True

        # 仅允许数字输入
        if not new_value.isdigit():
            self.length_tip.config(text="必须为数字！", foreground='red')
            return False

        num = int(new_value)
        if 4 <= num <= 50:
            self.length_tip.config(text="✓", foreground='green')
            return True

        self.length_tip.config(text="超出范围！", foreground='red')
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
        if self.char_options['special_preset'].get():
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
        # 最终验证
        value = self.length_var.get().strip()

        if not value:
            return messagebox.showerror("错误", "密码长度不能为空")
        if not value.isdigit() or not (4 <= int(value) <= 50):
            return messagebox.showerror("错误", "无效长度（4-50）")

        # 继续生成密码逻辑
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
        if self.char_options['special_preset'].get():
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
