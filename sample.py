from flask import Flask, render_template, request, redirect, url_for
from newspaper import Article
import summary

app = Flask(__name__)

def clean_text(text):
    lines = [line.strip() for line in text.split('\n') if 'Advertisement' not in line]
    return '\n'.join(lines)

def count_words(paragraph):
    words = paragraph.split()
    return len(words)

def get_cleaned_text(url):
    article = Article(url)
    article.download()
    article.parse()
    text_content = article.text
    cleaned_text = clean_text(text_content)
    summarized_text = summary.summarize_text(cleaned_text)
    return summarized_text, article.top_image, article.title, article.publish_date, article.authors

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.form['url']
    cleaned_content, header_image_url, title, publish_date, authors = get_cleaned_text(url)
    wordcount = count_words(cleaned_content)
    publish_date = str(publish_date)[0:10]
    return render_template('webpage_summary.html',
                           title=title,
                           publish_date=publish_date,
                           authors=authors,
                           header_image_url=header_image_url,
                           content=cleaned_content,
                           words = wordcount)

if __name__ == '__main__':
    app.run(debug=True)