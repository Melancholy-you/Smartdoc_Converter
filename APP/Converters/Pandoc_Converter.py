# ==============================================================================
# 文件: APP/Converters/Pandoc_Converter.py
# 描述: 本模块包含使用 Pandoc 命令行工具来转换文档的核心逻辑。
# (此文件名已根据你的项目结构更新为 PascalCase 风格)
# ==============================================================================

import subprocess
from pathlib import Path


def run_pandoc(input_path: str, template_path: str, output_dir: str) -> tuple[bool, str]:
    """
    执行 Pandoc 命令，使用指定的 LaTeX 模板将源文件转换为 PDF。

    参数:
        input_path (str): 源文件（如 .md, .docx）的完整路径。
        template_path (str): LaTeX 模板文件（.tex）的完整路径。
        output_dir (str): 输出的 PDF 文件将被保存到的目录。

    返回:
        tuple[bool, str]: 一个元组，包含：
                          - 一个布尔值，表示成功 (True) 或失败 (False)。
                          - 一条字符串消息，包含结果详情或错误信息。
    """
    # --- 1. 输入验证 ---
    input_file = Path(input_path)
    template_file = Path(template_path)
    output_path = Path(output_dir)

    if not input_file.exists():
        return False, f"错误：输入文件未找到: {input_path}"
    if not template_file.exists():
        return False, f"错误：模板文件未找到: {template_path}"
    if not output_path.is_dir():
        return False, f"错误：输出目录不存在: {output_dir}"

    # --- 2. 准备 Pandoc 命令 ---
    output_pdf_file = output_path / f"{input_file.stem}.pdf"

    command = [
        "pandoc",
        str(input_file),
        "--template", str(template_file),
        "--pdf-engine=xelatex",
        "--listings",
        "-o", str(output_pdf_file)
    ]

    # --- 3. 执行命令并处理错误 ---
    try:
        print(f"正在执行命令: {' '.join(command)}")
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        success_message = f"成功！文件已保存至: {output_pdf_file}"
        print(result.stdout)
        return True, success_message

    except FileNotFoundError:
        return False, "错误：Pandoc 未安装或未在系统路径中。"

    except subprocess.CalledProcessError as e:
        error_message = (
            f"Pandoc 转换失败，退出码为 {e.returncode}。\n"
            f"错误详情:\n"
            f"{e.stderr}"
        )
        return False, error_message
