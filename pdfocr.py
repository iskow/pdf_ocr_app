import os
import sys
import subprocess

os.environ["PATH"] = r"C:\Program Files\Tesseract-OCR" + ";" + os.environ.get("PATH", "")
#removes popup terminal windows
if sys.platform == "win32":
    _Popen = subprocess.Popen
    class _NoWindowPopen(_Popen):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('creationflags', subprocess.CREATE_NO_WINDOW)
            super().__init__(*args, **kwargs)
    subprocess.Popen = _NoWindowPopen

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import ocrmypdf
import threading
import pikepdf

window = ttk.Window(themename="superhero")
window.title("DO PDF OCR")
window.geometry("600x200")


input_folder = tk.StringVar()
output_folder = tk.StringVar()
max_threads = tk.IntVar(value=2)  


def browse_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder.set(folder_selected)

def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder.set(folder_selected)
    

frame_input = ttk.Frame(window)
frame_input.pack(padx=10, pady=10, fill=tk.X)

btn_browse = ttk.Button(frame_input, text="Browse PDF Folder", command=browse_input_folder, width = 17)
btn_browse.pack(side=tk.LEFT)

entry_input = ttk.Entry(frame_input, textvariable=input_folder, width=60)
entry_input.pack(side=tk.LEFT, padx=10, fill = tk.X, expand=True)

frame_output = ttk.Frame(window)
frame_output.pack(padx=10, pady=10, fill=tk.X)

btn_browse_output = ttk.Button(frame_output, text="Browse Output Folder", command=browse_output_folder, width = 17)
btn_browse_output.pack(side=tk.LEFT)

entry_output = ttk.Entry(frame_output, textvariable=output_folder, width=60)
entry_output.pack(side=tk.LEFT, padx=10, fill = tk.X, expand=True)

frame_threads = ttk.Frame(window)
frame_threads.pack(padx=10, pady=5, fill=tk.X)

lbl_threads = ttk.Label(frame_threads, text="Max Threads:")
lbl_threads.pack(side=tk.LEFT)

#max threads capped at 8
spin_threads = ttk.Spinbox(frame_threads, from_=1, to=8, textvariable=max_threads, width=5) 
spin_threads.pack(side=tk.LEFT, padx=10)

progress = ttk.Progressbar(frame_threads, orient=tk.HORIZONTAL, mode='determinate')
progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

def startocr():
    def run_ocr():
        activethreads = threading.Semaphore(max_threads.get())
        page_lock = threading.Lock()
        total_pages = 0
        log_path = os.path.join(output_folder.get(), "ocr_errors.log")
        pdf_files = [f for f in os.listdir(input_folder.get()) if f.endswith('.pdf')]
        total_files = len(pdf_files)
        progress['maximum'] = total_files
        progress['value'] = 0

        #OCR loop for each pdf file
        def process_file(filename): 
            nonlocal total_pages

            with activethreads:
                input_path = os.path.join(input_folder.get(), filename)
                output_path = os.path.join(output_folder.get(), filename)

                with pikepdf.open(input_path) as pdf:
                    page_count = len(pdf.pages)
                    lbl_status.config(text=f"Processing {filename} ({page_count} pages)")

                    #Acroform - place to look for pdf fields - is signed flags true if signature found
                    fields = pdf.Root.get("/AcroForm", {}).get("/Fields",[])
                    is_signed = any(pdf.get_object(f).get("/FT") == "/Sig" for f in fields)

                    if is_signed:
                        with open(log_path, "a") as log:
                            log.write(f"Skipped - PDF with Digital Signature: {filename}\n")
                        return


                try:
                    #timeout is 900sec or 15min - we can set to 0 for no timeout, deskew to straighten pages - pdfs with partial text are skipped
                    ocrmypdf.ocr(input_path, output_path, tesseract_timeout=900, deskew=True) 
                    with page_lock:
                        total_pages += page_count
                    progress['value'] += 1
                    window.update_idletasks()
                except Exception as e:
                    #exception loop popup window and added log file to dest folder just in case
                    messagebox.showerror("Error", f"Error occurred while processing {filename}:\n{e}")
                    with open(log_path, "a") as log:
                        log.write(f"{filename}: {e}\n")
        
        #loops through pdf files, creates thread for each file - calls process file and starts the thread
        threads = []
        for filename in pdf_files: 
            thread = threading.Thread(target=process_file, args=(filename,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        lbl_status.config(text=f"Total Pages Processed: {total_pages}")

        btn_run.config(state=tk.NORMAL)
        messagebox.showinfo("Done", f"OCR completed. Processed {len(pdf_files)} PDFs.")
    
    btn_run.config(state=tk.DISABLED)
    threading.Thread(target=run_ocr).start()


frame_run = ttk.Frame(window)
frame_run.pack(padx=10, pady=10, anchor="w")

btn_run = ttk.Button(frame_run, text="Run OCR", command=startocr)
btn_run.pack(side=tk.LEFT)

lbl_status = ttk.Label(frame_run, text="")
lbl_status.pack(side=tk.LEFT, padx=10)


window.mainloop()
