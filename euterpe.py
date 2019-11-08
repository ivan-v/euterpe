import random

# TODO:
# write notation for notes
# convert reasonable notation to pysynth(?)
# 

# Notation:
# First num dictates the first tone, subsequent tones are difference from the 
# first note

Modes = {
  "Ionian":     [0, 2, 4, 5, 7, 9, 11],
  "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
  "Lydian ":    [0, 2, 4, 6, 7, 9, 11],
  "Dorian":     [0, 2, 3, 5, 7, 9, 10],
  "Phrygian":   [0, 1, 3, 5, 7, 8, 10],
  "Aeolian":    [0, 2, 3, 5, 7, 8, 10]
}

Keys = {
  "C": [0, 0, 0, 0, 0, 0, 0],
  "G": [0, 0, 0, 0, 0, 0, 1], # [shift f up]
  "D": [0, 1, 0, 0, 0, 1, 0], # [shift f, c up]
  "A": [0, 0, 1, 0, 0, 1, 1], # [shift f, c, g up]
  "E": [0, 1, 1, 0, 0, 1, 1], # [shift f, c, g, d up]
  "B": [0, 1, 1, 0, 1, 1, 1], # [shift f, c, g, d, a up]
  "Fs": [1, 1, 1, 0, 1, 1, 1], # [shift f, c, g, d, a, e up]
  "Cs": [1, 1, 1, 1, 1, 1, 1], # [shift f, c, g, d, a, e, b up]
  "F ": [0, 0, 0, -1, 0, 0, 0], # [shift b down]
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
  mode = {str(key + " " + mode): modulo}
  return mode


def grow_chord_progression(progression):
  root = progression[0]
  if root == 0:
    options = [3, 4, 6]
  elif root == 4 or root == 6:
    options = [1, 3]
  elif root == 1:
    options = [3, 5]
  elif root == 3 and len(progression) > 2:
    options = [0, 5]
  elif root == 3:
    options = [5]
  elif root == 5:
    options = [0, 2]
  else:
    options = [0]
  return progression.insert(0, options[random.randint(0, len(options)-1)])


def generate_chord_progression():
  progression = []
  progression.append(0)
  # gotta be a better do-while way to do this
  grow_chord_progression(progression)
  while progression[0] is not 0:
    grow_chord_progression(progression)
  return progression

print(generate_chord_progression())
print(apply_key("Ionian", "C"))