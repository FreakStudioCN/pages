# Python env   :               
# -*- coding: utf-8 -*-        
# @Time    : 2026/3/7 下午4:04   
# @Author  : 李清水            
# @File    : view_json.py       
# @Description :

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os


class BIPESJSONViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("BIPES 积木 JSON 可视化工具")
        self.root.geometry("1200x800")

        # 初始化变量
        self.json_data = None
        self.current_file = ""

        # 创建主布局
        self._create_widgets()

    def _create_widgets(self):
        # 1. 顶部操作栏
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        # 文件选择按钮
        ttk.Button(top_frame, text="选择JSON文件", command=self.load_json_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="刷新显示", command=self.refresh_display).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="复制选中内容", command=self.copy_selected).pack(side=tk.LEFT, padx=5)

        # 当前文件标签
        self.file_label = ttk.Label(top_frame, text="未选择文件")
        self.file_label.pack(side=tk.RIGHT, padx=5)

        # 2. 树形展示区域（核心）
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 树形视图
        self.tree = ttk.Treeview(tree_frame, columns=("value"), show="tree headings")
        self.tree.heading("value", text="内容")
        self.tree.column("value", width=800)

        # 滚动条
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        # 布局
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # 3. 底部信息栏
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(bottom_frame, text="选中项详情：").pack(side=tk.LEFT)
        self.detail_text = tk.Text(bottom_frame, height=6, wrap=tk.WORD)
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=5)

        # 绑定树形选择事件
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_json_file(self):
        """选择并加载JSON文件"""
        file_path = filedialog.askopenfilename(
            title="选择BIPES JSON文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.json_data = json.load(f)
            self.current_file = file_path
            self.file_label.config(text=f"当前文件：{os.path.basename(file_path)}")
            self._build_tree()
            messagebox.showinfo("成功", f"已加载文件：{os.path.basename(file_path)}")
        except json.JSONDecodeError:
            messagebox.showerror("错误", "JSON格式错误，请检查文件")
        except Exception as e:
            messagebox.showerror("错误", f"加载失败：{str(e)}")

    def _build_tree(self):
        """构建树形结构（通用解析，适配所有同格式JSON）"""
        # 清空现有内容
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.json_data:
            return

        # 1. 添加Meta节点
        meta_node = self.tree.insert("", tk.END, text="Meta信息", values=[""])
        for key, value in self.json_data.get("meta", {}).items():
            self.tree.insert(meta_node, tk.END, text=key, values=[str(value)])

        # 2. 添加依赖节点
        dep_node = self.tree.insert("", tk.END, text="依赖项", values=[""])
        for dep in self.json_data.get("dependencies", []):
            self.tree.insert(dep_node, tk.END, text=dep, values=["依赖模块"])

        # 3. 添加Blocks节点（核心，递归解析）
        blocks_node = self.tree.insert("", tk.END, text="积木列表",
                                       values=[f"共{len(self.json_data.get('blocks', []))}个积木"])
        for idx, block in enumerate(self.json_data.get("blocks", [])):
            block_node = self.tree.insert(blocks_node, tk.END,
                                          text=f"积木{idx + 1}: {block.get('type', '未知类型')}",
                                          values=[block.get('message', '无描述')])
            # 递归解析积木的所有字段
            self._insert_dict_to_tree(block_node, block)

    def _insert_dict_to_tree(self, parent_node, data, prefix=""):
        """递归将字典插入树形结构（通用适配任意字段）"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "inputs":  # 单独处理inputs（数组）
                    input_node = self.tree.insert(parent_node, tk.END, text=f"{prefix}{key}", values=["输入参数列表"])
                    for input_idx, input_item in enumerate(value):
                        input_item_node = self.tree.insert(input_node, tk.END, text=f"参数{input_idx + 1}",
                                                           values=[input_item.get('name', '未知参数')])
                        self._insert_dict_to_tree(input_item_node, input_item, f"{prefix}{key}.{input_idx + 1}.")
                else:
                    # 普通字段
                    if isinstance(value, (dict, list)):
                        # 复杂类型先建节点，再递归
                        child_node = self.tree.insert(parent_node, tk.END, text=f"{prefix}{key}",
                                                      values=[f"[{type(value).__name__}]"])
                        self._insert_dict_to_tree(child_node, value, f"{prefix}{key}.")
                    else:
                        self.tree.insert(parent_node, tk.END, text=f"{prefix}{key}", values=[str(value)])
        elif isinstance(data, list):
            # 纯数组（非inputs）
            for idx, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    child_node = self.tree.insert(parent_node, tk.END, text=f"{prefix}[{idx}]",
                                                  values=[f"[{type(item).__name__}]"])
                    self._insert_dict_to_tree(child_node, item, f"{prefix}[{idx}].")
                else:
                    self.tree.insert(parent_node, tk.END, text=f"{prefix}[{idx}]", values=[str(item)])
        else:
            # 基础类型
            self.tree.insert(parent_node, tk.END, text=prefix, values=[str(data)])

    def on_tree_select(self, event):
        """选中树形节点时显示详情"""
        self.detail_text.delete(1.0, tk.END)
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        # 获取节点路径和值
        path = []
        current = item
        while current:
            path.insert(0, self.tree.item(current, "text"))
            current = self.tree.parent(current)

        # 拼接详情
        detail = f"节点路径：{' > '.join(path)}\n"
        detail += f"节点值：{self.tree.item(item, 'values')[0]}\n\n"

        # 如果是积木节点，尝试获取完整的积木信息
        if "积木" in path[-1] and len(path) >= 2 and path[-2] == "积木列表":
            block_idx = int(path[-1].split(":")[0].replace("积木", "")) - 1
            block_data = self.json_data.get("blocks", [])[block_idx]
            detail += "完整积木信息：\n"
            detail += json.dumps(block_data, ensure_ascii=False, indent=2)

        self.detail_text.insert(1.0, detail)

    def copy_selected(self):
        """复制选中节点的内容到剪贴板"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选中一个节点")
            return

        item = selected_items[0]
        value = self.tree.item(item, "values")[0]
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        messagebox.showinfo("成功", "已复制选中内容到剪贴板")

    def refresh_display(self):
        """刷新当前显示的JSON内容"""
        if self.current_file and os.path.exists(self.current_file):
            try:
                with open(self.current_file, "r", encoding="utf-8") as f:
                    self.json_data = json.load(f)
                self._build_tree()
                messagebox.showinfo("成功", "已刷新显示")
            except Exception as e:
                messagebox.showerror("错误", f"刷新失败：{str(e)}")
        else:
            messagebox.showwarning("提示", "请先加载一个有效的JSON文件")


if __name__ == "__main__":
    root = tk.Tk()
    app = BIPESJSONViewer(root)
    root.mainloop()