import psycopg2

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

cur.execute('DELETE FROM traffic;');
