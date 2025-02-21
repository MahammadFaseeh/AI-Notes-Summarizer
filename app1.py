from flask import Flask, render_template, request
from text_summary import summarizer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  


@app.route('/summary', methods=['POST','GET'])
def summary():
    if request.method == 'POST':
        rawdocs = request.form['rawdocs']
        summary, doc, len_rawdocs, len_summary = summarizer(rawdocs)
        return render_template('index.html', rawdocs=rawdocs, summary=summary, len_rawdocs=len_rawdocs, len_summary=len_summary)

if __name__ == "__main__":
    app.run(debug=True)
