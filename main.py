import tkinter as tk
import openai

# 配置OpenAI API密钥
openai.api_key = "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"


# 定义一个函数，当点击按钮时调用OpenAI API
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


# 创建一个Tkinter窗口
root = tk.Tk()
root.title("AI写作软件")
root.geometry("800x600")

# 创建输入框
input_box = tk.Entry(root, width=80)
input_box.pack(pady=10)

# 创建确认按钮
confirm_button = tk.Button(root, text="生成文本", command=generate_text)
confirm_button.pack(pady=10)

# 创建输出框
output_box = tk.Text(root, wrap=tk.WORD, width=80, height=20)
output_box.pack(pady=10)

# 启动Tkinter事件循环
root.mainloop()
