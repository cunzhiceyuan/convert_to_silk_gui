import os
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import subprocess
import pilk

class SilkConverterApp:
    def __init__(self, root):
        self.root = root
        root.title("音频转 Silk 工具")
        root.geometry("700x500")

        # 输入文件列表
        self.input_files = []

        # 界面组件
        tk.Label(root, text="输入音频文件/文件夹:").pack(anchor='w', padx=10, pady=(10,0))
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill='x', padx=10, pady=5)
        self.input_entry = tk.Entry(self.input_frame, state='readonly')
        self.input_entry.pack(side='left', fill='x', expand=True)
        tk.Button(self.input_frame, text="添加文件", command=self.add_files).pack(side='left', padx=5)
        tk.Button(self.input_frame, text="添加文件夹", command=self.add_folder).pack(side='left')
        tk.Button(self.input_frame, text="清空列表", command=self.clear_files).pack(side='left', padx=5)

        # 输出文件夹
        tk.Label(root, text="输出文件夹:").pack(anchor='w', padx=10)
        self.output_frame = tk.Frame(root)
        self.output_frame.pack(fill='x', padx=10, pady=5)
        self.output_entry = tk.Entry(self.output_frame)
        self.output_entry.pack(side='left', fill='x', expand=True)
        tk.Button(self.output_frame, text="浏览", command=self.select_output).pack(side='left', padx=5)

        # 转换按钮
        self.convert_btn = tk.Button(root, text="开始转换", command=self.start_conversion, bg='lightgreen')
        self.convert_btn.pack(pady=10)

        # 日志区域
        tk.Label(root, text="转换日志:").pack(anchor='w', padx=10)
        self.log_area = scrolledtext.ScrolledText(root, height=20, state='disabled')
        self.log_area.pack(fill='both', expand=True, padx=10, pady=5)

    def log(self, message):
        """在日志区域显示消息"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update_idletasks()

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="选择音频文件",
            filetypes=[("音频文件", "*.mp3 *.flac *.wav *.aac *.ogg *.m4a *.opus *.wma"), ("所有文件", "*.*")]
        )
        for f in files:
            if f not in self.input_files:
                self.input_files.append(f)
        self.update_input_display()

    def add_folder(self):
        folder = filedialog.askdirectory(title="选择包含音频文件的文件夹")
        if folder:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(('.mp3','.flac','.wav','.aac','.ogg','.m4a','.opus','.wma')):
                        full_path = os.path.join(root, file)
                        if full_path not in self.input_files:
                            self.input_files.append(full_path)
            self.update_input_display()

    def clear_files(self):
        self.input_files.clear()
        self.update_input_display()

    def update_input_display(self):
        self.input_entry.config(state='normal')
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, f"共 {len(self.input_files)} 个文件")
        self.input_entry.config(state='readonly')

    def select_output(self):
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("警告", "请先添加要转换的音频文件")
            return
        output_dir = self.output_entry.get().strip()
        if not output_dir:
            messagebox.showwarning("警告", "请选择输出文件夹")
            return
        # 禁用转换按钮，避免重复点击
        self.convert_btn.config(state='disabled', text='转换中...')
        # 在新线程中执行转换，避免界面卡死
        thread = threading.Thread(target=self.batch_convert, args=(output_dir,))
        thread.daemon = True
        thread.start()

    def batch_convert(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        success_count = 0
        total = len(self.input_files)
        for idx, audio_file in enumerate(self.input_files, 1):
            self.log(f"[{idx}/{total}] 正在处理: {os.path.basename(audio_file)}")
            try:
                # 生成临时 PCM 文件（位于系统临时目录）
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.pcm', delete=False) as tmp_pcm:
                    pcm_file = tmp_pcm.name
                # 输出 silk 文件
                base_name = os.path.splitext(os.path.basename(audio_file))[0]
                silk_file = os.path.join(output_dir, f"{base_name}.silk")
                # 1. 转 PCM
                if self.convert_to_pcm(audio_file, pcm_file):
                    # 2. PCM 转 Silk
                    if self.convert_pcm_to_silk(pcm_file, silk_file):
                        success_count += 1
                        self.log(f"✓ 转换成功: {silk_file}")
                    else:
                        self.log(f"✗ Silk 编码失败: {audio_file}")
                else:
                    self.log(f"✗ PCM 转换失败: {audio_file}")
            except Exception as e:
                self.log(f"✗ 处理出错: {audio_file} - {str(e)}")
            finally:
                # 删除临时 PCM 文件
                if os.path.exists(pcm_file):
                    os.remove(pcm_file)
        self.log(f"\n转换完成！成功: {success_count}/{total}")
        self.root.after(0, lambda: self.convert_btn.config(state='normal', text='开始转换'))

    def convert_to_pcm(self, input_file, pcm_file):
        """调用 ffmpeg 转为 24000Hz 单声道 s16le PCM"""
        try:
            cmd = ['ffmpeg', '-i', input_file, '-ac', '1', '-ar', '24000', '-f', 's16le', '-y', pcm_file]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"ffmpeg 错误: {e.stderr.decode() if e.stderr else str(e)}")
            return False
        except FileNotFoundError:
            self.log("未找到 ffmpeg，请确认 ffmpeg 已安装并加入 PATH")
            return False

    def convert_pcm_to_silk(self, pcm_file, silk_file):
        """使用 pilk 编码 Silk"""
        try:
            pilk.encode(pcm_file, silk_file, pcm_rate=24000, tencent=True)
            return True
        except Exception as e:
            self.log(f"pilk 编码错误: {str(e)}")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = SilkConverterApp(root)
    root.mainloop()