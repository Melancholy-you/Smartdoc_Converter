# ==============================================================================
# 文件: APP/main.py
# 描述: 这是应用程序的主入口和测试脚本。
# (此文件已重构，以匹配你的项目结构)
# ==============================================================================

import os
# 注意：这里的导入路径已根据你的项目结构进行更新
from APP.Converters.Pandoc_Converter import run_pandoc


def setup_test_environment():
    """根据你的项目结构创建测试所需的文件和目录。"""
    print("--- 正在设置测试环境 ---")

    # 确保你的项目结构中定义的目录存在
    os.makedirs("Tempaltes", exist_ok=True)
    os.makedirs("Test_Output", exist_ok=True)  # 创建一个专门的输出目录用于测试

    # --- 创建一个示例 Markdown 文件 (在项目根目录) ---
    md_content = """
# SmartDoc Converter 测试报告

这是用于测试 **SmartDoc Converter** 后端功能的报告。

## 功能点

- **粗体** 和 *斜体*
- `代码片段`

```python
def hello():
    print("Hello, Pandoc!")
```
"""
    with open("test_input_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("已创建测试输入文件: test_input_report.md")

    # --- 在你的 `Tempaltes` 文件夹中创建示例模板文件 ---
    tex_content = r"""
\documentclass{article}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{ctex}
\usepackage{listings}
\usepackage{xcolor}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    numbers=left,
    numbersep=5pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2
}
\lstset{style=mystyle}

\title{我的专属测试模板}
\author{SmartDoc Converter}
\date{\today}

\begin{document}
\maketitle

$body$

\newpage
\section*{附录}
这是模板中固定的附录内容。

\end{document}
"""
    # 注意：路径已更新为你的文件夹名 `Tempaltes`
    with open("Tempaltes/Latex.tex", "w", encoding="utf-8") as f:
        f.write(tex_content)
    print("已创建测试模板文件: Tempaltes/Latex.tex")
    print("--- 测试环境设置完毕 ---\n")


def main():
    """主函数，用于运行测试。"""
    setup_test_environment()

    # --- 测试案例 1: 成功转换 ---
    print("--- 测试案例 1: 成功转换 ---")
    # 注意：所有路径都已更新
    success, message = run_pandoc(
        input_path="test_input_report.md",
        template_path="Tempaltes/Latex.tex",
        output_dir="Test_Output"
    )
    print(f"结果: {'成功' if success else '失败'}")
    print(f"消息:\n{message}\n")

    # --- 测试案例 2: 输入文件未找到 ---
    print("--- 测试案例 2: 输入文件未找到 ---")
    success, message = run_pandoc(
        input_path="non_existent_file.md",
        template_path="Tempaltes/Latex.tex",
        output_dir="Test_Output"
    )
    print(f"结果: {'成功' if success else '失败'}")
    print(f"消息:\n{message}\n")


if __name__ == "__main__":
    # 运行方式保持不变:
    # 1. 在终端里，确保你位于项目根目录 (Smartdoc_Converter)
    # 2. 执行命令: python -m APP.main
    main()

