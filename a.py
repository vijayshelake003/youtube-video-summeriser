from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.route('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    transcript = get_transcript(video_id)
    summary = get_summary(transcript)
    return summary, 200

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    summarizer = pipeline('summarization')
    summarized_text = []

    for i in range(0, (len(transcript)//1000)+1):
        start = i * 1000
        end = (i + 1) * 1000
        segment = transcript[start:end]
        summary_text = summarizer(segment)[0]['summary_text']
        summarized_text.append(summary_text)

    return ' '.join(summarized_text)

if __name__ == '__main__':
    app.run()
