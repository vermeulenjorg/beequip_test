import json

from flask import Flask, jsonify, abort
import datetime
from database import getconnection


app = Flask(__name__)


# errors
@app.errorhandler(400)
def resource_not_found(e):
    """
    Unfindable object in database
    :rtype: object
    """
    return jsonify(error=str(e)), 400


@app.errorhandler(422)
def wrong_input(e):
    """
    Wrong Input Error
    :rtype: object
    """
    return jsonify(error=str(e)), 422


@app.errorhandler(500)
def internal_server_error(e):
    """
    Internal Server Error
    :rtype: object
    """
    return jsonify(error=str(e)), 500


@app.route("/")
def health_check():
    return jsonify(status=200, mimetype='application/json')


@app.route("/api/v1/lease/<reference>/<year>/<month>/<day>")
def get_outstanding_lease(reference, year, month, day):
    """
    This API is a reference to FR-1: What's the outstanding for a lease given a reference and date?
    I used SQL as much as possible for this case. Selects the
    :param reference: The lease Reference
    :param year: The Year for the outstanding Lease
    :param month: The Month for the outstanding Lease
    :param day: The Day for the outstanding lease
    :return: A JSON reponse containing mimetype, status, given parameters and result in 'data'
    """
    # check if date exists
    # try:
    #     datestring = datetime.datetime(year=int(year),month=int(month),day=int(day))
    # except ValueError:
    #     abort(422, description="Given Date doesn't Exists")
    # conn = getconnection()
    # cursor = conn.cursor()
    # # check if reference exists
    # try:
    #     cursor.execute("SELECT installment_no  FROM lease WHERE reference = '{0}' group by 1;".format(reference))
    # except Exception as e:
    #     print(e)
    #     abort(500, description="Internal Server Error")
    # if cursor.fetchone() == None:
    #     abort(422, description="installment_no doesn't Exists")
    # # check if before start of installment
    #     # check if reference exists
    # # cursor.execute("SELECT installment_no  FROM lease WHERE reference = '{0}';".format(reference))
    # try:
    #     cursor.execute("select row_to_json(outst) from ( SELECT CASE WHEN outstanding+principal < 0 THEN 0 ELSE  outstanding+principal  END outstanding from installment where date <= '{0}' AND installment_no in (SELECT installment_no  FROM lease WHERE reference = '{1}') ORDER BY date DESC LIMIT 1) outst;".format(datestring, reference))
    # except Exception as e:
    #     print(e)
    #     abort(500, description="Internal Server Error")
    # row = cursor.fetchone()
    # if row == None:
    #     abort(422, description="installment starts later")
    # cursor.close()
    # conn.close()
    return jsonify(status=200, mimetype='application/json')
    # return jsonify(status=200, mimetype='application/json', reference=reference, year=year, month=month, day=day, data=row)


#
# TODO
# What's the total outstanding for a organisation given a Camber of Commerce number and date?
# TODO
# What's the total outstanding per team and lane given a date?
# TODO
# What's the average outstanding at the start of the lease per team and lane?
# TODO
# What's the total daily outstanding given a year?
# TODO