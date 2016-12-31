from backend import app
from backend.version import __version__
from flask import jsonify

@app.route('/api/public/version', methods = ['GET'])
def api_version():
	return jsonify(__version__)
