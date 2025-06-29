# ==============================================================================
# 文件: APP/Converters/Pandoc_Converter.py
# (此版本增加了为每次转换创建独立输出文件夹的功能)
# ==============================================================================

import subprocess
from pathlib import Path
import datetime
import fitz
import os


def run_pandoc(input_path: str, template_path: str, base_output_dir: str) -> tuple[bool, str]:
    """
    执行 Pandoc 命令，为每次转换创建一个带时间戳的子文件夹，并将 .tex 文件输出到其中。
    """
    input_file = Path(input_path)
    template_file = Path(template_path)
    output_path = Path(base_output_dir)

    if not input_file.exists(): return False, f"错误：输入文件未找到: {input_path}"
    if not template_file.exists(): return False, f"错误：模板文件未找到: {template_path}"
    if not output_path.is_dir(): return False, f"错误：输出目录不存在: {base_output_dir}"

    pandoc_input_file = input_file
    temp_txt_file = None

    try:
        # ===============================================================
        #  !!!!!!!!!      核心修改：创建独立的输出子文件夹     !!!!!!!!!
        # ===============================================================
        # 1. 获取当前时间戳
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # 2. 构建新的子文件夹名 (格式: 文件名-时间戳)
        new_folder_name = f"{timestamp}-{input_file.stem}"

        # 3. 创建完整的子文件夹路径
        final_output_dir = output_path / new_folder_name

        # 4. 在文件系统中创建这个新文件夹
        os.makedirs(final_output_dir, exist_ok=True)
        # ===============================================================

        if input_file.suffix.lower() == '.pdf':
            print(f"检测到 PDF 文件，正在提取文本...")
            try:
                # 注意：从PDF提取的临时文件将放在新的子文件夹中，便于管理
                doc = fitz.open(input_file)
                pdf_text = "".join(page.get_text("text") for page in doc)
                doc.close()
                if not pdf_text.strip(): return False, f"错误：无法从 PDF 文件 {input_file.name} 中提取任何文本。"

                temp_txt_path = final_output_dir / f"{input_file.stem}_temp.txt"
                temp_txt_path.write_text(pdf_text, encoding="utf-8")

                pandoc_input_file = temp_txt_path
                temp_txt_file = temp_txt_path
                print(f"PDF 文本已提取至临时文件: {temp_txt_path}")
            except Exception as e:
                return False, f"处理 PDF 文件时出错: {e}"

        # 5. 定义最终输出的 .tex 文件名和路径
        output_tex_file = final_output_dir / f"{timestamp}-{input_file.stem}.tex"

        command = [
            "pandoc",
            str(pandoc_input_file),
            "--template", str(template_file),
            "--no-highlight",
            "-o", str(output_tex_file)  # 输出目标是新文件夹中的 .tex 文件
        ]

        print(f"正在执行命令: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')

        # 6. 修改成功信息，指向新的文件夹路径
        success_message = f"成功！输出文件已保存至新的文件夹中:\n{final_output_dir}"
        return True, success_message

    except FileNotFoundError:
        return False, "错误：Pandoc 未安装或未在系统路径中。"
    except subprocess.CalledProcessError as e:
        return False, f"Pandoc 生成 .tex 文件失败，退出码为 {e.returncode}。\n错误详情:\n{e.stderr}"
    finally:
        if temp_txt_file and temp_txt_file.exists():
            temp_txt_file.unlink()
            print(f"已删除临时文件: {temp_txt_file}")

# # ==============================================================================
# # 文件: APP/Converters/Pandoc_Converter.py
# # (根据你的建议，此版本只输出 .tex 文件，不再直接编译 PDF)
# # ==============================================================================
#
# import subprocess
# from pathlib import Path
# import datetime
# import fitz
#
#
# def run_pandoc(input_path: str, template_path: str, output_dir: str) -> tuple[bool, str]:
#     """
#     执行 Pandoc 命令，将源文件转换为一个 .tex 文件，以便手动编译。
#     """
#     input_file = Path(input_path)
#     template_file = Path(template_path)
#     output_path = Path(output_dir)
#
#     if not input_file.exists(): return False, f"错误：输入文件未找到: {input_path}"
#     if not template_file.exists(): return False, f"错误：模板文件未找到: {template_path}"
#     if not output_path.is_dir(): return False, f"错误：输出目录不存在: {output_dir}"
#
#     pandoc_input_file = input_file
#     temp_txt_file = None
#
#     try:
#         if input_file.suffix.lower() == '.pdf':
#             print(f"检测到 PDF 文件，正在提取文本...")
#             try:
#                 doc = fitz.open(input_file)
#                 pdf_text = "".join(page.get_text("text") for page in doc)
#                 doc.close()
#                 if not pdf_text.strip(): return False, f"错误：无法从 PDF 文件 {input_file.name} 中提取任何文本。"
#
#                 temp_txt_path = output_path / f"{input_file.stem}_temp.txt"
#                 temp_txt_path.write_text(pdf_text, encoding="utf-8")
#
#                 pandoc_input_file = temp_txt_path
#                 temp_txt_file = temp_txt_path
#                 print(f"PDF 文本已提取至临时文件: {temp_txt_path}")
#             except Exception as e:
#                 return False, f"处理 PDF 文件时出错: {e}"
#
#         # ===============================================================
#         #  !!!!!!!!!      核心修改：输出目标改为 .tex 文件     !!!!!!!!!
#         # ===============================================================
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
#         # 1. 输出文件名后缀改为 .tex
#         output_filename = f"{timestamp}-output.tex"
#         output_tex_file = output_path / output_filename
#
#         # 2. 我们依然使用 --no-highlight 来生成最干净的 LaTeX 代码
#         command = [
#             "pandoc",
#             str(pandoc_input_file),
#             "--template", str(template_file),
#             "--no-highlight",
#             "-o", str(output_tex_file)  # 3. 输出目标是 .tex 文件
#         ]
#
#         print(f"正在执行命令: {' '.join(command)}")
#         # 注意：这里不再需要 --pdf-engine，因为我们不生成 PDF
#         result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
#
#         # 4. 修改成功信息
#         success_message = f"成功！中间 TeX 文件已保存至: {output_tex_file}\n请在终端中手动使用 'xelatex <文件名>' 命令来编译它。"
#         return True, success_message
#
#     except FileNotFoundError:
#         return False, "错误：Pandoc 未安装或未在系统路径中。"
#     except subprocess.CalledProcessError as e:
#         # Pandoc 在生成 .tex 文件时也可能失败
#         return False, f"Pandoc 生成 .tex 文件失败，退出码为 {e.returncode}。\n错误详情:\n{e.stderr}"
#     finally:
#         if temp_txt_file and temp_txt_file.exists():
#             temp_txt_file.unlink()
#             print(f"已删除临时文件: {temp_txt_file}")
