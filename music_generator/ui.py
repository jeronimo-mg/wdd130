import tkinter as tk
from tkinter import ttk, scrolledtext

from music_theory import Scale
from lyric_processor import process_lyrics
from melody_generator import MelodyGenerator
from chord_generator import ChordGenerator
from audio_player import AudioPlayer

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Generator")
        self.geometry("800x600")

        self.generated_music = None
        self.player = AudioPlayer()

        self._create_widgets()

    def _create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input Section ---
        input_frame = ttk.LabelFrame(main_frame, text="Input Lyrics", padding="10")
        input_frame.pack(fill=tk.X, pady=5)

        self.lyrics_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=5)
        self.lyrics_text.pack(fill=tk.X, expand=True)
        self.lyrics_text.insert(tk.END, "Enter your song lyrics here.")

        # --- Controls ---
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=5)

        self.generate_button = ttk.Button(controls_frame, text="Generate Music", command=self.generate_music)
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.play_button = ttk.Button(controls_frame, text="Play/Stop", command=self.play_stop_music, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=5)

        # --- Options (Placeholders) ---
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=5)

        # Accompaniment Style
        ttk.Label(options_frame, text="Accompaniment:").pack(side=tk.LEFT, padx=5)
        self.accompaniment_style = ttk.Combobox(options_frame, values=["Arpeggio", "Strumming"], state="readonly")
        self.accompaniment_style.pack(side=tk.LEFT, padx=5)
        self.accompaniment_style.set("Arpeggio")

        # Melody Instrument
        ttk.Label(options_frame, text="Melody Instrument:").pack(side=tk.LEFT, padx=5)
        self.melody_instrument = ttk.Combobox(options_frame, values=["Piano", "Sine Wave"], state="readonly")
        self.melody_instrument.pack(side=tk.LEFT, padx=5)
        self.melody_instrument.set("Sine Wave")

        # --- Output Section ---
        output_frame = ttk.LabelFrame(main_frame, text="Generated Music", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        cols = ("Measure", "Melody", "Chord")
        self.tree = ttk.Treeview(output_frame, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def generate_music(self):
        lyrics = self.lyrics_text.get("1.0", tk.END).strip()
        if not lyrics:
            return

        # --- Run the generation pipeline ---
        words, syllable_counts = process_lyrics(lyrics)
        scale = Scale('C', 'major')
        melody_gen = MelodyGenerator(scale)
        melody, measures = melody_gen.generate_melody(syllable_counts)
        chord_gen = ChordGenerator(scale)
        chord_progression = chord_gen.generate_chords(measures)

        self.generated_music = (measures, chord_progression)

        # --- Display the results ---
        # Clear previous results
        for i in self.tree.get_children():
            self.tree.delete(i)

        for i, measure in enumerate(measures):
            measure_notes = [note.name for note in measure]
            chord = chord_progression[i]
            self.tree.insert("", "end", values=(i + 1, f"{measure_notes}", f"{chord}"))

        self.play_button.config(state=tk.NORMAL)


    def play_stop_music(self):
        if self.generated_music:
            # Get the selected accompaniment style from the dropdown
            style = self.accompaniment_style.get()

            print(f"Play/Stop button clicked. Style: {style}")
            measures, chord_progression = self.generated_music

            # Pass the selected style to the player
            self.player.play_song(measures, chord_progression, accompaniment_style=style)


if __name__ == '__main__':
    app = App()
    app.mainloop()
