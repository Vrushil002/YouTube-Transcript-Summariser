"""
Spyder Editor

This is a temporary script file.
"""
import tkinter as tk
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Create the main window
window = tk.Tk()
window.title("YouTube Transcript Summarizer")
window.geometry("800x600+100+100")

# Create a label for the URL input
url_label = tk.Label(text="Enter the URL of the YouTube video:")
url_label.pack()

# Create an input field for the URL
url_entry = tk.Entry()
url_entry.pack()

def fetch_transcript(video_id):
  transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
  transcript = ' '.join([d['text'] for d in transcript_list])
  return transcript

def summarize_transcript(transcript):
    summariser = pipeline('summarization', model='t5-base')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary
    
# Create a function to summarize the transcript
def summarize():
  # Get the URL from the input field
  url = url_entry.get()
  video_id = url.split('=')[1]
  summary = summarize_transcript(fetch_transcript(video_id))
  
  summary_text.delete(1.0, tk.END)  # Clear the widget
  summary_text.insert(tk.END, summary)

# Create a button to trigger the summarization
summarize_button = tk.Button(text="Summarize", command=summarize, font=("Arial", 16), fg="red", bg="blue")
summarize_button.pack()

# Create a Scrollbar widget
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side="right", fill="y")

# Create a Text widget and configure it to display the summary
summary_text = tk.Text(window, font=("Arial", 18), bd=1, relief="sunken", wrap=tk.WORD, yscrollcommand=scrollbar.set)
summary_text.pack(pady=10)


# Run the main loop
window.mainloop()

