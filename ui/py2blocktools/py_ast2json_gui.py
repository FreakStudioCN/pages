# Python env   :               
# -*- coding: utf-8 -*-        
# @Time    : 2026/3/7 下午4:08   
# @Author  : 李清水            
# @File    : py_ast2json_gui.py       
# @Description :

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
from pathlib import Path
import py_ast2json  # 导入py_ast2json.py的核心函数


class AST2JSONGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python AST → BIPES积木JSON 生成工具")
        self.root.geometry("1200x800")

        # 初始化变量
        self.selected_py_file = ""  # 选中的Python文件路径
        self.generated_json = ""  # 生成的JSON内容

        # 创建界面布局
        self._create_widgets()

    def _create_widgets(self):
        """构建GUI界面元素"""
        # 1. 顶部操作栏
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        # 文件选择区域
        ttk.Label(top_frame, text="Python驱动文件：").pack(side=tk.LEFT, padx=5)
        self.file_path_var = tk.StringVar(value="未选择文件")
        ttk.Label(top_frame, textvariable=self.file_path_var, width=80).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="选择文件", command=self.select_py_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="生成JSON", command=self.generate_json).pack(side=tk.LEFT, padx=5)

        # 2. 中间JSON预览区域（核心）
        preview_frame = ttk.Frame(self.root)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 预览区域标题
        ttk.Label(preview_frame, text="生成的BIPES积木JSON内容：").pack(anchor=tk.W)

        # JSON文本框 + 滚动条
        json_text_frame = ttk.Frame(preview_frame)
        json_text_frame.pack(fill=tk.BOTH, expand=True)

        self.json_text = tk.Text(json_text_frame, wrap=tk.NONE, font=("Consolas", 10))
        # 垂直滚动条
        scroll_y = ttk.Scrollbar(json_text_frame, orient=tk.VERTICAL, command=self.json_text.yview)
        # 水平滚动条（适配长行）
        scroll_x = ttk.Scrollbar(json_text_frame, orient=tk.HORIZONTAL, command=self.json_text.xview)
        self.json_text.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # 布局
        self.json_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # 3. 底部操作栏
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        # 功能按钮
        ttk.Button(bottom_frame, text="保存JSON文件", command=self.save_json_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="复制JSON内容", command=self.copy_json_content).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="清空预览", command=self.clear_preview).pack(side=tk.LEFT, padx=5)

        # 状态标签
        self.status_var = tk.StringVar(value="状态：就绪")
        ttk.Label(bottom_frame, textvariable=self.status_var).pack(side=tk.RIGHT, padx=5)

    def select_py_file(self):
        """选择Python驱动文件（.py）"""
        file_path = filedialog.askopenfilename(
            title="选择Python驱动文件",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")]
        )
        if not file_path:
            return

        # 验证文件合法性
        file_path = Path(file_path)
        if file_path.suffix != ".py":
            messagebox.showerror("错误", "仅支持选择.py格式的Python文件！")
            return

        self.selected_py_file = file_path
        self.file_path_var.set(f"{file_path}")
        self.status_var.set(f"状态：已选择文件 {file_path.name}")
        self.clear_preview()  # 选择新文件后清空预览

    def generate_json(self):
        """调用py_ast2json的核心函数生成JSON"""
        if not self.selected_py_file:
            messagebox.showwarning("提示", "请先选择有效的Python驱动文件！")
            return

        try:
            self.status_var.set(f"状态：正在解析 {self.selected_py_file.name}...")
            self.root.update()  # 刷新界面显示状态

            # 核心调用：使用py_ast2json的generate_generic_json函数生成JSON
            self.generated_json = py_ast2json.generate_generic_json(str(self.selected_py_file))

            # 显示JSON到预览框
            self.json_text.delete(1.0, tk.END)
            self.json_text.insert(1.0, self.generated_json)

            self.status_var.set(f"状态：JSON生成成功（{len(self.generated_json)} 字符）")
            messagebox.showinfo("成功", f"JSON生成完成！\n文件：{self.selected_py_file.name}")

        except SyntaxError as e:
            self.status_var.set("状态：AST解析失败（语法错误）")
            messagebox.showerror("解析错误", f"Python文件语法错误：\n{e}")
        except Exception as e:
            self.status_var.set("状态：JSON生成失败")
            messagebox.showerror("错误", f"生成JSON时出错：\n{str(e)}")

    def save_json_file(self):
        """保存生成的JSON到文件（默认与py文件同目录，同名.json）"""
        if not self.generated_json:
            messagebox.showwarning("提示", "请先生成有效的JSON内容！")
            return

        # 默认保存路径：原py文件同目录 + 同名.json
        default_save_path = self.selected_py_file.with_suffix(".json")

        # 选择保存路径
        save_path = filedialog.asksaveasfilename(
            title="保存BIPES积木JSON文件",
            initialfile=default_save_path.name,
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            initialdir=self.selected_py_file.parent
        )
        if not save_path:
            return

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.generated_json)

            self.status_var.set(f"状态：JSON已保存至 {save_path}")
            messagebox.showinfo("成功", f"JSON文件已保存：\n{save_path}")
        except Exception as e:
            self.status_var.set("状态：保存失败")
            messagebox.showerror("错误", f"保存JSON文件失败：\n{str(e)}")

    def copy_json_content(self):
        """复制预览框中的JSON内容到剪贴板"""
        if not self.generated_json:
            messagebox.showwarning("提示", "暂无JSON内容可复制！")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(self.generated_json)
        self.status_var.set("状态：JSON内容已复制到剪贴板")
        messagebox.showinfo("成功", "JSON内容已复制到剪贴板！")

    def clear_preview(self):
        """清空JSON预览框"""
        self.json_text.delete(1.0, tk.END)
        self.generated_json = ""
        self.status_var.set("状态：预览已清空")


def main():
    # 确保py_ast2json.py在Python路径中（同目录优先）
    if not Path("py_ast2json.py").exists():
        print("错误：未找到py_ast2json.py文件，请确保该文件与当前GUI文件在同一目录！")
        sys.exit(1)

    # 启动GUI
    root = tk.Tk()
    app = AST2JSONGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()