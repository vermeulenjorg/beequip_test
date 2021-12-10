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


def check_correct_input_date(year,month,day):
    """
    Checks if input date exists
    :param year: the year to check
    :param month: the month to check
    :param day: the day to check
    :return: the converted datestring
    """
    correct_date = False
    try:
        datestring = datetime.datetime(year=int(year),month=int(month),day=int(day))
    except ValueError:
        abort(422, description="Given Date doesn't Exists")
    return datestring


def check_if_input_exists(column,table, value):
    """
    check if given input is available in the database it will abort if the value is not found so no return is needed
    :param column: the column where the value is stored
    :param table: the table to check
    :param value: the value to check
    """
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("SELECT {0}  FROM {1} WHERE {0} = '{2}' group by 1;".format(column, table, value))
        result = cursor.fetchone()
        if result == None:
            abort(422, description="{0} doesnt exist in table {1}".format(value, column))
    except Exception as e:
        print(e)
        abort(500, description="Internal Server Error")



@app.route("/")
def health_check():
    """
    Just a basic endpoint to check health
    :return: Json with status 200 if correct
    """
    try:
        conn = getconnection()
    except Exception as e:
        print(e)
        abort(500, description="Internal Server Error")
    return jsonify(status=200, mimetype='application/json')


@app.route("/api/v1/lease/<reference>/<year>/<month>/<day>")
def get_outstanding_lease(reference, year, month, day):
    """
    This API is a reference to FR-1: What's the outstanding for a lease given a reference and date?
    I used SQL as much as possible for this case. And not reuse any statement to get data.
    :param reference: The lease Reference
    :param year: The Year for the outstanding Lease
    :param month: The Month for the outstanding Lease
    :param day: The Day for the outstanding lease
    :return: A JSON reponse containing mimetype, status, given parameters and result in 'data'
    """
    # check if date exists
    datestring = check_correct_input_date(year=year,month=month,day=day)
    # check if reference exists
    check_if_input_exists(column='reference', table='lease', value=reference)
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("select row_to_json(outst) "
                       "from ( SELECT CASE WHEN outstanding+principal < 0 THEN 0 ELSE  outstanding+principal  END outstanding "
                       "from installment where date <= '{0}' "
                       "AND installment_no in (SELECT installment_no  "
                       "FROM lease WHERE reference = '{1}') ORDER BY date DESC LIMIT 1) outst;".format(datestring, reference))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row == None:
            abort(422, description="installment starts later")
    except Exception as e:
        print(e)
        abort(500, description="Internal Server Error")

    return jsonify(status=200, mimetype='application/json', reference=reference, year=year, month=month, day=day, data=row)


@app.route("/api/v1/organisation/<coc_number>/<year>/<month>/<day>")
def get_total_organisational_outstanding_lease(coc_number, year, month, day):
    """
    This API is a reference to FR-2: What's the total outstanding for a organisation given a Camber of Commerce number and date?
    I used SQL as much as possible for this case. And not reuse any statement to get data.
    :param coc_number: the chamber of commerce number
    :param year: The Year for the total outstanding Lease
    :param month: The Month for the total outstanding Lease
    :param day: The Day for the total outstanding lease
    :return: A JSON reponse containing mimetype, status, given parameters and result in 'data'
    """
    # check if date exists
    datestring = check_correct_input_date(year=year, month=month, day=day)
    check_if_input_exists(column='coc_number', table='customer', value=coc_number)
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("select row_to_json(outst) "
                       "from (SELECT SUM(outstanding) AS total_outstanding "
                       "FROM (SELECT CASE WHEN outstanding+principal < 0 THEN 0 ELSE  outstanding+principal  END outstanding "
                       "from installment where date <= '{0}' "
                       "AND installment_no in (SELECT installment_no "
                       "from Lease where customer_id = (Select id from Customer "
                       "where coc_number = '{1}') group by 1)  ORDER BY date DESC LIMIT 1) total )  outst;".format(datestring, coc_number))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row == None:
            abort(422, description="installment starts later")
    except Exception as e:
        print(e)
        abort(500, description="Internal Server Error")

    return jsonify(status=200, mimetype='application/json', coc_number=coc_number, year=year, month=month, day=day, data=row)

