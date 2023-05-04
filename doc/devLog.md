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
