import tkinter as tk
import webview
import threading

def load_videos():
    video_urls = entry.get().split(",")
    
    for url in video_urls:
        threading.Thread(target=open_browser, args=(url.strip(),)).start()

def open_browser(url):
    webview.create_window("YouTube Video", url)

# Create a Tkinter window
window = tk.Tk()
window.title("YouTube Videos")

# Create a label and entry field for video URLs
label = tk.Label(window, text="Enter YouTube Video URLs (separated by commas):")
label.pack()
entry = tk.Entry(window)
entry.pack()

# Create a button to load videos
button = tk.Button(window, text="Load Videos", command=load_videos)
button.pack()

# Start the Tkinter event loop
window.mainloop()