@app.route("/api/v1/team/current")
def get_total_outstanding_per_team_and_lane():
    """
    This API is a reference to FR-3: What's the total outstanding per team and lane given a date?
    I used SQL as much as possible for this case. And not reuse any statement to get data.
    :return: outstandings per team and lane
    """
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute(
                       "select row_to_json(outst) from ( SELECT team, SUM(outstanding)  as total_outstanding , (SELECT json_agg(lane_sum) FROM (SELECT lane, total_outstanding FROM ( SELECT team, lane, SUM(outstanding) as total_outstanding "
                       "FROM lease let "
                       "LEFT JOIN (select ins.installment_no, CASE WHEN outstanding+principal < 0 THEN 0 ELSE  outstanding+principal  END outstanding "
                       "from installment ins INNER JOIN (SELECT installment_no, max(t) as t "
                       "FROM installment WHERE date <= '{0}' GROUP BY 1) maxi "
                       "ON maxi.installment_no = ins.installment_no AND maxi.t=ins.t) outs "
                       "ON outs.installment_no = let.installment_no where le.team=team GROUP BY 1,2) as a) as lane_sum) AS Lanes "
                       "FROM lease le "
                       "LEFT JOIN (select ins.installment_no, CASE WHEN outstanding+principal < 0 THEN 0 ELSE  outstanding+principal  END outstanding "
                       "from installment ins INNER JOIN (SELECT installment_no, max(t) as t "
                       "FROM installment WHERE date <= '{0}' GROUP BY 1) maxi "
                       "ON maxi.installment_no = ins.installment_no AND maxi.t=ins.t) outs "
                       "ON outs.installment_no = le.installment_no GROUP BY 1) outst;".format(datetime.datetime.now()))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows == None:
            abort(422, description="installment starts later")
    except Exception as e:
        print(e)
        abort(500, description="Internal Server Error")
    return jsonify(status=200, mimetype='application/json', data={'teams': rows})


@app.route("/api/v1/team/start")
def get_average_at_start_per_team_and_lane():
    """
    This API is a reference to FR-4: What's the average outstanding per team and lane at the start?
    I used SQL as much as possible for this case. And not reuse any statement to get data.
    :return: outstandings per team and lane at start
    """
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute(
                       "select row_to_json(outst) from (SELECT team, AVG(outstanding) as avg_outstanding, (SELECT json_agg(lane_sum) FROM (SELECT lane,avg_outstanding FROM ("
                       "SELECT team, lane, AVG(outstanding) AS avg_outstanding "
                       "FROM lease let "
                       "LEFT JOIN (select ins.installment_no, outstanding "
                       "from installment ins INNER JOIN (SELECT installment_no, min(t) as t "
                       "FROM installment GROUP BY 1) mini "
                       "ON mini.installment_no = ins.installment_no AND mini.t=ins.t) outs "
                       "ON outs.installment_no = let.installment_no where le.team=team GROUP BY 1,2) as a) as lane_sum) AS Lanes "
                       "FROM lease le "
                       "LEFT JOIN (select ins.installment_no, outstanding "
                       "from installment ins INNER JOIN (SELECT installment_no, min(t) as t "
                       "FROM installment GROUP BY 1) mini "
                       "ON mini.installment_no = ins.installment_no AND mini.t=ins.t) outs "
                       "ON outs.installment_no = le.installment_no GROUP BY 1 ) outst;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows == None:
            abort(422, description="installment starts later")
    except Exception as e:
        print(e)
        abort(500, description="Internal Server Error")
    return jsonify(status=200, mimetype='application/json', data={'teams': rows})


@app.route("/api/v1/daily/<year>")
def get_total_daily_outstanding(year):
    """
    This API is a reference to FR-5: What's the total outstanding per team and lane given a date?
    I used SQL as much as possible for this case. And not reuse any statement to get data.
    :return:
    """
    try:
        conn = getconnection()
        cursor = conn.cursor()
        cursor.execute("select row_to_json(outst) from (SELECT generated_days as day, (SELECT SUM(outstanding) FROM (SELECT DISTINCT ON (installment_no) installment_no, CASE WHEN outstanding+principal < 0 THEN 0 ELSE  outstanding+principal  END outstanding "
                       "FROM  installment  WHERE date <= gd.generated_days "
                       "ORDER BY installment_no, t desc) AS out) "
                       "FROM (SELECT generate_series(date '{0}-01-01', date '{0}-12-31', '1 day') as generated_days) gd"
                       ") outst;".format(year))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        abort(500, description="Internal Server Error")
    return jsonify(status=200, mimetype='application/json', year=year, data={'days':rows})
