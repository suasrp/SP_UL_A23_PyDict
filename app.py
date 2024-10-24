import streamlit as st
import random
from gtts import gTTS
import tempfile
from PyDictionary import PyDictionary

# List of words
words = [
    "abbreviate", "abnormality", "abode", "abrasion", "abundantly", "academic",
    "accessory", "accordion", "acidic", "acne", "acrobat", "adhesive",
    "admirable", "adoption", "adversary", "affected", "affliction", "affordable",
    "agenda", "airport", "alimony", "allergic", "alliance", "alpaca",
    "alphabetical", "amateur", "amplify", "amusing", "animate", "anklebone",
    "annex", "antibacterial", "antibiotic", "anxiety", "apparition", "appease",
    "applause", "aptitude", "aquamarine", "arcade", "arrangement", "assortment",
    "athletic", "attractive", "auditory", "avalanche", "avocado", "badminton",
    "balky", "Ballyhoo", "barbarian", "bareback", "bargain", "barrette",
    "bashfulness", "beacon", "bedazzle", "bedridden", "beforehand", "behavior",
    "believable", "beneficial", "benevolent", "biannual", "bicultural", "bicycle",
    "billionaire", "bimonthly", "biodiversity", "bionics", "birthmark", "blamable",
    "blarney", "blissful", "blistering", "bluebonnet", "bolster", "bonfire",
    "boomerang", "botulism"
]

class SpellingApp:
    def __init__(self):
        self.dictionary = PyDictionary()
        self.current_word = None
        self.score = 0
        self.results = []

    def generate_audio(self, word):
        tts = gTTS(text=word, lang='en')
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            tts.save(tmp.name)
            return tmp.name

    def show_meaning(self, word):
        meaning = self.dictionary.meaning(word)
        return meaning if meaning else "Meaning not found."

    def check_spelling(self, user_input):
        if user_input.lower() == self.current_word:
            self.score += 1
            return "Correct!"
        else:
            return f"Incorrect. The correct spelling is: {self.current_word}"

    def start_test(self):
        self.current_word = random.choice(words)
        return self.current_word

def main():
    st.title("Spelling Test")
    app = SpellingApp()
    
    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.results = []
    
    st.subheader("Instructions:")
    st.write("1. Click 'Start Test' to begin.")
    st.write("2. Spell the displayed word.")
    st.write("3. Use the buttons to hear the word or see its meaning.")
    
    if st.button("Start Test"):
        current_word = app.start_test()
        st.session_state.current_word = current_word
        st.session_state.user_input = ""
        st.session_state.result_message = ""

    if 'current_word' in st.session_state:
        st.write(f"### Spell the word: {st.session_state.current_word}")
        
        if st.button("Pronounce"):
            audio_file = app.generate_audio(st.session_state.current_word)
            st.audio(audio_file)

        if st.button("Show Meaning"):
            meaning = app.show_meaning(st.session_state.current_word)
            st.write(f"Meaning: {meaning}")

        st.text_input("Your answer:", key='user_input')

        if st.button("Submit"):
            result_message = app.check_spelling(st.session_state.user_input)
            st.session_state.results.append((st.session_state.current_word, st.session_state.user_input, result_message))
            st.session_state.result_message = result_message
            
            if len(st.session_state.results) >= len(words):
                st.write(f"Your total score is: {app.score}/{len(words)}")
                st.session_state.clear()  # Reset for next test

            else:
                st.session_state.current_word = app.start_test()
                st.session_state.user_input = ""

        if st.session_state.result_message:
            st.write(st.session_state.result_message)

if __name__ == "__main__":
    main()
