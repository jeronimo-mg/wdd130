import random
from music_theory import Scale, Chord

# Common chord progressions in a major key, represented by scale degrees (1-based)
COMMON_PROGRESSIONS = [
    [1, 5, 6, 4],  # I-V-vi-IV (very common)
    [1, 4, 5, 1],  # I-IV-V-I (classic)
    [1, 6, 4, 5],  # I-vi-IV-V ("50s progression")
    [2, 5, 1, 4]   # ii-V-I-IV (jazz-influenced)
]

class ChordGenerator:
    def __init__(self, scale):
        self.scale = scale
        self.diatonic_chords = scale.diatonic_chords
        # Select a progression to follow for this song
        self.progression_template = random.choice(COMMON_PROGRESSIONS)

    def generate_chords(self, measures):
        progression = []
        num_measures = len(measures)
        template_len = len(self.progression_template)

        for i in range(num_measures):
            # --- Final Measure Rule ---
            if i == num_measures - 1:
                progression.append(self.scale.get_chord_by_degree(1)) # Always end on tonic
                continue

            # --- Get suggested chord from the template ---
            template_degree = self.progression_template[i % template_len]
            suggested_chord = self.scale.get_chord_by_degree(template_degree)

            # --- Find best chord based on melody and suggestion ---
            best_chord = self._find_best_chord(measures[i], suggested_chord)
            progression.append(best_chord)

        return progression

    def _find_best_chord(self, measure, suggested_chord):
        """
        Finds the best chord for a measure.
        It prioritizes the suggested chord from the progression template,
        but will consider other diatonic chords if they are a much better
        fit for the melody.
        """
        measure_note_names = {note.name for note in measure}
        best_fit_chord = suggested_chord

        # Score the suggested chord
        suggested_chord_notes = set(suggested_chord.notes)
        max_score = len(measure_note_names.intersection(suggested_chord_notes))

        # Check if another diatonic chord is a significantly better fit
        for chord in self.diatonic_chords:
            if chord == suggested_chord:
                continue

            chord_notes = set(chord.notes)
            score = len(measure_note_names.intersection(chord_notes))

            # A different chord is only chosen if it's a much better fit (e.g., matches 2+ more notes)
            if score > max_score + 1:
                max_score = score
                best_fit_chord = chord

        return best_fit_chord

if __name__ == '__main__':
    from music_theory import Note

    c_major_scale = Scale('C', 'major')
    chord_gen = ChordGenerator(c_major_scale)

    # Sample measures
    measures = [
        [Note('C'), Note('G'), Note('E'), Note('G')],
        [Note('A'), Note('B'), Note('G'), Note('A')],
        [Note('D'), Note('F'), Note('E'), Note('D')],
        [Note('C'), Note('C'), Note('C')]
    ]

    print("--- Refined Chord Generation Test ---")
    print(f"Scale: {c_major_scale.root_note_name} {c_major_scale.scale_type}")
    prog_degrees = [str(d) for d in chord_gen.progression_template]
    print(f"Using Progression Template (degrees): {'-'.join(prog_degrees)}")

    chord_progression = chord_gen.generate_chords(measures)

    print("\n--- Results ---")
    for i, measure in enumerate(measures):
        measure_notes = [note.name for note in measure]
        print(f"Measure {i+1} (Melody: {measure_notes}) -> Chord: {chord_progression[i]}")
