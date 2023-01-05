import os
import pprint
import numpy as np
from pydub import AudioSegment
import speech_recognition as sr
from collections import namedtuple
from collections import defaultdict
from pyannote.audio import Pipeline
from distutils.errors import UnknownFileError

r = sr.Recognizer()

Splits = namedtuple('Splits',('start','stop'))
speakers_dict = defaultdict(list)
speaker_ranking_list = [0] * 10
repeat_ranking_list = [0] * 10
speed_ranking_list = [0] * 10
pitch_ranking_list = [0] * 10
pasues_ranking_list = [0] * 10


pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token="")



def devide_wav_by_speaker_and_intervals(wav_file):
    myaudio = AudioSegment.from_file(wav_file, "wav")
    
    for curr_speaker,curr_split_list in speakers_dict.items():     
        for curr_split in curr_split_list:
          
          if((curr_split.stop - curr_split.start) > 2):
            wav_file_part = myaudio[curr_split.start * 1000 : curr_split.stop * 1000]
            
            if not os.path.exists("speaker_{speaker_id}".format(speaker_id = int(curr_speaker))):
              os.makedirs("speaker_{speaker_id}".format(speaker_id = int(curr_speaker)))
            
            wav_file_part.export( "speaker_{speaker_id}/audio_chunk_{curr_interval}.wav".format(curr_interval = curr_split.stop, speaker_id = int(curr_speaker)), format="wav")      
    

def split_speaker_id(speaker):
  return speaker[-1]


def speaker_diaraztion():
  print("starting diaraztion.....")
  
  diarization = pipeline("test2.wav")
  
  for turn, _, speaker in diarization.itertracks(yield_label=True):
    interval = Splits(turn.start , turn.end)
    speakers_dict[split_speaker_id(speaker)].append(interval)
  
  os.system('cls||clear')
  print("done!")


#needs to be in a for loop probably
def get_speech_rate(file):
    # Load the WAV file
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    # Calculate the speech rate
    rate = sr.speech_rate(audio)
    
    #add the avarge calculation
    print(rate)


def repetative_analsys(file_path, speaker_id):
  current_interval = sr.AudioFile(file_path)
  with current_interval as source:
    audio = r.record(source)
  
    #audio_interval = AudioSegment.from_file(file_path, "wav")
    try:  
      text = r.recognize_google(audio)
    except Exception as e:
      return
  
    total_repeat_sum = 0
  #splited_text = text.split()
  #a dict to hold how much each word repeats
  word_counts = {}
  
  if(len(text) > 0):
      
    for word in text:
        # If the word is not yet in the dictionary, add it with a count of 1
      if word not in word_counts:
        word_counts[word] = 1
        # If the word is already in the dictionary, increment its count
      else:
        word_counts[word] += 1
      
    for curr_value in word_counts.values():
      if (curr_value >= 5):
        total_repeat_sum += 1
      
      if(total_repeat_sum >= 5):
        repeat_ranking_list[int(speaker_id)] += -1
      else:
        repeat_ranking_list[int(speaker_id)] += 1
        
        
def normalize_results(score_list):
  for index in range(len(score_list)):
    score_list[index] *= 0.01
  
  

 
 
#need to add next -> add features from other branch -> full test
def main():
  speaker_diaraztion()
  devide_wav_by_speaker_and_intervals("test2.wav")

  for curr_speaker in speakers_dict.keys():
    for filename in os.listdir(f"speaker_{int(curr_speaker)}"):
      
      f = os.path.join(f"speaker_{int(curr_speaker)}" ,filename)
      if os.path.isfile(f):
        repetative_analsys(f"speaker_{int(curr_speaker)}/{filename}", curr_speaker)
        
  normalize_results(repeat_ranking_list)
  
  os.system('cls||clear')

    
    
main()

print(repeat_ranking_list)