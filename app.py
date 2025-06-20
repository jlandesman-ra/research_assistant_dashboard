from flask import Flask, jsonify, render_template
from flask_cors import CORS
from cached_asana_service import CachedAsanaService
from mock_asana_service import MockAsanaService
from config import Config
import traceback

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize cached service (primary) and mock service (fallback)
cached_service = CachedAsanaService()
mock_service = MockAsanaService()

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/api/project-data')
def get_project_data():
    """Get project data from Asana"""
    try:
        data = cached_service.get_project_data()
        
        # Get cache timestamp
        cache_timestamp = cached_service.get_cache_timestamp()
        
        return jsonify({
            'success': True,
            'data': data,
            'cache_timestamp': cache_timestamp
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Asana Dashboard API is running'
    })

@app.route('/api/refresh-cache', methods=['POST'])
def refresh_cache():
    """Refresh the cache and return updated data"""
    try:
        # Force refresh the cache
        data = cached_service.get_project_data(force_refresh=True)
        
        # Get updated cache timestamp
        cache_timestamp = cached_service.get_cache_timestamp()
        
        return jsonify({
            'success': True,
            'data': data,
            'cache_timestamp': cache_timestamp,
            'message': 'Cache refreshed successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to refresh cache'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 