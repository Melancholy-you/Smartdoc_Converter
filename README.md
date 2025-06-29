# Smartdoc_Converter
核心使命: 创建一个桌面应用程序，它优雅地结合了 Pandoc 的转换精度和 本地大语言模型 (LLM) 的灵活性，为用户提供一个简单、强大、高度可定制的文档格式转换工具。
目标用户:
* 需要频繁撰写报告、论文的学生和学者。
* 需要处理格式化文档的技术写作者。
* 任何希望将自己的笔记（如 Word, Markdown）无缝套入精美 LaTeX 模板的用户。


核心功能 (MVP - 最小可行产品):
* GUI: 简洁直观的图形用户界面。
* 文件选择: 支持用户选择一个源文件 (如 .md, .docx, .txt)。
* 模板选择: 支持用户选择一个自定义的 LaTeX 模板 (.tex)。
* 引擎切换: 用户可以明确选择使用 Pandoc 或 LLM 作为转换引擎。
* 一键转换: “开始转换”按钮启动整个流程。
* 状态反馈: 实时向用户显示当前状态（如“正在转换...”、“成功”、“失败”及错误信息）。


技术栈 (Technology Stack):
* 编程语言: Python 3.9+
* GUI 框架: CustomTkinter (提供现代、美观的界面)
* 核心引擎1 (精确): Pandoc
* 核心引擎2 (灵活): Ollama 驱动的本地大模型 (如 Llama 3)
* Python 库: customtkinter, ollama, python-docx, subprocess
