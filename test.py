import os
import pprint
import numpy as np
from pydub import AudioSegment
import speech_recognition as sr
from collections import namedtuple
from collections import defaultdict
from pyannote.audio import Pipeline


Splits = namedtuple('Splits',('start','stop'))
speakers_dict = defaultdict(list)
speaker_ranking_list = []



pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token="")



def devide_wav_by_speaker_and_intervals(wav_file, speaker_id):
    myaudio = AudioSegment.from_file(wav_file, "wav")
    
    for curr_speaker,curr_split_list in speakers_dict.items():
      
      if(int(curr_speaker) == speaker_id):     
        for curr_split in curr_split_list:
          wav_file_part = myaudio[curr_split.start : curr_split.stop]
          #need to add formating so the export is dynamic
          wav_file_part.export( "first_speaker/audio_chunk_{}.wav".format(curr_split.stop), format="wav")      
    
    
      



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


#needs to be in a for loop probably
def get_speech_rate(interval):
    # Load the WAV file
    r = sr.Recognizer()
    with sr.AudioFile(interval) as source:
        audio = r.record(source)
    # Calculate the speech rate
    rate = sr.speech_rate(audio)
    return rate


def speaker_rank_list_init():
    for speaker_id in len(speakers_dict.keys()):
      #init the ranking score to 0
      speaker_ranking_list[speaker_id] = 0
 
 
#need to add next -> format how the files are saved -> how to iterate over those files by speaker for each feature.  
def main():
    speaker_diaraztion()
    speaker_rank_list_init()
    for speaker_id in len(speakers_dict.keys()):
      devide_wav_by_speaker_and_intervals("test.wav",speaker_id)
    
    
    
main()
