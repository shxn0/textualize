import os
from google.cloud import speech
import io

import streamlit as st
import pandas as pd

from word import Word


def main():

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/secret.json'

    # ファイルを読み込んでテキスト化する
    def transcribe_file(content, lang = 'English') -> str:

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
            return result.alternatives[0].transcript
        
    
    # 音声認識したテキストから単語リストを生成
    def generate_word_list() -> list[str]:
        text = st.session_state.result

        words = []
        for index, word in enumerate(text.split(' ')):
            words.append(Word(index = index, name = word))
        return words


    # 入力値をもとに単語を検索をする
    def search(input_words: list[str]) -> list[Word]:
        words = generate_word_list()
        
        result = []
        for target in input_words:
            for w in words:
                if(w.name == target):
                    result.append(w)
        return result
    
    
    # 検索文字列の前後5単語を抽出する
    def extract_words(matched_words) -> list[list[Word]]:
        lumps = []
        for word in matched_words:
            lumps.append(generate_word_list()[word.index-5:word.index+6])
        return lumps


    # Streamlitへの書き出し
    st.title('文字起こしアプリ')
    st.header('Overview')
    st.write('This is a transcription application that uses Google Cloud Speech-to-Text. The link is below.')
    st.markdown('<a href="https://cloud.google.com/speech-to-text?hl-ja">Cloud Speech-to-Text</a>', unsafe_allow_html=True)


    # APIコール結果をセッションで保持する
    if 'result' not in st.session_state:
        st.session_state['result'] = None


    # ファイルアップロード
    upload_file = st.file_uploader('Upload File', type=['mp3', 'wav'])

    # ファイル切り替える際にセッションを破棄する
    if upload_file is None:
        st.session_state.result = None
        st.session_state.word_1 = ''
        st.session_state.word_2 = ''
        st.session_state.word_3 = ''

    if upload_file is not None:
        content = upload_file.read()
        st.subheader('File Details')
        file_details = {
            'FileName': upload_file.name,
            'FileType': upload_file.type,
            'FileSize': upload_file.size
        }
        st.write(file_details)
        st.subheader('Audio Playback')
        st.audio(content)

        st.subheader('Chose Language')
        option = st.selectbox('Select a language for translation', ('English', 'Japanese'))

        st.write('文字起こし')
        if st.button('開始'):
            comment = st.empty()
            comment.write('Analyzing..')
#             st.session_state.result = transcribe_file(content, lang = option)
            st.session_state.result = "Erin how can I help you today I see you signed up for a course online and I just cannot access that I've been trying the last 4 hours download display doesn't do anything"
            comment.write('')
        if st.session_state.result is not None:
            st.write(st.session_state.result)

        if st.session_state.result:
            # 複数検索フォーム入力
            st.title('Multi Forms')
            input_words = []
            with st.form(key='search'):
                st.caption('Type words for searching') 
                col1, col2, col3 = st.columns([2,2,2])

                with col1:
                    word1 = st.text_input(label = '1', key = 'word_1')
                    input_words.append(word1)
                with col2:
                    word2 = st.text_input(label = '2', key = 'word_2')
                    input_words.append(word2)        
                with col3:
                    word3 = st.text_input(label = '3', key = 'word_3')
                    input_words.append(word3)        
                    st.form_submit_button(label="Search")

            matched_words = search(input_words)
            lumps = extract_words(matched_words)
            for lump in lumps:
                for word in lump:
                    st.write(word.name)
                    
                    
if __name__ == "__main__":
    main()