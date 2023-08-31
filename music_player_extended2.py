import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import random
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Music Player")
        self.window.configure(bg="white")

        self.playlist = []
        self.current_song_index = 0
        self.shuffle_mode = False
        self.repeat_mode = False

        self.create_gui()

        pygame.mixer.init()

    def create_gui(self):
        self.play_button = self.create_styled_button("Play", self.play_music)
        self.pause_button = self.create_styled_button("Pause", self.pause_music)
        self.stop_button = self.create_styled_button("Stop", self.stop_music)
        self.next_button = self.create_styled_button("Next", self.next_song)
        self.previous_button = self.create_styled_button("Previous", self.previous_song)
        self.select_folder_button = self.create_styled_button("Select Folder", self.select_folder)
        self.shuffle_button = self.create_styled_button("Shuffle", self.toggle_shuffle)
        self.repeat_button = self.create_styled_button("Repeat", self.toggle_repeat)
        self.search_button = self.create_styled_button("Search", self.search_song)

        self.volume_scale = tk.Scale(self.window, from_=0, to=100, orient="horizontal", label="Volume", command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack()

        self.search_entry = tk.Entry(self.window)
        self.search_entry.pack()

        self.album_art_label = tk.Label(self.window)
        self.album_art_label.pack()

        self.song_info_label = tk.Label(self.window, text="", font=("Helvetica", 12))
        self.song_info_label.pack()

        self.playlist_box = tk.Listbox(self.window, bg="#f0f0f0")
        self.playlist_box.pack()

        self.playlist_box.bind("<<ListboxSelect>>", self.on_song_select)

    def create_styled_button(self, text, command):
        button = tk.Button(self.window, text=text, command=command, bg="#007acc", fg="white", relief="flat")
        button.config(font=("Helvetica", 12))
        button.pack()
        return button

    def update_buttons(self):
        self.shuffle_button.config(bg="#007acc" if not self.shuffle_mode else "#a0a0a0")
        self.repeat_button.config(bg="#007acc" if not self.repeat_mode else "#a0a0a0")

    def play_music(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_song_index])
            pygame.mixer.music.play()
            self.update_song_info()

    def pause_music(self):
        pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()

    def next_song(self):
        if self.shuffle_mode:
            self.current_song_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
        self.play_music()

    def previous_song(self):
        self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
        self.play_music()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.load_songs(folder)

    def load_songs(self, folder):
        self.playlist = []
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(('.mp3', '.ogg', '.wav')):
                    song_path = os.path.join(root, file)
                    self.playlist.append(song_path)
        self.update_playlist()

    def update_playlist(self):
        self.playlist_box.delete(0, tk.END)
        for song in self.playlist:
            self.playlist_box.insert(tk.END, os.path.basename(song))
        self.update_album_art()

    def on_song_select(self, event):
        selected_index = self.playlist_box.curselection()
        if selected_index:
            self.current_song_index = selected_index[0]
            self.play_music()

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        self.update_buttons()

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        self.update_buttons()

    def set_volume(self, value):
        pygame.mixer.music.set_volume(int(value) / 100)

    def search_song(self):
        query = self.search_entry.get().lower()
        found_indices = [i for i, song in enumerate(self.playlist) if query in song.lower()]
        if found_indices:
            self.current_song_index = found_indices[0]
            self.play_music()
        else:
            messagebox.showinfo("Search Result", "No matching songs found.")

    def update_album_art(self):
        if self.playlist:
            song_path = self.playlist[self.current_song_index]
            image_path = os.path.splitext(song_path)[0] + ".jpg"
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((200, 200), Image.ANTIALIAS)
                album_art = ImageTk.PhotoImage(img)
                self.album_art_label.config(image=album_art)
                self.album_art_label.image = album_art
            else:
                self.album_art_label.config(image="")
                self.album_art_label.image = None

    def update_song_info(self):
        if self.playlist:
            song_path = self.playlist[self.current_song_index]
            song_name = os.path.basename(song_path)
            self.song_info_label.config(text=song_name)

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("500x600")
    app = MusicPlayer(window)
    window.mainloop()
