import pygame
import numpy as np
import time
import sys

# --- Pygame Initialization ---
try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    if pygame.mixer.get_init() is None:
        raise RuntimeError("Pygame mixer could not be initialized.")
    AUDIO_ENABLED = True
    print("Audio device found, audio enabled.")
except (pygame.error, RuntimeError) as e:
    AUDIO_ENABLED = False
    print(f"Warning: Could not initialize audio: {e}", file=sys.stderr)
    print("Running in dummy audio mode (no sound).", file=sys.stderr)

# --- Note and Sound Generation ---
NOTE_FREQUENCIES = {
    'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63,
    'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00,
    'A#': 466.16, 'B': 493.88
}

def get_frequency(note_name, octave=4):
    base_freq = NOTE_FREQUENCIES.get(note_name, 440.00)
    return base_freq * (2 ** (octave - 4))

def generate_sine_wave(frequency, duration_ms):
    if not AUDIO_ENABLED: return None
    sample_rate = pygame.mixer.get_init()[0]
    num_samples = int(sample_rate * duration_ms / 1000.0)
    buf = np.zeros((num_samples, 2), dtype=np.int16)
    max_sample = 2**15 - 1
    for i in range(num_samples):
        t = float(i) / sample_rate
        sine_val = np.sin(2 * np.pi * frequency * t)
        buf[i][0] = int(sine_val * max_sample)
        buf[i][1] = int(sine_val * max_sample)
    return pygame.sndarray.make_sound(buf)

# --- AudioPlayer Class ---
class AudioPlayer:
    def __init__(self):
        self.audio_enabled = AUDIO_ENABLED
        self.sounds = {}
        if self.audio_enabled:
            for name in NOTE_FREQUENCIES.keys():
                self.sounds[name] = generate_sine_wave(get_frequency(name), 1000) # Longer duration for flexibility

    def play_note(self, note_name, duration_sec, octave=4):
        if self.audio_enabled:
            freq = get_frequency(note_name, octave)
            sound = generate_sine_wave(freq, duration_sec * 1000)
            sound.play(maxtime=int(duration_sec * 1000))
        else:
            print(f"  (Playing note: {note_name})")

    def _play_strum(self, chord, duration_sec):
        if self.audio_enabled:
            for note_name in chord.notes:
                self.play_note(note_name, duration_sec, octave=3) # Accompaniment octave
        else:
            print(f"  (Strumming chord: {chord.root_note_name} {chord.chord_type})")

    def _play_arpeggio(self, chord, beats_per_measure, beat_duration):
        arpeggio_pattern = [chord.notes[0], chord.notes[1], chord.notes[2], chord.notes[1]]
        if len(chord.notes) < 3: # Handle diminished chords etc.
            arpeggio_pattern = [chord.notes[0], chord.notes[1], chord.notes[0], chord.notes[1]]

        if self.audio_enabled:
            for i in range(beats_per_measure):
                note_name = arpeggio_pattern[i % len(arpeggio_pattern)]
                self.play_note(note_name, beat_duration, octave=3)
                time.sleep(beat_duration)
        else:
            notes_to_play = [arpeggio_pattern[i % len(arpeggio_pattern)] for i in range(beats_per_measure)]
            print(f"  (Arpeggiating chord: {chord.root_note_name} {chord.chord_type} -> {notes_to_play})")
            time.sleep(beats_per_measure * beat_duration) # Simulate time passing

    def play_song(self, measures, chord_progression, tempo=120, accompaniment_style="Strumming"):
        beat_duration = 60.0 / tempo

        print(f"\nPlaying music with '{accompaniment_style}' accompaniment... (Press Ctrl+C to stop)")

        try:
            for i, measure in enumerate(measures):
                chord = chord_progression[i]

                # --- Accompaniment ---
                if accompaniment_style == "Arpeggio":
                    # Arpeggio is played in a separate thread/process in a real app
                    # Here, we'll block and play it before the melody of the measure
                    beats_in_measure = int(sum(n.duration for n in measure) / 0.25)
                    self._play_arpeggio(chord, beats_in_measure, beat_duration)
                    # Rewind time to play melody over it (conceptual)
                    # In this simple model, we play it before
                else: # Strumming
                    measure_duration = sum(n.duration for n in measure) * (60.0/tempo) * 4
                    self._play_strum(chord, measure_duration)

                # --- Melody ---
                # In a real player, melody and accompaniment would be mixed.
                # Here we play them sequentially for simplicity.
                if accompaniment_style != "Arpeggio": # Arpeggio already handles timing
                    for note in measure:
                        self.play_note(note.name, note.duration * (60.0/tempo) * 4)
                        time.sleep(note.duration * (60.0/tempo) * 4)

        except KeyboardInterrupt:
            if self.audio_enabled: pygame.mixer.stop()
            print("\nPlayback stopped.")
        finally:
            if self.audio_enabled: pygame.quit()

if __name__ == '__main__':
    from music_theory import Note, Chord, Scale
    player = AudioPlayer()
    c_major_scale = Scale('C', 'major')
    measures = [[Note('C', duration=0.25), Note('E', duration=0.25), Note('G', duration=0.5)]]
    progression = [c_major_scale.diatonic_chords[0]]

    print("\n--- Testing Strumming Accompaniment ---")
    player.play_song(measures, progression, accompaniment_style="Strumming")

    print("\n--- Testing Arpeggio Accompaniment ---")
    player.play_song(measures, progression, accompaniment_style="Arpeggio")

    print("\n--- Test Complete ---")
