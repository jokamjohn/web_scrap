from app import app
from flask import make_response, jsonify, request
from daily_nation import DailyNation


@app.route('/')
def get_topics():
    topics = DailyNation.get_topics()
    return make_response(jsonify({
        'status': 'success',
        'topics': topics
    }))


@app.route('/topics')
def get_data():
    topic = request.args.get('topic')
    try:
        data = DailyNation.get_data(topic)
    except ValueError:
        return make_response(jsonify({
            'status': 'failed',
            'message': 'topic not found'
        })), 400
    return make_response(jsonify({
        'status': 'success',
        'data': data
    }))
