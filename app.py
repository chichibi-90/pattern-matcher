from flask import Flask, render_template, jsonify, request
from db_connection import get_ccy_pairs, get_price_data, find_similar_patterns
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with the web UI"""
    return render_template('index.html')

@app.route('/api/ccy-pairs')
def api_ccy_pairs():
    """API endpoint to get all available currency pairs"""
    try:
        pairs = get_ccy_pairs()
        return jsonify({'success': True, 'pairs': pairs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/price-data/<ccy_pair>')
def api_price_data(ccy_pair):
    """API endpoint to get price data for a specific currency pair"""
    try:
        data = get_price_data(ccy_pair)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/pattern-match', methods=['POST'])
def api_pattern_match():
    """API endpoint to find similar patterns in other currency pairs"""
    try:
        data = request.get_json()
        ccy_pair = data.get('ccy_pair')
        price_data = data.get('price_data')
        num_candles = data.get('num_candles', 20)
        top_n = data.get('top_n', 5)
        
        if not ccy_pair or not price_data:
            return jsonify({'success': False, 'error': 'Missing ccy_pair or price_data'}), 400
        
        similar_patterns = find_similar_patterns(ccy_pair, price_data, num_candles, top_n)
        return jsonify({'success': True, 'matches': similar_patterns})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


