NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SCALE_INTERVALS = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10]
}
CHORD_INTERVALS = {
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    'diminished': [0, 3, 6],
    'dominant7th': [0, 4, 7, 10]
}

class Note:
    def __init__(self, name, octave=4, duration=0.25):
        # duration is in fractions of a whole note (e.g., 0.25 = quarter note)
        self.name = name
        self.octave = octave
        self.duration = duration
        self.pitch = NOTES.index(name)

    def __repr__(self):
        return f"Note({self.name}{self.octave}, dur={self.duration})"

class Chord:
    def __init__(self, root_note_name, chord_type='major'):
        self.root_note_name = root_note_name
        self.chord_type = chord_type
        self.notes = self._build_chord()

    def _build_chord(self):
        root_note_index = NOTES.index(self.root_note_name)
        chord_notes = []
        intervals = CHORD_INTERVALS.get(self.chord_type, CHORD_INTERVALS['major'])
        for interval in intervals:
            note_index = (root_note_index + interval) % 12
            chord_notes.append(NOTES[note_index])
        return chord_notes

    def __repr__(self):
        return f"Chord({self.root_note_name} {self.chord_type})"

class Scale:
    def __init__(self, root_note_name, scale_type='major'):
        self.root_note_name = root_note_name
        self.scale_type = scale_type
        self.notes = self._build_scale()
        self.diatonic_chords = self._generate_diatonic_chords()

    def _build_scale(self):
        root_note_index = NOTES.index(self.root_note_name)
        scale_notes = []
        for interval in SCALE_INTERVALS[self.scale_type]:
            note_index = (root_note_index + interval) % 12
            scale_notes.append(NOTES[note_index])
        return scale_notes

    def _generate_diatonic_chords(self):
        chords = []
        if self.scale_type == 'major':
            qualities = ['major', 'minor', 'minor', 'major', 'major', 'minor', 'diminished']
            for i, note_name in enumerate(self.notes):
                chords.append(Chord(note_name, qualities[i]))
        return chords

    def get_note(self, degree):
        return self.notes[degree - 1]

    def get_chord_by_degree(self, degree):
        # Degree is 1-based, so adjust for 0-based list index
        return self.diatonic_chords[degree - 1]

    def __repr__(self):
        return f"Scale({self.root_note_name} {self.scale_type})"
