import os
from moviepy.editor import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import mimetypes
import random
import string

from moviepy.config import change_settings
change_settings({ "IMAGEMAGICK_BINARY": r"D:\\ProgramFiles\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, AudioFileClip, afx,CompositeAudioClip

# clip1 = VideoFileClip("one.mp4").subclip(10, 20).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)
# clip2 = VideoFileClip("two.mp4").subclip(10, 20).fx (vfx.fadein, 1).fx(vfx.fadeout, 1)
# clip3 = VideoFileClip ("one.mp4").subclip (20, 30).fx(vfx.fadein, 1).fx (vfx.fadeout, 1)
# clip4 = VideoFileClip("one.mp4").subclip(10, 20).fx(vfx.fadein, 1).fx(vfx.fadeout, 1)

# audio = AudioFileClip("Hymn for the Weekend.mp3").fx(afx.audio_fadein, 1).fx(afx.volumex, 0.1)

# combined = concatenate_videoclips([clip1, clip2, clip3, clip4])

# combined.audio = CompositeAudioClip([audio])
#------------------------------------------------------------------------------------------------------------------
# combined.write_videofile("Edit.mp4")

# os.chdir('../data/input')
# cur_path = os.path.dirname(os.path.abspath(__file__))
# print(cur_path)

# for root, dirs, files in os.walk (cur_path, topdown=False):
#     for name in files:
#         print(os.path.join(root, name))
#     for name in dirs:
#         print(os.path.join(root, name))

# clip = VideoFileClip("C:\Users\LUISA\OneDrive\Escritorio\Multimedia\Video_editor\data\input\one.mp4")
# w, h = clip.size
# duration= clip.duration
# fps = clip.fps

# print("Width x Height: ", w, "x", h)
# print("Duration: ", duration)
# print("FPS: ", fps)

class FileObject:
    def __init__(self, path, label, data_type):
        self.path = path
        self.label = label
        self.data_type = data_type

class VideoEditorGUI(tk.Frame) :
    def __init__(self, master):
        self.master=master
        tk.Frame.__init__(self, self.master)
        self.gui= self.configure_gui()
        self.widgets = self.create_widgets()
        self.importedObjects=[]
        
    def configure_gui(self): 
        self.master.geometry('1280x760')
    
    def create_widgets (self):
        importButoon = tk.Button(self.master, text="Import", font=("Helvatica", 18), padx=18, pady=5, fg="#FFF", bg="#3582e8", command=self.open_dialog) 
        importButoon.grid(sticky="W", column=0, row=0, padx=10, pady=10)

        processButton = tk.Button(self.master, text="Process", font=("Helvatica", 18), padx=18, pady=5, fg="#FFF", bg="#3582e8", command=self.processData) 
        processButton.grid(sticky="w", column=8, row=1, padx=18, pady=10)

        overlayEntry = tk. Entry(self.master, width=15, text="Title", font=("Helvatica", 18)) 
        overlayEntry.grid(sticky="W", column=8, row=2, padx=10, pady=10)

        return overlayEntry
    
    def open_dialog(self):
        self.master.filename=filedialog.askopenfilename(initialdir="/", title="Select Fiels", filetypes=[('Allfiles', '*.*')])
        
        if mimetypes.guess_type(self.master.filename)[0].startswith('video'):
            openFileLabel = tk.Label(self.master, anchor="e", justify=tk.LEFT, text="Location: " + self.master.filename + "Type. " + "Video", font=("Helvatica", 13))
            openFileLabel.grid(sticky="W", column=0, row=len(self.importedObjects) + 4, padx=10, pady=2) 
            file = FileObject(self.master.filename, openFileLabel, "video")
            self.importedObjects.append(file)
        else:
            openFileLabel = tk.Label(self.master, anchor="e", justify=tk.LEFT, text="Location: " + self.master.filename + "Type. " + "Audio", font=("Helvatica", 13))
            openFileLabel.grid(sticky="W", column=0, row=len(self.importedObjects) + 4, padx=10, pady=2) 
            file = FileObject(self.master.filename, openFileLabel, "audio")
            self.importedObjects.append(file)

    def get_random_string (self, lenght):
        letters=string.ascii_lowercase
        result_str = ''.join(random.choice (letters) for i in range(lenght))
        return result_str

    def processData(self):
        dir_name = filedialog.askdirectory()

        file_name_extension = "/" + self.get_random_string(8)
        video_name = dir_name + file_name_extension + "_video" + ".mp4"
        gif_name = dir_name + file_name_extension + "_gif" + ".gif"
        thumbnail_name = dir_name + file_name_extension + "_thumbnail"+ ".jpg"

        video_clip_found = None
        audio_clip_found = None
        for file in self.importedObjects:
            if(file.data_type == "video"):
                video_clip_found = file
            elif(file.data_type == "audio"):
                audio_clip_found = file
            
        if (video_clip_found and audio_clip_found):
            clip = VideoFileClip (video_clip_found.path)

            overlayEntry = self.widgets
            clip_overlay= TextClip (overlayEntry.get(), color="blue", font="Amiri-Bold",
                                kerning=5, fontsize=158).set_position("center").set_duration(15)
            
        frame = clip.get_frame(int(10))
        thumb_image = Image.fromarray(frame) 
        thumb_image.save(thumbnail_name)
        background_audio_clip = AudioFileClip (audio_clip_found.path) 
        bg_music = background_audio_clip.subclip(0, clip. duration)
        
        resized_clip = clip.resize(0.5)
        resized_clip.write_gif(gif_name) 
        # ffmpeg -i input.mp4 -vcodec h264 -acodac aad output.mp4 I

        clip_with_audio=clip.set_audio(bg_music)
        final_clip=CompositeVideoClip([clip_with_audio, clip_overlay]) 
        final_clip.write_videofile(video_name, codec='libx264', audio_codec='aac')

if __name__=='__main__':
    root= tk.Tk()
    root.title("Video Editor")

    main_app=VideoEditorGUI(root)
    root.mainloop()