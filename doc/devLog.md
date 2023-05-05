# 开发记录

## 前提条件

- 安装python3运行环境
- 安装开发工具PyCharm
- 能正常使用chatGPT

## 项目简介

writeMore是一款智能写作软件。使用OpenAI提供的api，作为底层的文本生成能力。优化写作场景的使用体验。

项目旨在解决chatGPT生成文章的诸多痛点。

- 文本生成的提示词（prompt）很难构建和复用
- chatGPT的交互体验，不适合写作场景（无法手动修改，难以重写）
- 无法调整模型参数

项目全程使用GPT生成代码，之后由人工测试和调整。以测试GPT编写代码的可能性。

## 项目创建

使用PyCharm新建项目

![新建项目](./img/createProject1.png)

设置项目目录和开发环境

![项目目录与开发环境](./img/createProject2.png)

创建完成并测试环境是否正常

![创建完成](./img/createProject3.png)

## 使用GPT开发

### 实现基础文本生成功能

> prompt:
>
> 现在，你是一位资深的软件开发工程师，而我是一位产品经理。我会给你提出产品需求，你帮我使用python代码实现。 
>
> 我的第一个需求是： 
>
> 使用python开发一个桌面应用程序。该程序是一款AI写作软件，基于OpenAI提供的api能力，做到输入框输入提示词，点击确认按钮后，后台调用api获取ai生成的文本，然后在另一个文本框输出。 要求使用OpenAI公司提供的python库openai。

> GPT:
>
> 为了实现这个需求，我们可以使用`Tkinter`库创建一个简单的桌面应用程序，结合`openai`库调用OpenAI的API。首先，请确保你已经安装了`openai`库，使用以下命令安装：
>
> ``` shell
> pip install openai
> ```
>
> 接下来，我们将创建一个简单的桌面应用程序，包含一个输入框、一个按钮和一个输出框：
>
> ``` python
> import tkinter as tk
> import openai
> 
> # 配置OpenAI API密钥
> openai.api_key = "your_api_key"
> 
> # 定义一个函数，当点击按钮时调用OpenAI API
> def generate_text():
>     prompt = input_box.get()
>     if prompt.strip() != "":
>         response = openai.Completion.create(
>             engine="davinci-codex",
>             prompt=prompt,
>             max_tokens=100,
>             n=1,
>             stop=None,
>             temperature=0.5,
>         )
>         output_text = response.choices[0].text
>         output_box.delete(1.0, tk.END)
>         output_box.insert(tk.END, output_text)
> 
> # 创建一个Tkinter窗口
> root = tk.Tk()
> root.title("AI写作软件")
> root.geometry("800x600")
> 
> # 创建输入框
> input_box = tk.Entry(root, width=80)
> input_box.pack(pady=10)
> 
> # 创建确认按钮
> confirm_button = tk.Button(root, text="生成文本", command=generate_text)
> confirm_button.pack(pady=10)
> 
> # 创建输出框
> output_box = tk.Text(root, wrap=tk.WORD, width=80, height=20)
> output_box.pack(pady=10)
> 
> # 启动Tkinter事件循环
> root.mainloop()
> 
> ```
>
> 在这段代码中，我们定义了一个`generate_text`函数，该函数从输入框获取提示词并调用OpenAI API生成文本。然后，这个函数将生成的文本插入到输出框中。
>
> 请注意，您需要将`your_api_key`替换为您的实际OpenAI API密钥。此外，您可能需要根据实际情况调整API调用参数，例如引擎、最大令牌数等。
>
> 这个简单的桌面应用程序应该满足您的需求。如果您需要进一步自定义，请随时在此基础上进行修改。

GPT给出的代码中，需要我们手动设置API key

