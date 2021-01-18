from flask import jsonify

class Response:
    @staticmethod
    def success(data = None):
        return jsonify({
            'code': 0,
            'msg': 'ok',
            'data': data
        })
    
    @staticmethod
    def error(msg = None):
        return jsonify({
            'code': 1,
            'msg': msg,
            'data': None
        })
