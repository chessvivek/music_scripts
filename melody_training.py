import numpy as np
from scipy.io.wavfile import write
from playsound import playsound as ps

samplerate = 44100

def get_wave(freq, duration=0.5):
    '''
    Function takes the "frequecy" and "time_duration" for a wave 
    as the input and returns a "numpy array" of values at all points 
    in time
    '''
    
    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave

def get_piano_notes():
    '''
    Returns a dict object for all the piano 
    note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    # Frequency of Note C4
    base_freq = 261.63
    
    note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
    
    return note_freqs

def get_song_data(music_notes):
    '''
    Function to concatenate all the waves (notes)
    '''
    note_freqs = get_piano_notes() # Function that we made earlier
    song = [get_wave(note_freqs[note]) for note in music_notes]
    song = np.concatenate(song)
    return song

def is_separated(num_choice, separation):
    if len(num_choice) == 0:
        return False

    for i in np.arange(len(num_choice)):
        for j in np.arange(i + 1, len(num_choice)):
            if np.abs(num_choice[j] - num_choice[i]) < separation:
                return False
    
    return True

piano_notes = np.array(list(get_piano_notes()))
print("Scale: ", piano_notes)

num_notes = input("Enter the number of notes in melody: ")
# do_notes_repeat = True if input("Do notes repeat? ")[0] == 'y' else False
do_notes_repeat = False
print("Guess the melody shape!")

min_separation = 2
num_choice = []

while not is_separated(num_choice, min_separation): 
    num_choice = np.random.choice(len(piano_notes), int(num_notes), replace=do_notes_repeat)
    
notes_choice = piano_notes[num_choice]
data = get_song_data(notes_choice)
data = data * (16300/np.max(data))

write('melody.wav', samplerate, data.astype(np.int16))
ps('melody.wav')

while (len(input("Press enter to show notes or any other key to repeat: ")) > 0):
    ps('melody.wav')

print("notes: ", notes_choice)
print("order: ", num_choice)
