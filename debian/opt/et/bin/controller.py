import json
import logging
from optparse import OptionParser
import pygeoip
import urllib2

MAX_BATCH_SIZE = 200

parser = OptionParser('usage: et -d <geo data>')
parser.add_option('-d', '--data', dest='geo_data_path',
  help='path to GeoIP data', metavar='DATA')
options, args = parser.parse_args()

if not options.geo_data_path:
  options.geo_data_path = '/opt/et/data/GeoLiteCity.dat'

gi = pygeoip.GeoIP(options.geo_data_path)

batch = []

def retGeo(ip):
    try:
        rec = gi.record_by_name(ip)
        return rec['latitude'], rec['longitude']
    except Exception as exc:
        return None, None

def batch_append(src, dst):
    if not dst.startswith('192.168'):
        addr = dst
        lat, lon = retGeo(dst)
    elif not src.startswith('192.168'):
        addr = src
        lat, lon = retGeo(src)
    else:
        return
    batch.append((addr, lat, lon))
    if len(batch) >= MAX_BATCH_SIZE:
        upload_batch()

def upload_batch():
    url = 'http://ec2-54-188-199-29.us-west-2.compute.amazonaws.com:9999/api/packet'
    headers = {
        'Content-Type': 'application/json'
    }
    req = urllib2.Request(url, json.dumps(batch), headers)
    try:
        urllib2.urlopen(req)
        global batch
        batch = []
    except Exception as exc:
        logging.error('error occurred while trying to upload data: {}'.format(exc))
