from backend import app
from backend.version import __version__
from flask import jsonify
from flask import request
from repository import Repository

repository = Repository(app.config)

index='event'
doc_type='ficha'

@app.route('/api/public/version', methods = ['GET'])
def api_version():
	return jsonify(__version__)


@app.route('/api/public/notify/<login>', methods=['POST'])
def api_notify(login):
	event = request.json
	print event
	sheet_id = event['sheet_id']
	print sheet_id
	repository.insert(login, event, index, doc_type)

	print 'Insert OK'
	return login
