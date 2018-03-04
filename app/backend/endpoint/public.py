from backend import app, logger
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


@app.route('/api/public/notify', methods=['POST'])
def api_notify():
	event = request.json
	sheet_id = event['sheet_id']
	print sheet_id
	try:
		repository.add(event, index, doc_type)
		response = jsonify(message='Event created')
		response.status_code = 200
		return response
	except Exception as e:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(e).__name__, e.args)
		print message
		response = jsonify(message='errors')
		response.status_code = 500
		return response
