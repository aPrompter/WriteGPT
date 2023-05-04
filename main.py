import tkinter as tk
from tkinter.simpledialog import askstring
import tkinter.messagebox
import openai

openai.api_key = "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"


def generate_text():
    prompt = input_box.get()
    if prompt.strip() != "":
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        output_text = response.choices[0].text
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, output_text)


def edit_text(event):
    ctrl_pressed = event.state & 0x4  # 检查Ctrl键是否按下
    if ctrl_pressed and event.keysym == 'q':  # 检查是否按下了Ctrl + Q
        selected_text = output_box.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            suggestion = askstring("修改建议", "请输入修改意见：")
            if suggestion:
                prompt = f"{selected_text} -> {suggestion}"
                print(f"{selected_text} -> {suggestion}")
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=4000 - len(prompt),
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                new_text = response.choices[0].text
                if tk.messagebox.askyesno("替换确认", f"原文本：{selected_text}\n新文本：{new_text}\n是否替换？"):
                    output_box.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    output_box.insert(tk.INSERT, new_text)


root = tk.Tk()
root.title("AI写作软件")
root.geometry("800x600")

input_box = tk.Entry(root, width=80)
input_box.pack(pady=10)

confirm_button = tk.Button(root, text="生成文本", command=generate_text)
confirm_button.pack(pady=10)

output_box = tk.Text(root, wrap=tk.WORD, width=80, height=20)
output_box.pack(pady=10)
output_box.bind('<Control-Key>', edit_text)

root.mainloop()
