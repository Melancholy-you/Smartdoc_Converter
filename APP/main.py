
# ==============================================================================
# 文件: APP/main.py
# (此版本已采纳你的建议，不再创建模板文件，仅创建测试输入文件)
# ==============================================================================
import os
from APP.Converters.Pandoc_Converter import run_pandoc
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def main():
    """主函数，运行所有测试案例。"""
    # 定义你的模板路径，所有测试都将使用这个文件
    template_file_path = "Templates/Latex.tex"
    print(f"将使用模板: {template_file_path}\n")

    # --- 测试案例 1: 成功转换 Markdown ---
    print("--- 测试案例 1: 成功转换 Markdown ---")
    success, message = run_pandoc("APP/Input/Gemini CLI 深度分析 2025年6月29日.md", template_file_path, "Test_Output")
    print(f"结果: {'成功' if success else '失败'}\n消息:\n{message}\n")

    # --- 测试案例 2: 成功转换 PDF ---
    print("--- 测试案例 2: 成功转换 PDF ---")
    success, message = run_pandoc("APP/Input/个人系统重构.pdf", template_file_path, "Test_Output")
    print(f"结果: {'成功' if success else '失败'}\n消息:\n{message}\n")


if __name__ == "__main__":
    main()
