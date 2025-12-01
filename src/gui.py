"""简化的GUI界面（基于tkinter）"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
from main import CorpusAnalyzer
from utils.logger import logger


class AnalyzerGUI:
    """语料分析工具GUI"""
    
    def __init__(self, root):
        """初始化GUI"""
        self.root = root
        self.root.title("PPT语料分析工具")
        self.root.geometry("800x600")
        
        # 变量
        self.file_path = tk.StringVar()
        self.dimensions = tk.StringVar(value="老师,教学")
        self.analysis_type = tk.StringVar(value="both")
        self.output_dir = tk.StringVar(value="output")
        
        # 创建界面
        self._create_widgets()
        
        # 分析器
        self.analyzer = None
    
    def _create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = ttk.Label(
            self.root, 
            text="PPT主题生成场景语料分析工具", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(self.root, text="1. 选择语料文件", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(file_frame, textvariable=self.file_path, width=60).pack(side="left", padx=5)
        ttk.Button(file_frame, text="浏览", command=self._browse_file).pack(side="left")
        
        # 自定义维度输入
        dim_frame = ttk.LabelFrame(self.root, text="2. 输入自定义维度（多个用逗号分隔）", padding=10)
        dim_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(dim_frame, textvariable=self.dimensions, width=70).pack()
        ttk.Label(dim_frame, text="示例: 老师,教学 或 页数,风格", foreground="gray").pack()
        
        # 分析类型选择
        type_frame = ttk.LabelFrame(self.root, text="3. 选择分析类型", padding=10)
        type_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Radiobutton(type_frame, text="请求语料（需求分析）", 
                       variable=self.analysis_type, value="request").pack(anchor="w")
        ttk.Radiobutton(type_frame, text="反馈语料（效果反馈）", 
                       variable=self.analysis_type, value="feedback").pack(anchor="w")
        ttk.Radiobutton(type_frame, text="双场景分析", 
                       variable=self.analysis_type, value="both").pack(anchor="w")
        
        # 输出目录
        output_frame = ttk.LabelFrame(self.root, text="4. 输出目录", padding=10)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_dir, width=60).pack(side="left", padx=5)
        ttk.Button(output_frame, text="选择", command=self._browse_output).pack(side="left")
        
        # 开始按钮
        self.start_button = ttk.Button(
            self.root, 
            text="开始分析", 
            command=self._start_analysis,
            style="Accent.TButton"
        )
        self.start_button.pack(pady=10)
        
        # 进度显示区域
        log_frame = ttk.LabelFrame(self.root, text="分析日志", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, state="disabled")
        self.log_text.pack(fill="both", expand=True)
    
    def _browse_file(self):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择语料文件",
            filetypes=[
                ("Excel文件", "*.xlsx"),
                ("CSV文件", "*.csv"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.file_path.set(filename)
    
    def _browse_output(self):
        """浏览输出目录"""
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.output_dir.set(dirname)
    
    def _log(self, message: str):
        """添加日志"""
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
    
    def _start_analysis(self):
        """开始分析"""
        # 验证输入
        if not self.file_path.get():
            messagebox.showerror("错误", "请选择语料文件")
            return
        
        if not self.dimensions.get().strip():
            messagebox.showerror("错误", "请输入至少一个自定义维度")
            return
        
        # 解析维度
        dims = [d.strip() for d in self.dimensions.get().split(",") if d.strip()]
        
        # 禁用按钮
        self.start_button.config(state="disabled", text="分析中...")
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        
        # 在新线程中执行分析
        thread = threading.Thread(
            target=self._run_analysis,
            args=(self.file_path.get(), dims, self.analysis_type.get(), self.output_dir.get())
        )
        thread.daemon = True
        thread.start()
    
    def _run_analysis(self, file_path: str, dimensions: list, analysis_type: str, output_dir: str):
        """执行分析（在独立线程中）"""
        try:
            self._log("="*60)
            self._log("初始化分析器...")
            
            # 初始化分析器
            self.analyzer = CorpusAnalyzer()
            
            self._log(f"文件: {file_path}")
            self._log(f"自定义维度: {', '.join(dimensions)}")
            self._log(f"分析类型: {analysis_type}")
            self._log("="*60)
            self._log("")
            
            # 执行分析
            results = self.analyzer.analyze(
                file_path=file_path,
                custom_dimensions=dimensions,
                analysis_type=analysis_type,
                output_dir=output_dir
            )
            
            # 完成
            self._log("")
            self._log("="*60)
            self._log("分析完成！")
            self._log(f"结果已保存到: {output_dir}")
            self._log("="*60)
            
            # 弹出提示
            self.root.after(0, lambda: messagebox.showinfo(
                "完成", 
                f"分析完成！\n结果已保存到: {output_dir}"
            ))
            
        except Exception as e:
            error_msg = f"分析失败: {str(e)}"
            self._log("")
            self._log(error_msg)
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
        
        finally:
            # 恢复按钮
            self.root.after(0, lambda: self.start_button.config(state="normal", text="开始分析"))


def main():
    """启动GUI"""
    root = tk.Tk()
    app = AnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

