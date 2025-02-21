from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import spacy
from heapq import nlargest
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

app = Flask(__name__)
CORS(app)  # Allow frontend requests to communicate with backend

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Summarizer function
def summarizer(raw_text):
    stopwords = list(STOP_WORDS)
    doc = nlp(raw_text)
    word_freq = {}

    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            word_freq[word.text] = word_freq.get(word.text, 0) + 1

    max_freq = max(word_freq.values(), default=1)  # Avoid division by zero
    word_freq = {word: freq / max_freq for word, freq in word_freq.items()}

    sent_tokens = [sent for sent in doc.sents]
    sent_score = {}

    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq:
                sent_score[sent] = sent_score.get(sent, 0) + word_freq[word.text]

    select_len = max(1, int(len(sent_tokens) * 0.3))  # Ensure at least one sentence
    summary = nlargest(select_len, sent_score, key=sent_score.get)
    final_summary = " ".join([sent.text for sent in summary])

    return final_summary

@app.route('/')
def index():
    return render_template('index.html')  # Loads frontend

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        raw_text = data.get('text', '')

        if not raw_text.strip():
            return jsonify({"error": "No text provided"}), 400

        summary = summarizer(raw_text)

        return jsonify({"summary": summary})  # Return summary as JSON response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
