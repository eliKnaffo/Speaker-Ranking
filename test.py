import os
import pprint
import numpy as np
from pydub import AudioSegment
from collections import namedtuple
from collections import defaultdict
from pyannote.audio import Pipeline


Splits = namedtuple('Splits',('start','stop'))
speakers_dict = defaultdict(list)



pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token="")



def devide_wav_by_speaker_and_intervals(wav_file, speaker_id):
    myaudio = AudioSegment.from_file(wav_file, "wav")
    intervals_list = []
    
    for curr_speaker,Splits in speakers_dict.items():
      print(curr_speaker)
      if(curr_speaker == speaker_id):
        print(Splits.start)
        wav_file_part = myaudio[Splits.start:Splits.end]
        intervals_list.append(wav_file_part)
    
    return intervals_list
      



def split_speaker_id(speaker):
  return speaker[-1]


def speaker_diaraztion():
  print("starting diaraztion.....")
  
  diarization = pipeline("test.wav")
  
  for turn, _, speaker in diarization.itertracks(yield_label=True):
    interval = Splits(turn.start , turn.end)
    speakers_dict[split_speaker_id(speaker)].append(interval)
  
  os.system('cls||clear')
  print("done!")



def avg_speed_of_speaker(speaker_id):
  #get speaker intervals
  speaker_intervals = speakers_dict.get(speaker_id)
  #check speed in each interval
  #avarge the intervals
  #save to speaker speeds dict
  print(speaker_intervals)
  
  
def main():
    speaker_diaraztion()
    test_list = devide_wav_by_speaker_and_intervals("test.wav",1)
    
    print(test_list)
    
    
    
main()

"""
# Create an array to hold the pitch of each speaker's speech
speaker_pitches = []
for i in range(n_speakers):
  speaker_pitches.append(0)

# Calculate the pitch of each speaker's speech
for i, cluster_id in enumerate(cluster_ids):
  # Calculate the pitch of speech as the average frequency of the audio segment
  pitch = np.mean(librosa.pitch_tuning(audio[i]))
  speaker_pitches[cluster_id] += pitch

# Create an array to hold the repetitiveness of each speaker's speech
speaker_repetitiveness = []
for i in range(n_speakers):
  speaker_repetitiveness.append(0)

# Calculate the repetitiveness of each speaker's speech
for i, cluster_id in enumerate(cluster_ids):
  # Calculate the repetitiveness of speech as the average repetition rate of the audio segment
  repetitiveness = np.mean(librosa.beat.tempo(audio[i], sr=sr))
  speaker_repetitiveness[cluster_id] += repetitiveness

# Create an array to hold the pauses of each speaker's speech
speaker_pauses = []
for i in range(n_speakers):
  speaker_pauses.append(0)

# Calculate the pauses of each speaker's speech
for i, cluster_id in enumerate(cluster_ids):
  # Calculate the pauses in speech as the number of silence segments in the audio
  pauses = len(librosa.effects.split(audio[i], top_db=20))
  speaker_pauses[cluster_id] += pauses

# Create an array to hold the scores for each speaker
speaker_scores = []
for i in range(n_speakers):
  speaker_scores.append(0)

# Calculate the overall score for each speaker
for i in range(n_speakers):
  score = speaker_speeds[i] + speaker_pitches[i] - speaker_repetitiveness[i] - speaker_pauses[i]
  speaker_scores[i] = score



print(speaker_scores)

"""