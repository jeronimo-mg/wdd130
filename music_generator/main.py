import tkinter as tk

# --- Main Application Logic ---

def run_cli():
    """Runs the application as a command-line tool."""
    from music_theory import Scale
    from lyric_processor import process_lyrics
    from melody_generator import MelodyGenerator
    from chord_generator import ChordGenerator
    from audio_player import AudioPlayer

    print("--- Running in Command-Line Interface (CLI) mode ---")

    # 1. Define sample lyrics
    lyrics = "The quick brown fox jumps over the lazy dog."
    print(f"Lyrics: {lyrics}")

    # 2. Process the lyrics
    words, syllable_counts = process_lyrics(lyrics)
    print(f"Syllable counts: {syllable_counts}\n")

    # 3. Create a scale
    scale = Scale('C', 'major')
    print(f"Using scale: {scale.root_note_name} {scale.scale_type}")

    # 4. Generate a melody
    melody_gen = MelodyGenerator(scale)
    melody, measures = melody_gen.generate_melody(syllable_counts)

    # 5. Generate a chord progression
    chord_gen = ChordGenerator(scale)
    chord_progression = chord_gen.generate_chords(measures)

    # 6. Print the generated music structure
    print("\n--- Generated Music Structure ---")
    for i, measure in enumerate(measures):
        measure_notes = [note.name for note in measure]
        chord = chord_progression[i]
        print(f"  Measure {i+1}: Melody: {measure_notes}, Chord: {chord}")

    # 7. Play the generated music
    print("\n--- Audio Playback ---")
    player = AudioPlayer()
    player.play_song(measures, chord_progression, tempo=120)

    print("\n--- Program Finished ---")


def main():
    """
    Launches the application. Tries to launch the GUI, but falls back
    to a command-line interface if a display is not available.
    """
    try:
        # Attempt to import and run the GUI
        from ui import App
        app = App()
        app.mainloop()
    except tk.TclError as e:
        if "no display name" in str(e):
            print("No display environment found. Falling back to CLI mode.")
            run_cli()
        else:
            raise

if __name__ == "__main__":
    main()
