import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
from string import punctuation
text = """Technology has significantly transformed human life in ways that were unimaginable just a few decades ago. The rapid advancements in artificial intelligence, automation, and digital communication have reshaped industries, workplaces, and everyday interactions. From the rise of smartphones to the development of self-driving cars, the world has entered an era where convenience and efficiency are at the forefront of progress. One of the most notable aspects of technological growth is the impact on communication. Gone are the days when people had to rely on letters or landline phones to stay connected. Today, with the advent of instant messaging apps, social media, and video conferencing, individuals can communicate with anyone, anywhere in the world, in real time. This has strengthened global connections, allowing businesses to collaborate across continents and families to remain close despite physical distances. Moreover, technology has revolutionized education, making learning more accessible than ever before. Online courses, virtual classrooms, and e-books have provided students with a vast array of resources that cater to different learning styles. Platforms like Coursera, Udemy, and Khan Academy allow individuals to gain new skills from the comfort of their homes, breaking barriers that once made education exclusive to specific institutions. Additionally, artificial intelligence and machine learning have introduced personalized learning experiences, enabling students to progress at their own pace. Another crucial domain that has seen immense transformation is healthcare. Modern medical technology has not only enhanced diagnostic and treatment methods but also improved patient care and management. Innovations such as robotic surgeries, wearable health trackers, and telemedicine have allowed doctors to provide better and more efficient healthcare services. Telemedicine, in particular, has bridged the gap between doctors and patients in remote areas, ensuring that medical expertise is accessible even in the most challenging locations. Furthermore, breakthroughs in genetic research and biotechnology are paving the way for customized medicine, where treatments can be tailored based on an individual's genetic makeup. Beyond communication, education, and healthcare, automation and artificial intelligence are reshaping the job market. While some fear that automation may replace human jobs, others argue that it will create new opportunities, requiring individuals to adapt and acquire new skills. Industries such as manufacturing, retail, and customer service have already witnessed the integration of AI-driven tools that optimize operations. However, technology has also brought challenges, including concerns about privacy, cybersecurity, and the ethical implications of AI. The rise of digital platforms has led to increased data collection, raising questions about how personal information is used and stored. Cybersecurity threats have become more sophisticated, requiring constant updates in security measures to protect individuals and organizations from cyberattacks. Additionally, ethical debates surrounding AI and machine learning continue to grow, especially in areas such as facial recognition and decision-making algorithms. Despite these challenges, technology remains a driving force for progress. As society continues to innovate, striking a balance between technological advancement and ethical responsibility will be crucial. By leveraging technology wisely, humanity can continue to overcome barriers, improve lives, and build a future that is more connected, efficient, and sustainable than ever before"""
def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    #print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)
    tokens = [token.text for token in doc]
    #print(tokens)
    #punctuation = punctuation + '\n
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1
    #print(word_freq)
    max_freq = max(word_freq.values())
    #print(max_freq)
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
    #print(word_freq)
    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)
    sent_score = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text]
                else:
                    sent_score[sent] += word_freq[word.text]
    #print(sent_score)
    select_len = int(len(sent_tokens)*0.3)
    #print(select_len)
    summary = nlargest(select_len, sent_score, key = sent_score.get)
    #print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    #print(text)
    #print(summary)
    #print("length of original text:",len(text.split(" ")))
    #print("length of summary:",len(summary.split(" ")))
    return summary, doc, len(rawdocs.split(" ")), len(summary.split(" "))