我们可以到[OpenAI官网](https://platform.openai.com/account/api-keys)申请一个key。

将openai.api_key = "your_api_key"的your_api_key替换为自己的api key后，我们尝试执行一下。

初次运行使用，在调用Open AI的接口时失败了

![error1](./img/error1.png)

我们将报错信息交给GPT处理一下

> GPT:
> 抱歉给您带来了困扰。看起来问题出在使用的模型名称“davinci-codex”上。请使用有效的模型名称，例如 "text-davinci-002"。请将代码中的以下部分：
>
> ``` python
> response = openai.Completion.create(
>     engine="davinci-codex",
>     prompt=prompt,
>     max_tokens=100,
>     n=1,
>     stop=None,
>     temperature=0.5,
> )
> ```
>
> 替换为：
>
> ``` python
> response = openai.Completion.create(
>     engine="text-davinci-002",
>     prompt=prompt,
>     max_tokens=100,
>     n=1,
>     stop=None,
>     temperature=0.5,
> )
> ```
>
> 更新模型名称后，程序应该可以正常运行。如果您遇到其他问题，请随时告诉我。

GPT指出是模型的名称问题。我们可以根据自己的需要选择具体的模型，模型清单可以访问[官网地址](https://platform.openai.com/docs/models/gpt-3-5)。

在本项目中，我们选择更强大的文本模型`text-davinci-003`。

接下来试试效果

我们使用提示词“写一篇科普文，主题是AI发展历史”作为测试用例

![第一次成功](./img/firstSuccess.png)

基础的功能已经实现了，但给出的文本内容很少。我们再要求GPT帮我们优化下

> prompt:
> 现在可以正常运行了，但是模型给出的文本内容很少，不是一篇完整的文章，请帮我继续优化，让文章能完整的输出

> GPT:
>
> 我明白您的需求。为了生成更长的文本，我们可以增加`max_tokens`参数的值，同时，我们可以通过调整`temperature`参数来影响生成文本的随机性。数值越小，输出结果越确定性，数值越大，结果越随机。此外，为了确保文章结构的完整性，我们可以在`stop`参数中设置一个终止符，例如句号或者换行符。以下是修改后的`generate_text`函数：
>
> ``` python
> def generate_text():
>     prompt = input_box.get()
>     if prompt.strip() != "":
>         response = openai.Completion.create(
>             engine="text-davinci-002",
>             prompt=prompt,
>             max_tokens=500,  # 增加最大令牌数
>             n=1,
>             stop=["\n"],  # 设置终止符
>             temperature=0.7,  # 调整temperature参数
>         )
>         output_text = response.choices[0].text
>         output_box.delete(1.0, tk.END)
>         output_box.insert(tk.END, output_text)
> ```
>
> 在此示例中，我们将`max_tokens`参数设置为500，这将允许模型生成更长的文本。同时，我们将`temperature`参数调整为0.7，以获得一个适度的随机性。最后，我们将终止符设置为换行符，以确保生成的文章更具完整性。
>
> 请注意，生成更长文本可能会增加API调用的时间。此外，如果您发现生成的文本仍然不够长或太长，可以继续调整`max_tokens`参数。如果您需要进一步优化，请随时告诉我。

GPT告诉我们，可以通过调整max_tokens参数，增加内容输出长度。

我们可以在官网查到，最大的tokens，可以是4096。在这里，我们就不用GPT推荐的500，而直接用4000。

![modelTokenMax](./img/modelTokenMax.png)

修改后的结果是：

![第二次成功](./img/secondSuccess.png)

这样基础的文本生成功能就完成了。

### 添加文章修改功能

> Prompt:
>
> 下一个需求是让模型给出的文本可以被修改。
>
>  修改的部分是，用鼠标选中的内容。选中之后，按ctrl+q后，出现一个悬浮框，悬浮框内输入修改意见。点击确认后，将鼠标选中的内容与悬浮框输入的建议，一并通过api传给模型。 
>
> 模型给出结果后，替换鼠标选中的内容。但在替换之前，需要用户确认是否替换。

> GPT:
>
> 为了实现这个需求，我们需要对现有的程序进行一些修改和扩展。首先，我们需要创建一个悬浮框窗口用于输入修改意见。其次，我们需要在输出框的文本被选中并按下Ctrl+K时触发悬浮框。最后，我们需要将选中的内容和修改意见一起传递给模型，并在用户确认后替换选中的内容。
>
> 以下是实现这个功能的代码：
>
> ``` python
> import tkinter as tk
> from tkinter.simpledialog import askstring
> import openai
> 
> openai.api_key = "your_api_key"
> 
> def generate_text():
>     prompt = input_box.get()
>     if prompt.strip() != "":
>         response = openai.Completion.create(
>             engine="text-davinci-002",
>             prompt=prompt,
>             max_tokens=500,
>             n=1,
>             stop=["\n"],
>             temperature=0.7,
>         )
>         output_text = response.choices[0].text
>         output_box.delete(1.0, tk.END)
>         output_box.insert(tk.END, output_text)
> 
> def edit_text(event):
>     if event.state == 4 and event.keysym == 'q':  # 检查是否按下了Ctrl + Q
>         selected_text = output_box.get(tk.SEL_FIRST, tk.SEL_LAST)
>         if selected_text:
>             suggestion = askstring("修改建议", "请输入修改意见：")
>             if suggestion:
>                 prompt = f"{selected_text} -> {suggestion}"
>                 response = openai.Completion.create(
>                     engine="text-davinci-002",
>                     prompt=prompt,
>                     max_tokens=100,
>                     n=1,
>                     stop=None,
>                     temperature=0.7,
>                 )
>                 new_text = response.choices[0].text
>                 if tk.messagebox.askyesno("替换确认", f"原文本：{selected_text}\n新文本：{new_text}\n是否替换？"):
>                     output_box.delete(tk.SEL_FIRST, tk.SEL_LAST)
>                     output_box.insert(tk.INSERT, new_text)
> 
> root = tk.Tk()
> root.title("AI写作软件")
> root.geometry("800x600")
> 
> input_box = tk.Entry(root, width=80)
> input_box.pack(pady=10)
> 
> confirm_button = tk.Button(root, text="生成文本", command=generate_text)
> confirm_button.pack(pady=10)
> 
> output_box = tk.Text(root, wrap=tk.WORD, width=80, height=20)
> output_box.pack(pady=10)
> output_box.bind('<Control-Key>', edit_text)
> 
> root.mainloop()
> 
> ```
>
> 现在，当您在输出框中选中文本并按下Ctrl+K时，将弹出一个悬浮框让您输入修改意见。模型会结合选中的文本和修改意见生成新的文本。在替换选中的内容之前，程序会询问用户是否确认替换。
>
> 请注意，为了使此代码正常工作，您需要确保您的OpenAI API密钥已

代码复制到pycharm中，出现一个问题，ide提示Cannot find reference 'messagebox' in '__init__.pyi' 

![这是问题](./img/ideWrong.png)

把问题交给GPT

> Prompt: Cannot find reference 'messagebox' in '__init__.pyi' 

> GPT:抱歉，我的失误。我们需要在代码中导入`tkinter.messagebox`。请在代码的开头添加以下导入语句：
>
> ```python
> import tkinter.messagebox
> ```
>
> 现在，程序应该可以正常运行，并且在替换选中的内容之前会弹出确认框。如果您遇到其他问题，请随时告诉我。

开始测试代码：

选中文本之后按ctrl+q，没有任何反应。

这个时候，我们需要确认一下event.state是否正确

![检查state](./img/checkState.png)

可以看到state是12与GPT给出的4不一致。让GPT解决一下这个问题

> prmpt:使用debug模式，查看按下ctrl+q的event.state，结果是state=12，而不是代码中的4。如何处理

> GPT:
>
> 抱歉给您带来了困扰。`event.state`的值可能因平台和系统而异。在这种情况下，我们可以使用另一种方法来检测Ctrl键是否被按下。我们可以使用`event.keysym`属性检查按键符号，并结合`event.state & 0x4`来检查Ctrl键的状态。以下是修改后的`edit_text`函数定义部分：
>
> ```python
> def edit_text(event):
>     ctrl_pressed = event.state & 0x4  # 检查Ctrl键是否按下
>     if ctrl_pressed and event.keysym == 'q':  # 检查是否按下了Ctrl + Q
>         # ...函数的其余部分保持不变
> ```
>
> 这个修改应该解决了您的问题。现在，按下Ctrl + Q时，`edit_text`函数应该能够正确触发。如果您遇到其他问题，请随时告诉我。

解决了这个问题后，我们再来测试一下。
![修改文章1](./img/fixArticle1.png)

图中选中的是第一段文字，点击ok后，报错了

![bug](./img/fixArticleBug.png)

将报错信息给GPT后，得到的回答是，token长度超过限制。

> GPT:
> 抱歉给您带来了困扰。这个错误是因为模型的最大上下文长度限制为4097个令牌，而您的请求超过了这个限制。为了解决这个问题，您可以尝试减少`max_tokens`的值，以保持在模型的上下文长度限制范围内。
>
> 以下是更新后的代码，其中`max_tokens`值已更改为3000。您可以根据需要调整此值，但请确保保持在模型的最大上下文长度限制内：(代码只是将max_tokens改为3000，此处就省略代码)
>
> 这个修改应该解决了您的问题。如果您还有其他问题，请随时告诉我。

这里我们再优化一下，改为动态调整预设的tokens

``` python
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=4000 - len(prompt),
    n=1,
    stop=None,
    temperature=0.7,
)
```

设置完成后，再次测试

![第二次测试修改文章](./img/fixArticle2.png)

![文章修改结果](./img/articleFixResult.png)

![文章修改结果](./img/articleFixResult2.png)

可以看到，文本已经实现了使用GPT修改内容的功能了。

### 添加模板生成文章

> prompt: 现在，你是一位资深的软件开发工程师，而我是一位产品经理。
>
> 我会给你提出产品需求，你帮我使用python代码实现。 
>
> 在上述的代码中添加新的需求 新需求是为了解决，每次写文章都需要重新构建prompt的问题 我希望可以将prompt复用，每次只需要填写可替换的关键信息就行了。
>
>  prompt的复用，通过导入模板实现，模板文件是json文件。
>
> 模板格式： { “type1":"value1", "type2":"value2" } 
>
> 现在我需要你做的事情是。 添加选择模板，导入模板，导出模板三个功能的按钮，平行放在输入框上方。 
>
> 点击按钮后，弹出一个悬浮框。 
>
> 选择模板点击后，悬浮框内有一个下拉框，下拉框选中了文章类型后，将对应的模板value放入输入框中。 
>
> 导入模板按钮点击后，导入.json文件并解析。
>
> 要求在下一次打开应用，还能通过选择模板使用
>
>  导出模板按钮点击后，导出.json文件 当应用第一次使用的时候，是没有模板的。
>
> 选择模板按钮点击后，提示用户没有模板。

> GPT:
>
> 根据您的需求，我已经更新了代码以支持模板功能。现在有三个新按钮：选择模板，导入模板和导出模板。您可以使用这些按钮来处理模板。以下是完整的代码：
>
> ```python
> import tkinter as tk
> from tkinter import filedialog, messagebox
> import openai
> import json
> 
> openai.api_key = "your_api_key"
> 
> templates = {}
> 
> def load_templates():
>     try:
>         with open('templates.json', 'r') as f:
>             return json.load(f)
>     except FileNotFoundError:
>         return {}
> 
> def save_templates():
>     with open('templates.json', 'w') as f:
>         json.dump(templates, f)
> 
> def choose_template():
>     if templates:
>         template_types = list(templates.keys())
>         selected_type = tk.StringVar(root)
>         selected_type.set(template_types[0])
> 
>         def apply_template():
>             template = templates[selected_type.get()]
>             input_box.delete(0, tk.END)
>             input_box.insert(0, template)
>             template_dialog.destroy()
> 
>         template_dialog = tk.Toplevel(root)
>         template_dialog.title("选择模板")
> 
>         tk.Label(template_dialog, text="选择模板：").pack(pady=5)
>         tk.OptionMenu(template_dialog, selected_type, *template_types).pack(pady=5)
>         tk.Button(template_dialog, text="应用模板", command=apply_template).pack(pady=5)
>     else:
>         messagebox.showerror("错误", "没有模板可供选择，请先导入模板。")
> 
> def import_template():
>     file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
>     if file_path:
>         with open(file_path, 'r') as f:
>             new_templates = json.load(f)
>         templates.update(new_templates)
>         save_templates()
>         messagebox.showinfo("成功", "模板已成功导入。")
> 
> def export_template():
>     file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
>     if file_path:
>         with open(file_path, 'w') as f:
>             json.dump(templates, f)
>         messagebox.showinfo("成功", "模板已成功导出。")
> 
> templates = load_templates()
> 
> root = tk.Tk()
> root.title("AI写作软件")
> root.geometry("800x600")
> 
> template_buttons = tk.Frame(root)
> template_buttons.pack(pady=5)
> 
> choose_template_button = tk.Button(template_buttons, text="选择模板", command=choose_template)
> choose_template_button.pack(side=tk.LEFT, padx=5)
> 
> import_template_button = tk.Button(template_buttons, text="导入模板", command=import_template)
> import_template_button.pack(side=tk.LEFT, padx=5)
> 
> export_template_button = tk.Button(template_buttons, text="导出模板", command=export_template)
> export_template_button.pack(side=tk.LEFT, padx=5)
> 
> input_box = tk.Entry(root, width=80)
> input_box.pack(pady=10)
> 
> confirm_button = tk.Button(root, text="生成文本", command=generate_text)
> confirm_button.pack(pady=10)
> 
> output_box = tk.Text(root, wrap=tk.WORD, width=80, height=20)
> output_box.pack(pady=10)
> output_box.bind('<Control-Key>', edit_text)
> 
> root.mainloop()
> ```
>
> 这个代码应该符合您的需求。请注意，您需要确保在运行该程序的文件夹中有一个名为`templates.json`的文件，用于存储导入的模板。如果您在打开应用程序时

在给出的代码中，没有加上之前的功能。我们需要对代码进行一个拼接。

最终的代码是：
``` python
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import filedialog, messagebox
import openai
import json

openai.api_key = "your_api_key"


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

template_buttons = tk.Frame(root)
template_buttons.pack(pady=5)

choose_template_button = tk.Button(template_buttons, text="选择模板", command=choose_template)
choose_template_button.pack(side=tk.LEFT, padx=5)

import_template_button = tk.Button(template_buttons, text="导入模板", command=import_template)
import_template_button.pack(side=tk.LEFT, padx=5)

export_template_button = tk.Button(template_buttons, text="导出模板", command=export_template)
export_template_button.pack(side=tk.LEFT, padx=5)

input_box = tk.Entry(root, width=80)
input_box.pack(pady=10)

confirm_button = tk.Button(root, text="生成文本", command=generate_text)
confirm_button.pack(pady=10)

output_box = tk.Text(root, wrap=tk.WORD, width=80, height=20)
output_box.pack(pady=10)
output_box.bind('<Control-Key>', edit_text)

root.mainloop()

```

首先我们设置一个模板文件a.json，内容如下：
``` json
{
    "读后感":"请写一篇读后感，书名是{书名}，作者是{作者}，字数要求{字数}"
}
```

之后运行程序

**先导入模板**

![加载模板](./img/loadJsonFile.png)

**选择模板**

![选择模板](./img/chooseTemplate.png)

![选择模板结果](.\img\chooseTempalteResult.png)

替换输入框中大括号包括的词。

![替换词语](./img/templateResult.png)

可以看到，模板功能完成了



### 文本导出功能

接下来，我们开发文本导出功能。

所以导出的文件格式设置为word

> promt:我的下一个需求是，让GPT生成的内容，从输出框导出。 导出的文件格式为word。导出路径和文件名称需要让用户选择 导出按钮设置在输出框之后

> GPT:为了实现这个需求，我们需要安装一个库：python-docx。您可以使用下面的命令来安装：
>
> ```shell
> pip install python-docx
> ```
>
> 然后在代码中，我们将使用`tkinter.filedialog`库来让用户选择文件路径和名称。以下是修改后的代码：
>
> ```python
> import tkinter as tk
> from tkinter.simpledialog import askstring
> import tkinter.messagebox
> import tkinter.filedialog
> import openai
> from docx import Document
> 
> openai.api_key = "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"
> 
> 
> def generate_text():
>     prompt = input_box.get()
>     if prompt.strip() != "":
>         response = openai.Completion.create(
>             engine="text-davinci-003",
>             prompt=prompt,
>             max_tokens=4000,
>             n=1,
>             stop=None,
>             temperature=0.7,
>         )
>         output_text = response.choices[0].text
>         output_box.delete(1.0, tk.END)
>         output_box.insert(tk.END, output_text)
> 
> 
> def edit_text(event):
>     # ... 省略edit_text函数的其他代码 ...
> 
> 
> def export_to_word():
>     file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".docx",
>                                                       filetypes=[("Word Document", "*.docx"), ("All Files", "*.*")])
>     if file_path:
>         content = output_box.get(1.0, tk.END).strip()
>         if content:
>             doc = Document()
>             doc.add_paragraph(content)
>             doc.save(file_path)
>             tkinter.messagebox.showinfo("导出成功", f"文件已成功导出到：{file_path}")
>         else:
>             tkinter.messagebox.showerror("导出失败", "输出框为空，无法导出")
> 
> 
> root = tk.Tk()
> root.title("AI写作软件")
> root.geometry("800x600")
> 
> input_box = tk.Entry(root, width=80)
> input_box.pack(pady=10)
> 
> confirm_button = tk.Button(root, text="生成文本", command=generate_text)
> confirm_button.pack(pady=10)
> 
> output_box = tk.Text(root, wrap=tk.WORD, width=80, height=20)
> output_box.pack(pady=10)
> output_box.bind('<Control-Key>', edit_text)
> 
> export_button = tk.Button(root, text="导出到Word", command=export_to_word)
> export_button.pack(pady=10)
> 
> root.mainloop()
> ```
>
> 在这个修改后的代码中，我们添加了一个名为`export_to_word`的函数，它会执行以下操作：
>
> 1. 使用`tkinter.filedialog.asksaveasfilename`函数弹出一个对话框让用户选择导出文件的路径和名称。
> 2. 判断输出框中是否有内容，如果没有内容则弹出一个错误提示。
> 3. 如果有内容，创建一个新的Word文档（使用python-docx库的Document类）。
> 4. 将输出框中的内容添加到Word文档中。
> 5. 保存Word文档到用户选择的路径。
> 6. 弹出一个提示框告知用户文件已成功导出。
>
> 最后，我们在输出框下方添加了一个名为"导出到Word"的按钮，单击该按钮将调用`export_to_word`函数。

GPT这次给的代码，需要调整一下。

![导出文章代码问题](./img/exportFileError.png)

在export_to_word函数中，将tkinter去除。



接下来我们来测试一下：

![导出文章](.\img\exprotFile.png)

![word文件](./img/wordFile.png)

可以看到，文件已经可以成功导出了。

### 优化编辑能容的prompt

现阶段有一个问题。

使用ctrl+q实现的让模型再次修改内容，结果往往不行

现在要求GPT优化prompt。

> prompt:接下来的需求是，优化编辑文章时，通过api传输给GPT的prompt。 现在的prompt是：                prompt = f"{selected_text} -> {suggestion}" 模型给出的结果，往往不符合要求。 请给我一个更好的prompt，让模型根据suggestion，修改selected_text的内容。

> GPT:
> 为了让模型更好地理解任务，我们可以使用更明确的指示来构建prompt。这里是一个改进的prompt：
>
> ```python
> prompt = f"原文本：'{selected_text}'\n修改意见：'{suggestion}'\n根据修改意见，生成一个新的文本片段："
> ```
>
> 这个新的prompt首先给出原文本，然后给出修改意见，最后明确指示模型根据修改意见生成一个新的文本片段。这样的表述更有利于模型理解任务，从而生成更符合要求的结果。将这个新的prompt替换到原来的`edit_text`函数中即可。
>
> 以下是修改后的`edit_text`函数：
>
> ```python
> def edit_text(event):
>     ctrl_pressed = event.state & 0x4  # 检查Ctrl键是否按下
>     if ctrl_pressed and event.keysym == 'q':  # 检查是否按下了Ctrl + Q
>         selected_text = output_box.get(tk.SEL_FIRST, tk.SEL_LAST)
>         if selected_text:
>             suggestion = askstring("修改建议", "请输入修改意见：")
>             if suggestion:
>                 prompt = f"原文本：'{selected_text}'\n修改意见：'{suggestion}'\n根据修改意见，生成一个新的文本片段："
>                 print(f"{selected_text} -> {suggestion}")
>                 response = openai.Completion.create(
>                     engine="text-davinci-003",
>                     prompt=prompt,
>                     max_tokens=4000 - len(prompt),
>                     n=1,
>                     stop=None,
>                     temperature=0.7,
>                 )
>                 new_text = response.choices[0].text
>                 if tk.messagebox.askyesno("替换确认", f"原文本：{selected_text}\n新文本：{new_text}\n是否替换？"):
>                     output_box.delete(tk.SEL_FIRST, tk.SEL_LAST)
>                     output_box.insert(tk.INSERT, new_text)
> ```
>
> 通过这个优化，应该能够帮助模型更好地理解编辑任务，从而生成更符合要求的结果。

把代码替换后，我们继续测试。

![tokenLenError](./img/tokenLenError.png)

结果由出现错误了。

之前设置的，max_tokens=4000 - len(prompt)，还是不能把token限制在4097.

> prompt:python中，有一个字符串变量。如何获取所占字节数量

> GPT:要获取一个Python字符串变量所占的字节数量，可以使用Python内置函数 `len()` 和字符串对象的 `encode()` 方法。具体步骤如下：
>
> 1. 使用 `encode()` 方法将字符串转换为指定编码的字节序列，可以使用常见的编码方式如UTF-8或GBK等。
> 2. 使用 `len()` 函数获取字节序列的长度，即为字符串变量所占的字节数量。
>
> 下面是一个示例代码，假设要获取字符串变量 `my_string` 在UTF-8编码下所占的字节数量：
>
> ```python
> my_string = "这是一个字符串"
> 
> # 将字符串转换为UTF-8编码的字节序列
> my_bytes = my_string.encode('utf-8')
> 
> # 获取字节序列的长度，即为字符串变量所占的字节数量
> byte_count = len(my_bytes)
> 
> # 输出结果
> print(f"String '{my_string}' occupies {byte_count} bytes in UTF-8 encoding.")
> ```
>
> 上述代码将输出以下结果：
>
> ```
> String '这是一个字符串' occupies 21 bytes in UTF-8 encoding.
> ```
>
> 需要注意的是，不同的编码方式下，同一字符串变量所占的字节数量可能会不同。因此，在使用 `encode()` 方法时需要指定正确的编码方式，以确保得到正确的字节数量。

GPT给出的方案是，使用encode方法将字符串转换为指定编码的字节序列。然后再计算字节序列的长度。

按照它的指示，我们将计算方法改为：

max_tokens=4000 - len(prompt.encode('utf-8'))



接下来我们继续测试。

![测试新prompt修改文章](.\img\testModifyArticle.png)

![测试新prompt修改文章的结果](.\img\testModifyArticleResult.png)

我们与之前prompt生成的修改结果对比：
![之前文章修改结果](./img/articleFixResult.png)

可以发现修改后的文本，更加符合我们的需求了。



### 优化布局

现在的布局还是很难看。我们要求GPT帮忙优化一下布局

> prompt: 
>
> ``` pyt
> # 之前的源代码，这里省略
> ```
>
> 优化代码，让桌面程序的布局更加合理。

>GPT:
>
>您可以通过调整控件的尺寸、间距以及使用ttk主题库以提高应用程序的外观。这是一个优化后的代码示例：
>
>```python
>import tkinter as tk
>from tkinter import ttk
>from tkinter.simpledialog import askstring
>from tkinter import filedialog, messagebox
>import openai
>import json
>from docx import Document
>
>openai.api_key = "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"
>
>def load_templates():
>    # ...
>    pass
>
>def save_templates():
>    # ...
>    pass
>
>def choose_template():
>    # ...
>    pass
>
>def import_template():
>    # ...
>    pass
>
>def export_template():
>    # ...
>    pass
>
>templates = load_templates()
>
>def generate_text():
>    # ...
>    pass
>
>def edit_text(event):
>    # ...
>    pass
>
>def export_to_word():
>    # ...
>    pass
>
>root = tk.Tk()
>root.title("AI写作软件")
>root.geometry("800x600")
>
>main_frame = ttk.Frame(root, padding="10")
>main_frame.pack(fill=tk.BOTH, expand=True)
>
>template_buttons = ttk.Frame(main_frame)
>template_buttons.pack(pady=5)
>
>choose_template_button = ttk.Button(template_buttons, text="选择模板", command=choose_template)
>choose_template_button.pack(side=tk.LEFT, padx=5)
>
>import_template_button = ttk.Button(template_buttons, text="导入模板", command=import_template)
>import_template_button.pack(side=tk.LEFT, padx=5)
>
>export_template_button = ttk.Button(template_buttons, text="导出模板", command=export_template)
>export_template_button.pack(side=tk.LEFT, padx=5)
>
>input_box = ttk.Entry(main_frame, width=80)
>input_box.pack(pady=10)
>
>confirm_button = ttk.Button(main_frame, text="生成文本", command=generate_text)
>confirm_button.pack(pady=10)
>
>output_box = tk.Text(main_frame, wrap=tk.WORD, width=80, height=20)
>output_box.pack(pady=10, expand=True, fill=tk.BOTH)
>output_box.bind('<Control-Key>', edit_text)
>
>export_button = ttk.Button(main_frame, text="导出文件", command=export_to_word)
>export_button.pack(pady=10)
>
>root.mainloop()
>```
>
>这个优化后的代码调整了控件的布局，使程序的外观更加整洁。添加了`ttk.Frame`以实现更好的外观，同时使用了`fill`和`expand`选项，使得文本框能够随窗口大小调整而改变尺寸。最后，我们将所有的`tk.Button`替换为`ttk.Button`以保持一致的外观风格。

优化后的布局

![优化后的布局](./img/prefLayout.png)

可以看到，整体布局比之前合理了。



### API-key设置

刚刚忘记将API-key设置为手动输入了。

这里再补充一下，继续然GPT帮我们将功能完成

> prompt：下一个需求是，在原有的应用中，去除默认的openai的api-key，改为让用户可以输入和修改自己的api-key。 
>
> api-key输入后，需要在下一次使用的时候，加载进来。 
>
> api-key相关功能并列放在最上面一行

> user:
>
> 为了实现这个需求，我们需要对现有的代码进行以下修改：
>
> 1. 移除默认的OpenAI API密钥。
> 2. 添加一个新的输入框，让用户输入他们自己的API密钥。
> 3. 提供一个按钮，用于保存用户的API密钥。
> 4. 在程序启动时，尝试从一个文件中读取保存的API密钥。
> 5. 将API密钥输入框和保存按钮放在最上面一行。
>
> 以下是修改后的代码：
>
> ```python
> import os
> 
> # 移除默认的OpenAI API密钥
> # openai.api_key = "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"
> 
> API_KEY_FILE = 'api_key.txt'
> 
> 
> def load_api_key():
>     if os.path.exists(API_KEY_FILE):
>         with open(API_KEY_FILE, 'r') as f:
>             return f.read().strip()
>     return ''
> 
> 
> def save_api_key():
>     with open(API_KEY_FILE, 'w') as f:
>         f.write(api_key_entry.get())
>     openai.api_key = api_key_entry.get()
>     messagebox.showinfo("成功", "API密钥已保存。")
> 
> 
> # 在程序启动时，尝试从一个文件中读取保存的API密钥
> openai.api_key = load_api_key()
> 
> # 省略其他代码...
> 
> # 创建API密钥输入框和保存按钮
> api_key_frame = ttk.Frame(main_frame)
> api_key_frame.pack(pady=5)
> 
> ttk.Label(api_key_frame, text="API密钥：").pack(side=tk.LEFT, padx=5)
> api_key_entry = ttk.Entry(api_key_frame, width=40)
> api_key_entry.pack(side=tk.LEFT, padx=5)
> api_key_entry.insert(0, openai.api_key)
> 
> save_api_key_button = ttk.Button(api_key_frame, text="保存API密钥", command=save_api_key)
> save_api_key_button.pack(side=tk.LEFT, padx=5)
> 
> # 省略其他代码...
> ```
>
> 这个修改后的代码将会在程序启动时尝试从`api_key.txt`文件中读取API密钥。如果文件不存在或者内容为空，用户需要在输入框中输入他们自己的API密钥，并点击保存按钮。

把代码复制到工程中，测试一下

![测试API-key能否手动使用](./img/setApiKey.png)

可以看到，现在通过手动输入API-key，可以成功的调用api

### api调用失败时提示

> prompt:下一需求是，当网络连接失败，或其他原因导致无法调用api的时候，提示用户无法使用openai的服务

> GPT:
>
> 为了实现这个需求，我们需要在调用OpenAI API时捕获可能的异常，并在发生异常时给用户一个友好的提示。我们可以通过修改`generate_text`函数来实现这一点。
>
> 在`generate_text`函数中，我们将`openai.Completion.create()`函数调用包裹在一个`try`语句中，并在`except`语句中捕获可能的异常。当发生异常时，我们可以使用`messagebox.showerror()`函数显示一个错误对话框。
>
> 以下是修改后的`generate_text`函数：
>
> ```python
> def generate_text():
>     prompt = input_box.get()
>     if prompt.strip() != "":
>         try:
>             response = openai.Completion.create(
>                 engine="text-davinci-003",
>                 prompt=prompt,
>                 max_tokens=4000,
>                 n=1,
>                 stop=None,
>                 temperature=0.7,
>             )
>             output_text = response.choices[0].text
>             output_box.delete(1.0, tk.END)
>             output_box.insert(tk.END, output_text)
>         except Exception as e:
>             messagebox.showerror("错误", f"无法调用OpenAI API：{str(e)}")
> ```
>
> 现在，如果在调用API时出现网络连接失败或其他错误，程序会捕获异常并向用户显示一个友好的错误提示。

GPT给出的方案是使用try-except处理异常。报错的时候，就弹出消息框。

给出的代码只有generate_text这个函数。

但其实edit_text函数，也使用了。我们在这两个地方都加上提示

``` python

def generate_text():
    prompt = input_box.get()
    if prompt.strip() != "":
        try:
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

```

使用一个错误的密钥测试一下。

![使用api异常](./img/useAPIError.png)

现在任何调用api失败的时候，都会提示用户了。

### 最终代码

``` py
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

```



### 生成可执行文件

> prompt:现在代码已经写完了，如何将代码打包成可执行文件

> GPT:
>
> 要将Python代码打包成可执行文件，您可以使用`PyInstaller`库。首先，确保您已经安装了`PyInstaller`。如果没有，请使用以下命令安装：
>
> ```bash
> pip install pyinstaller
> ```
>
> 安装完成后，您可以使用`pyinstaller`命令将代码打包成可执行文件。假设您的代码文件名为`ai_writer.py`，可以使用以下命令打包：
>
> ```bash
> pyinstaller --onefile ai_writer.py
> ```
>
> `--onefile`参数表示将所有依赖项打包成一个单独的可执行文件。
>
> 打包完成后，您可以在`dist`文件夹下找到生成的可执行文件。对于Windows系统，它将是一个`.exe`文件；对于macOS和Linux系统，它将是一个可执行的二进制文件。
>
> 注意：请确保您的计算机上已经安装了与源代码中使用的库相匹配的库版本，以避免在生成可执行文件时出现版本不兼容的问题。在这个例子中，您需要安装`openai`，`tkinter`和`python-docx`库。

安装一下pyInstaller

![安装PyInstaller.png](./img/installPyInstaller.png)

生成可执行文件

![生成可执行文件](.\img\installProject.png)

......省略中间信息

![执行结果](.\img\installProjectResult.png)

在项目的dist文件中，我们可以看到main.exe文件生成了

![最终文件](./img/exeFile.png)

从文件下中找到可执行文件执行一下。

![文件夹中的可执行文件](./img/dirExeFile.png)

![运行结果](.\img\packageResult.png)
