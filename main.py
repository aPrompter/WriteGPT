import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkinter import filedialog, messagebox
import openai
import json
from docx import Document
import os

API_KEY_FILE = 'api_key.txt'


def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            return f.read().strip()
    return ''


def save_api_key():
    with open(API_KEY_FILE, 'w') as f:
        f.write(api_key_entry.get())
    openai.api_key = api_key_entry.get()
    messagebox.showinfo("成功", "API密钥已保存。")


# 在程序启动时，尝试从一个文件中读取保存的API密钥
openai.api_key = load_api_key()


def load_templates():
    try:
        with open('templates.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_templates():
    with open('templates.json', 'w') as f:
        json.dump(templates, f)


def choose_template():
    if templates:
        template_types = list(templates.keys())
        selected_type = tk.StringVar(root)
        selected_type.set(template_types[0])

        def apply_template():
            template = templates[selected_type.get()]
            input_box.delete(0, tk.END)
            input_box.insert(0, template)
            template_dialog.destroy()

        template_dialog = tk.Toplevel(root)
        template_dialog.title("选择模板")

        tk.Label(template_dialog, text="选择模板：").pack(pady=5)
        tk.OptionMenu(template_dialog, selected_type, *template_types).pack(pady=5)
        tk.Button(template_dialog, text="应用模板", command=apply_template).pack(pady=5)
    else:
        messagebox.showerror("错误", "没有模板可供选择，请先导入模板。")


def import_template():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as f:
            new_templates = json.load(f)
        templates.update(new_templates)
        save_templates()
        messagebox.showinfo("成功", "模板已成功导入。")


def export_template():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as f:
            json.dump(templates, f)
        messagebox.showinfo("成功", "模板已成功导出。")


templates = load_templates()


def generate_text():
    prompt = input_box.get()
    if prompt.strip() != "":
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=4000 - len(prompt.encode('utf-8')),
                n=1,
                stop=None,
                temperature=0.7,
            )
            output_text = response.choices[0].text
            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, output_text)
        except Exception as e:
            messagebox.showerror("错误", f"无法调用OpenAI API：{str(e)}")


def edit_text(event):
    ctrl_pressed = event.state & 0x4  # 检查Ctrl键是否按下
    if ctrl_pressed and event.keysym == 'q':  # 检查是否按下了Ctrl + Q
        selected_text = output_box.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            suggestion = askstring("修改建议", "请输入修改意见：")
            if suggestion:
                prompt = f"原文本：'{selected_text}'\n修改意见：'{suggestion}'\n根据修改意见，生成一个新的文本片段："
                try:
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=4000 - len(prompt.encode('utf-8')),
                        n=1,
                        stop=None,
                        temperature=0.7,
                    )
                    new_text = response.choices[0].text
                    if tk.messagebox.askyesno("替换确认", f"原文本：{selected_text}\n新文本：{new_text}\n是否替换？"):
                        output_box.delete(tk.SEL_FIRST, tk.SEL_LAST)
                        output_box.insert(tk.INSERT, new_text)
                except Exception as e:
                    messagebox.showerror("错误", f"无法调用OpenAI API：{str(e)}")


def export_to_word():
    file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                             filetypes=[("Word Document", "*.docx"), ("All Files", "*.*")])
    if file_path:
        content = output_box.get(1.0, tk.END).strip()
        if content:
            doc = Document()
            doc.add_paragraph(content)
            doc.save(file_path)
            messagebox.showinfo("导出成功", f"文件已成功导出到：{file_path}")
        else:
            messagebox.showerror("导出失败", "输出框为空，无法导出")


root = tk.Tk()
root.title("AI写作软件")
root.geometry("800x600")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# 创建API密钥输入框和保存按钮
api_key_frame = ttk.Frame(main_frame)
api_key_frame.pack(pady=5)

ttk.Label(api_key_frame, text="API密钥：").pack(side=tk.LEFT, padx=5)
api_key_entry = ttk.Entry(api_key_frame, width=40)
api_key_entry.pack(side=tk.LEFT, padx=5)
api_key_entry.insert(0, openai.api_key)

save_api_key_button = ttk.Button(api_key_frame, text="确认API密钥", command=save_api_key)
save_api_key_button.pack(side=tk.LEFT, padx=5)

template_buttons = ttk.Frame(main_frame)
template_buttons.pack(pady=5)

choose_template_button = ttk.Button(template_buttons, text="选择模板", command=choose_template)
choose_template_button.pack(side=tk.LEFT, padx=5)

import_template_button = ttk.Button(template_buttons, text="导入模板", command=import_template)
import_template_button.pack(side=tk.LEFT, padx=5)

export_template_button = ttk.Button(template_buttons, text="导出模板", command=export_template)
export_template_button.pack(side=tk.LEFT, padx=5)

input_box = ttk.Entry(main_frame, width=80)
input_box.pack(pady=10)

confirm_button = ttk.Button(main_frame, text="生成文本", command=generate_text)
confirm_button.pack(pady=10)

output_box = tk.Text(main_frame, wrap=tk.WORD, width=80, height=20)
output_box.pack(pady=10, expand=True, fill=tk.BOTH)
output_box.bind('<Control-Key>', edit_text)

export_button = ttk.Button(main_frame, text="导出文件", command=export_to_word)
export_button.pack(pady=10)

root.mainloop()
