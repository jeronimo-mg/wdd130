import random
from music_theory import Note, Scale

class MelodyGenerator:
    def __init__(self, scale):
        self.scale = scale
        self.motif = self._create_motif()

    def _create_motif(self, length=3):
        """Creates a short melodic motif as a sequence of scale steps."""
        # e.g., [+1, -2] means "go up one step in the scale, then down two steps"
        return [random.choice([-2, -1, 1, 2]) for _ in range(length)]

    def generate_melody(self, syllable_counts):
        total_syllables = sum(syllable_counts)
        scale_notes = self.scale.notes

        measures = []
        current_measure_notes = []
        current_measure_duration = 0.0

        # Start the melody on the root or the fifth for stability
        current_scale_degree = random.choice([0, 4])
        motif_index = 0

        for i in range(total_syllables):
            # --- Rhythmic Variety ---
            # Decide duration: 80% chance of a quarter note, 20% for two eighth notes
            if random.random() < 0.8:
                notes_for_syllable = [(current_scale_degree, 0.25)] # (degree, duration)
            else:
                # Two eighth notes
                notes_for_syllable = [(current_scale_degree, 0.125), (current_scale_degree, 0.125)]

            # --- Melodic Contour (Motif-based) ---
            # Apply the next step from the motif
            current_scale_degree += self.motif[motif_index]
            # Keep the note within the scale bounds (7 notes)
            current_scale_degree %= len(scale_notes)
            motif_index = (motif_index + 1) % len(self.motif)

            # --- Add notes to measure ---
            for degree, duration in notes_for_syllable:
                if current_measure_duration + duration > 1.0: # 1.0 = whole note (4/4 measure)
                    # End the current measure and start a new one
                    measures.append(current_measure_notes)
                    current_measure_notes = []
                    current_measure_duration = 0.0

                note_name = scale_notes[degree]
                current_measure_notes.append(Note(note_name, duration=duration))
                current_measure_duration += duration

        # Add any remaining notes
        if current_measure_notes:
            measures.append(current_measure_notes)

        # --- Final Measure Rules ---
        if measures:
            # Ensure the last note is the tonic with a long duration
            last_measure = measures[-1]
            tonic_note = Note(self.scale.root_note_name, duration=0.25)

            # If last measure has room, add the tonic. Otherwise, replace the last note.
            last_measure_dur = sum(n.duration for n in last_measure)
            if last_measure_dur < 1.0:
                 last_measure.append(tonic_note)
            else:
                last_measure[-1] = tonic_note

        melody = [note for measure in measures for note in measure]
        return melody, measures

if __name__ == '__main__':
    # Test the refined melody generator
    c_major_scale = Scale('C', 'major')
    syllables = [1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2] # Some test syllables

    melody_gen = MelodyGenerator(c_major_scale)
    print(f"Generated Motif (scale steps): {melody_gen.motif}")

    melody, measures = melody_gen.generate_melody(syllables)

    print("\n--- Refined Melody Generation Test ---")
    for i, measure in enumerate(measures):
        print(f"  Measure {i+1}: {measure}")
