
import os
from google.cloud import speech
import io

import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/secret.json'


# ファイルを読み込んでテキスト化する
def transcribe(content, lang = 'English') -> str:

    lang_code = {
        'English': 'en-US',
        'Japanese': 'ja-JP'
    }

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content = content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        language_code = lang_code[lang],
    )
    
    response = client.recognize(config = config, audio = audio)

    for result in response.results:
        st.write(result.alternatives[0].transcript)



# streamlitへの書き出し
st.title('文字起こしアプリ')
st.header('Overview')
st.write('This is a transcription application that uses Google Cloud Speech-to-Text. The link is below.')
st.markdown('<a href="https://cloud.google.com/speech-to-text?hl-ja">Cloud Speech-to-Text</a>', unsafe_allow_html=True)

upload_file = st.file_uploader('Upload File', type=['mp3', 'wav'])
if upload_file is not None:
    content = upload_file.read()
    st.subheader('File Details')
    file_details = {'FileName': upload_file.name, 'FileType': upload_file.type, 'FileSize': upload_file.size}
    st.write(file_details)
    st.subheader('Audio Playback')
    st.audio(content)
    
    st.subheader('Chose Language')
    option = st.selectbox('Select a language for translation', ('English', 'Japanese'))
    st.write('Language selected: ', option)
    
    st.write('文字起こし')
    if st.button('開始'):
        comment = st.empty()
        comment.write('変換中です')
        transcribe(content, lang = option)
        comment.write('完了しました')