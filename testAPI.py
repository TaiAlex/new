import glob
import os.path
import pydub
import speech_recognition as sr
import pyaudio
from pydub.utils import which
import pandas as pd
import json

def split_list_answer(text_path, answer):
    col_answer = []
    col_index = []
    result = []
    print(answer)
    with open(text_path,"r", encoding="UTF-8") as f:
        ot = f.read()       #original text
    for j in ot.split('bắt đầu'):
        answer1 = j.split('thời')[0].strip()[-1]
        col_answer.append(answer1.upper())
    col_answer.pop(0)
    print(col_answer)
    for i in range(len(col_answer)):
        col_index.append(f'Câu {i + 1}')
    for i in range(len(col_answer)):
        if col_answer[i] == answer[i]:
            result.append('True')
        else:
            result.append('False')
    df = pd.DataFrame(zip(col_answer, answer, result), index = col_index, columns=['Answer of student', 'Answer', 'Result'])
    print(df)
    with open(text_path + '.json', 'w') as t:
        json1 = df.to_json(t, force_ascii=False)
    print(json.dumps(json1, indent=3))
    # dfj = json.loads(df.to_json(orient='table',index=False))
    print(df.to_html())
    # return json1
    return df.to_html(justify='center')

def find_path():
    folder_path = r'/home/ubuntu/new/upload/*'
    sub_folders = glob.glob(folder_path)
    the_lastest_subfolder = max(sub_folders, key=os.path.getctime)
    files = glob.glob(the_lastest_subfolder + '\*')
    the_last_file = max(files, key=os.path.getctime)
    print(the_last_file)
    return the_last_file

def mp3_to_wav(file_path):
    type = file_path.split('.')[1]
    if type == 'mp3':
        mp3_path = str(file_path)
        wav_path = str(file_path.split('.')[0] + '.wav')
        sound = pydub.AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")
        print(wav_path)
        return wav_path
    elif type == 'm4a':
        m4a_path = str(file_path)
        wav_path = str(file_path.split('.')[0] + '.wav')
        sound = pydub.AudioSegment.from_file(m4a_path, format='m4a')
        sound.export(wav_path, format="wav")
        print(wav_path)
        return wav_path
    elif type == 'wav':
        return file_path
    else:
        return False
    
def wav_to_text(wav):
    r = sr.Recognizer()
    with sr.AudioFile(wav) as source:
        audio = r.record(source)
        text = r.recognize_google(audio, language = "vi-VI")
        with open('log.txt', mode = 'a', encoding = 'UTF-8', errors = 'ignore') as data:
            data.write(str(text))
            
def wav_to_txt(wav):
    text_path = wav.split('.')[0] + '.txt'
    print(text_path)
    r = sr.Recognizer()
    with sr.AudioFile(wav) as source:
        audio = r.record(source)
        text = r.recognize_google(audio, language = "vi-VI")
        with open(text_path, mode = 'a', encoding = 'UTF-8', errors = 'ignore') as data:
            data.write(str(text))
        return text_path


    
# wav_to_txt(r'E:/04-02-2023/folder1/upload/audio/audio.mp3')
