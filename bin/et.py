#!/usr/bin/env python2.7

import logging
import json
import sys
import psycopg2
from datetime import timedelta
from flask import Flask, make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


app = Flask(__name__)

db_server = 'et.cntms98hv39g.us-west-2.rds.amazonaws.com' 
 
conn = None
cur = None
try:
	conn = psycopg2.connect("dbname=et host=%s user=calgrove password=mlfun4us!" % db_server)
	conn.autocommit = True
	cur = conn.cursor()
except Exception as exc:
	logging.error('exception raised trying to connect to database\n%s', str(exc))
	sys.exit(1)


@app.route('/api/packet', methods=['POST'])
def packet():
	batch = json.loads(request.data)
	args_str = ','.join(cur.mogrify('(%s, %s, %s)', data) for data in batch)
	try:
		cur.execute('INSERT INTO traffic (ip, lat, lon) VALUES ' + args_str)
	except Exception as exc:
		print exc
	return ''


@app.route('/api/traffic', methods=['GET'])
@crossdomain(origin='*')
def traffic():
	traffic_data = []
	try:
		cur.execute("select lat, lon, count(*) from traffic group by lat, lon;")
		rows = cur.fetchall()
		for row in rows:
			traffic_data.append({
				'lat': float(row[0]),
				'lon': float(row[1]),
				'count': int(row[2])
			})
	except Exception as exc:
		print exc
	return json.dumps(traffic_data)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=9999)


