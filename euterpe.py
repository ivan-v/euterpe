import random

# TODO:
# write notation for notes
# convert reasonable notation to pysynth(?)
# 

# Notation:
# First num dictates the first tone, subsequent tones are difference from the 
# first note


# Modes are recorded in relative pitches to the tonic/root note, 0.
Modes = {
  "Ionian":     [0, 2, 4, 5, 7, 9, 11],
  "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
  "Lydian ":    [0, 2, 4, 6, 7, 9, 11],
  "Dorian":     [0, 2, 3, 5, 7, 9, 10],
  "Phrygian":   [0, 1, 3, 5, 7, 8, 10],
  "Aeolian":    [0, 2, 3, 5, 7, 8, 10],
  # TODO: make non-8 note scales work properly
  "Pentatonic": [0, 2, 4, 6, 9],
  "Blues":      [0, 3, 5, 6, 7, 10],

}

# Keys are recorded how/which tones (selected by the modes) have to be modified
Keys = {
  "C":  [0, 0, 0, 0, 0, 0, 0],
  "G":  [0, 0, 0, 0, 0, 0, 1], # [shift f up]
  "D":  [0, 1, 0, 0, 0, 1, 0], # [shift f, c up]
  "A":  [0, 0, 1, 0, 0, 1, 1], # [shift f, c, g up]
  "E":  [0, 1, 1, 0, 0, 1, 1], # [shift f, c, g, d up]
  "B":  [0, 1, 1, 0, 1, 1, 1], # [shift f, c, g, d, a up]
  "Fs": [1, 1, 1, 0, 1, 1, 1], # [shift f, c, g, d, a, e up]
  "Cs": [1, 1, 1, 1, 1, 1, 1], # [shift f, c, g, d, a, e, b up]
  "F":  [0, 0, 0, -1, 0, 0, 0], # [shift b down]
  "Bb": [-1, 0, 0, -1, 0, 0, 0], # [shift b, e down]
  "Eb": [-1, 0, 0, -1, -1, 0, 0], # [shift b, e, a down]
  "Ab": [-1, -1, 0, -1, -1, 0, 0], # [shift b, e, a, d down]
  "Db": [-1, -1, 0, -1, -1, -1, 0], # [shift b, e, a, d, g down]
  "Gb": [-1, -1, -1, -1, -1, -1, 0], # [shift b, e, a, d, g, c down]
  "Cb": [-1, -1, -1, -1, -1, -1, -1] # [shift b, e, a, d, g, c, f down] 
}

def apply_key(mode, key):
  modulo = [0, 0, 0, 0, 0, 0, 0]
  for i in range(len(Keys[key])):
    modulo[i] = Modes[mode][i] + Keys[key][i]
  return (str(key + " " + mode), modulo)


def grow_chord_progression(progression):
  x = progression
  root = x[0]
  if root == 0:
    options = [3, 4, 6]
  elif root == 4 or root == 6:
    options = [1, 3]
  elif root == 1:
    options = [3, 5]
  elif root == 3 and len(x) > 2:
    options = [0, 5]
  elif root == 3:
    options = [5]
  elif root == 5:
    options = [0, 2]
  else:
    options = [0]
  return [random.choice(options)] + progression


def generate_chord_progression():
  progression = []
  progression.append(0)
  progression = grow_chord_progression(progression)
  while progression[0] is not 0:
    progression = grow_chord_progression(progression)
  return progression

# Sequences, unlike modulos/scales, use scale degrees instead of tone pitches.
# i.e., [0, 1, 2, 3, 4, 5, 6, 7] for typical Greek modes

# Returns the reverse of the sequence
def retrograde(sequence):
  return sequence[::-1]

# Returns the inverse (centered around the tonic) of the sequence
def invert(sequence):
  x = []
  for i in range(len(sequence)):
    x.extend([8 - sequence[i]])
  return x

def apply_mode_to_progression(progression, mode):
	new_progression = []
	for tone in progression:
		new_progression.append(tone)
	for i in range(len(new_progression)):
		new_progression[i] = mode[1][progression[i]]
	return new_progression

def convert_progression_to_etuerpea_string(progression, root, mode):
	s = ""
	for i in range(len(progression)):
		note = progression[i]
		if mode.index(note) < 5:
			third = mode[mode.index(note)+2]
		else:
			third = mode[mode.index(note)-4] + 12
		if mode.index(note) < 3:
			fifth = mode[mode.index(note)+4]
		else:
			fifth = mode[mode.index(note)-2] + 12
		s += ("(note qn " + str(root+note) + " :=: note qn " + str(root+third) 
			+ " :=: note qn "  + str(root+fifth)) + ")"
		if i < len(progression)-1:
			diff  = mode.index(progression[i+1]) - mode.index(note)
			if diff == 2 or diff == -2:
				step = mode[mode.index(note)+int(diff/2)]
				s += " :+: note hn " + str(root+step*int(diff/2))
			elif diff == 1 or diff == -1:
				s += " :+: note hn " + str(root+note)
			else:
				first_step  = mode[mode.index(note) + int(diff/3)] 
				second_step = mode[mode.index(progression[i+1]) - int(diff/3)]
				s += " :+: note qn " + str(root+first_step) + " :+: note qn " + str(root+second_step)
		if i <= len(progression)-2:
			if random.randint(1, 5) == 1:
				s += " :+: rest (1 % 4)"
			s += " :+: "
	return s

# TO NOTE:
# Ionian B is BoTW marimba ambient exploration


# TESTS
print(generate_chord_progression())
print(apply_key("Ionian", "C"))
sequence = generate_chord_progression()
# print(invert(sequence))
print(sequence)
a = apply_mode_to_progression(sequence, apply_key("Aeolian", "Ab"))
print(a)
print(convert_progression_to_etuerpea_string(a, 60, apply_key("Aeolian", "Ab")[1]))