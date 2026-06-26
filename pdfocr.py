import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ocrmypdf
import threading
import os
import pikepdf

window = tk.Tk()
window.title("DO PDF OCR")
window.geometry("500x200")

input_folder = tk.StringVar()
output_folder = tk.StringVar()
max_threads = tk.IntVar(value=2)  # Default to 2


def browse_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder.set(folder_selected)

def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder.set(folder_selected)
    

frame_input = tk.Frame(window)
frame_input.pack(padx=10, pady=10, anchor="w")

btn_browse = tk.Button(frame_input, text="Browse PDF Folder", command=browse_input_folder)
btn_browse.pack(side=tk.LEFT)

entry_input = tk.Entry(frame_input, textvariable=input_folder, width=40, state='readonly')
entry_input.pack(side=tk.LEFT, padx=10)

frame_output = tk.Frame(window)
frame_output.pack(padx=10, pady=10, anchor="w")

btn_browse_output = tk.Button(frame_output, text="Browse Output Folder", command=browse_output_folder)
btn_browse_output.pack(side=tk.LEFT)

entry_output = tk.Entry(frame_output, textvariable=output_folder, width=40, state='readonly')
entry_output.pack(side=tk.LEFT, padx=10)

frame_threads = tk.Frame(window)
frame_threads.pack(padx=10, pady=5, anchor="w")

lbl_threads = tk.Label(frame_threads, text="Max Threads:")
lbl_threads.pack(side=tk.LEFT)

spin_threads = tk.Spinbox(frame_threads, from_=1, to=8, textvariable=max_threads, width=5) #max threads capped at 8
spin_threads.pack(side=tk.LEFT, padx=10)

def startocr():
    def run_ocr():
        activethreads = threading.Semaphore(max_threads.get())
        page_lock = threading.Lock()
        total_pages = 0
        pdf_files = [f for f in os.listdir(input_folder.get()) if f.endswith('.pdf')]
        total_files = len(pdf_files)
        progress['maximum'] = total_files
        progress['value'] = 0

        def process_file(filename): #OCR loop for each pdf file
            nonlocal total_pages
            with activethreads:
                input_path = os.path.join(input_folder.get(), filename)
                output_path = os.path.join(output_folder.get(), filename)

                with pikepdf.open(input_path) as pdf:
                    page_count = len(pdf.pages)
                    lbl_status.config(text=f"Processing {filename} ({page_count} pages)")
                try:
                    ocrmypdf.ocr(input_path, output_path)
                    with page_lock:
                        total_pages += page_count
                    progress['value'] += 1
                    window.update_idletasks()
                except Exception as e:
                    messagebox.showerror("Error", f"Error occurred while processing {filename}:\n{e}")
        
        threads = []
        for filename in pdf_files: #loops through pdf files, creates thread for each file - calls process file and starts the thread
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


frame_run = tk.Frame(window)
frame_run.pack(padx=10, pady=10, anchor="w")

btn_run = tk.Button(frame_run, text="Run OCR", command=startocr)
btn_run.pack(side=tk.LEFT)

lbl_status = tk.Label(frame_run, text="")
lbl_status.pack(side=tk.LEFT, padx=10)

progress = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress.pack(padx=10, pady=10, anchor="w")

window.mainloop()
