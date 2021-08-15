import os
from google.cloud import speech
import io
import streamlit as st
import pandas as pd
from word import Word
from janome.tokenizer import Tokenizer

from language import Language


def main():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/secret.json'

    # ファイルを読み込んでテキスト化する
    def transcribe_file(content, lang = Language.ENG.value[1]) -> str:

        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content = content)
        config = speech.RecognitionConfig(
            encoding = speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            language_code = lang,
        )
        response = client.recognize(config = config, audio = audio)

        for result in response.results:
            return result.alternatives[0].transcript
        
    
    # 音声認識したテキストから単語リストを生成
    def generate_word_list(lang) -> list[str]:
        text = st.session_state.result

        if lang == Language.JP.value[0]:
            text = morphological_analyze(text)
        elif lang == Language.ENG.value[0]:
            text = text.split(' ')
        else:
            pass

        words = []
        for index, word in enumerate(text):
            words.append(Word(index = index, name = word))
        return words


    # 入力値をもとに単語を検索をする
    def search(input_words: list[str]) -> list[Word]:
        words = generate_word_list(st.session_state.lang)
        
        result = []
        for target in input_words:
            for w in words:
                if(w.name == target):
                    result.append(w)
        return result
    
    
    # 入力された検索文字列毎に前後5単語を抽出して二次元配列を作成
    def extract_words(matched_words) -> list[list[Word]]:
        lumps = []
        word_list = generate_word_list(st.session_state.lang)

        for word in matched_words:
            if len(word_list) < 11:
                lumps.append(word_list)
            elif word.index < 5:
                lumps.append(word_list[:word.index+6])
            else: lumps.append(word_list[word.index-5:word.index+6])
        return lumps
    
    
    def create_table(lumps):
        df = pd.DataFrame(data = map(lambda l: map(lambda w: w.name, l), lumps))
        st.table(df)


    # 検索文字列をハイライト
    def highlight_col(df):
        copied_df = df.copy()
        copied_df.loc[:,:] = None
        copied_df[[5]] = 'background-color: #F7A8D4'
        return copied_df


    # 形態素解析で日本語を分割
    def morphological_analyze(text) -> list[str]:
        t = Tokenizer()
        return t.tokenize(text, wakati=True)


    # Streamlitへの書き出し
    st.title('文字起こしアプリ')
    st.header('Overview')
    st.write('This is a transcription application that uses Google Cloud Speech-to-Text. The link is below.')
    st.markdown('<a href="https://cloud.google.com/speech-to-text?hl-ja">Cloud Speech-to-Text</a>', unsafe_allow_html = True)


    # APIコール結果をセッションで保持する
    if 'result' not in st.session_state:
        st.session_state['result'] = None

    # 選択言語をセッションで保持する
    if 'lang' not in st.session_state:
        st.session_state['lang'] = None

    # ファイルアップロード
    upload_file = st.file_uploader('Upload File', type = ['mp3', 'wav'])

    # ファイル切り替える際にセッションを破棄する
    if upload_file is None:
        st.session_state.result = None
        st.session_state.word_1 = ''
        st.session_state.word_2 = ''
        st.session_state.word_3 = ''
        st.session_state.lang = None

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
        option = st.selectbox('Select a language for translation', (Language.ENG.value[0], Language.JP.value[0]))
        st.session_state.lang = option

        st.write('文字起こし')
        if st.button('開始'):
            comment = st.empty()
            comment.write('Analyzing..')
            st.session_state.result = transcribe_file(content, lang = Language.get_code(option))
            # st.session_state.result = "Erin how can I help you today I see you signed up for a course online and I just cannot access that I've been trying the last 4 hours download display doesn't do anything"
            # st.session_state.result = 'ご住所の変更でございますねご連絡ありがとうございます恐れ入りますがご契約内容を確認いたしますのでお電話を頂いてる方は契約者ご本人様でいらっしゃいますかはいそうです本人ですそれではお電話をいただいておりますお客様のお名前をお願い致します山田太郎です'
            comment.write('')
        if st.session_state.result is not None:
            st.write(st.session_state.result)

        if st.session_state.result:
            # 複数検索フォーム入力
            st.title('Multi Forms')
            input_words = []
            with st.form(key = 'search'):
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
                    st.form_submit_button(label = "Search")

            matched_words = search(input_words)
            lumps = extract_words(matched_words)
            
            if len(lumps) is not 0:
                create_table(lumps)

                    
if __name__ == "__main__":
    main()