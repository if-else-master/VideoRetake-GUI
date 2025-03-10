import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os
from pathlib import Path

class InferenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("影片音訊合成工具")
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="人臉影片:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.face_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.face_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="瀏覽", command=self.browse_face).grid(row=0, column=2)
        
        ttk.Label(main_frame, text="音訊檔案:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.audio_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.audio_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="瀏覽", command=self.browse_audio).grid(row=1, column=2)
        
        ttk.Label(main_frame, text="輸出路徑:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar(value="results/output.mp4")
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=5)
        ttk.Button(main_frame, text="瀏覽", command=self.browse_output).grid(row=2, column=2)
        
        ttk.Button(main_frame, text="執行推理", command=self.run_inference).grid(row=3, column=1, pady=20)
        
        self.status_var = tk.StringVar(value="準備就緒")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=3)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
    
    def browse_face(self):
        filename = filedialog.askopenfilename(
            title="選擇人臉影片",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if filename:
            self.face_path.set(filename)
    
    def browse_audio(self):
        filename = filedialog.askopenfilename(
            title="選擇音訊檔案",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            self.audio_path.set(filename)
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="選擇輸出位置",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def run_inference(self):
        if not os.path.exists(self.face_path.get()):
            self.status_var.set("錯誤：找不到人臉影片檔案")
            return
        if not os.path.exists(self.audio_path.get()):
            self.status_var.set("錯誤：找不到音訊檔案")
            return
            
        output_dir = os.path.dirname(self.output_path.get())
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        self.status_var.set("處理中...")
        self.progress.start()
        
        try:
            cmd = [
                "python3", "inference.py",
                "--face", self.face_path.get(),
                "--audio", self.audio_path.get(),
                "--outfile", self.output_path.get()
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.status_var.set("處理完成！輸出檔案：" + self.output_path.get())
            else:
                self.status_var.set(f"錯誤：{stderr}")
                
        except Exception as e:
            self.status_var.set(f"執行時發生錯誤：{str(e)}")
        
        finally:
            self.progress.stop()

def main():
    root = tk.Tk()
    app = InferenceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()