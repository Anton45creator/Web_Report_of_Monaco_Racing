import datetime
import json
from flasgger import Swagger
from simplexml import dumps
from flask import Flask, make_response, request, render_template
from flask_restful import Api
import rest
from db_helper import *

report = report_data()
report_reverse = sorted(report, key=lambda k: k['position'], reverse=True)


app = Flask(__name__)
api = Api(app, default_mediatype='application/json', prefix='/api/v1')
swagger = Swagger(app)


def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps({'response': data},
                                        default=converter), code)
    response.headers.extend(headers or {})
    return response


@api.representation('application/xml')
def output_xml(data, code, headers=None):
    response = make_response(dumps({'response': data}), code)
    response.headers.extend(headers or {})
    return response


@app.route('/')
def base():
    return render_template("base.html")


@app.route('/report/drivers', methods=['POST', 'GET'])
def statistic():
    order = request.args.get('order')
    if order == 'desc':
        return render_template("statistic.html", driver=report_reverse)
    else:
        return render_template("statistic.html", driver=report)


@app.route('/driver', methods=['POST', 'GET'])
def action():
    if request.method == 'POST':
        driver_id = request.form['key'].upper()
        for driver in report:
            if driver['key'] == driver_id:
                return render_template("drivers.html", pilot=driver)

    else:
        driver_id = request.args.get('driver_id')
        if driver_id:
            for driver in report:
                if driver['key'] == driver_id:
                    return render_template("drivers.html", pilot=driver)


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


api.add_resource(rest.Report, '/report')
api.add_resource(rest.Driver, '/driver/<driver_id>')

if __name__ == "__main__":
    app.run()
