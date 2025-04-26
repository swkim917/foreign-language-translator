import streamlit as st
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr

st.set_page_config(page_title="스트림릿 외국어 번역기", page_icon="🎙️")

with st.sidebar:
    st.write("made by **Kim Sang-woo**")
    st.write("*Dukmoon girl's high school*")


st.title("🎙️ Streamlit 외국어 번역기")
st.header("한국어 음성 입력 → 텍스트로 변환 → 선택한 외국어로 번역 → 외국어 음성 출력")


# 외국어 선택하기
lang = st.selectbox(
    "어떤 외국어로 번역할까요?",
    ("영어", "일본어", "중국어", "프랑스어", "독일어", "스페인어")
)

if lang == "영어":
    lang_code = "en"
elif lang == "일본어":
    lang_code = "ja"
elif lang == "중국어":
    lang_code = "zh-CN"
elif lang == "프랑스어":
    lang_code = "fr"
elif lang == "독일어":
    lang_code = "de"
elif lang == "스페인어":
    lang_code = "es"



# 1. 브라우저에서 음성 녹음 받기
audio_data = st.audio_input("마이크 아이콘을 클릭하고 말씀하세요! (자동 녹음)")

if audio_data:
    # st.audio(audio_data, autoplay=True)  # 녹음된 음성 재생
    
    recognizer = sr.Recognizer()
    
    # 2. BytesIO 형태의 오디오 데이터를 SpeechRecognition에 전달
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)
        try:
            # 3. 구글 STT API 호출 (언어 설정 가능)
            text = recognizer.recognize_google(audio, language='ko-KR')  # language='zh-CN' → 중국어
            st.success("📝 텍스트로 변환:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("음성을 인식할 수 없습니다.")
        except sr.RequestError:
            st.error("Google STT 서비스 오류 발생")





        # 한국어를 변수 lang에 지정한 언어로 번역한 텍스트 출력하기
        # 한국어(ko), 영어(en), 일본어(ja), 간체 중국어(zh-CN), 번체 중국어(zh-TW), 프랑스어(fr), 독일어(de), 이탈리아어(it), 스페인어(es), 러시아어(ru), 아랍어(ar), 포르투갈어(pt)
        translator = Translator()
        result = translator.translate(text, dest=lang_code)

        st.success("💬 " + lang + "로 번역:")
        st.write(result.text)



        # 번역된 텍스트를 음성으로 변환하여 mp3 오디오 파일 생성하기
        tts = gTTS(text=result.text, lang=lang_code)
        tts.save('speech.mp3')

        # 오디오 파일 소리 재생하기
        st.success("🔊 " + lang + " 음성 출력:")
        st.audio('speech.mp3', autoplay=True)

