import dpkt
import socket
from optparse import OptionParser
import pygeoip

parser = OptionParser('usage: et -p <pcap file> -d <geo data>')
parser.add_option('-d', '--data', dest='geo_data_path',
  help='path to GeoIP data', metavar='DATA')
parser.add_option('-p', '--pcap', dest='pcap_path',
  help='path to packet capture', metavar='PCAP')
options, args = parser.parse_args()

if not options.geo_data_path:
  options.geo_data_path = '/opt/et/data/GeoLiteCity.dat'

gi = pygeoip.GeoIP(options.geo_data_path)

def retGeoStr(ip):
    try:
        rec = gi.record_by_name(ip)
        city = rec['city']
        country = rec['country_code3']
        if city:
            geoLoc = city + ', ' + country
        else:
            geoLoc = country
        return geoLoc
    except Exception as exc:
        return 'Unregistered'

def printPcap(pcap):
    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print
            print '[+] Src: ' + src + ' --> Dst: ' + dst
            print '[+] Src: ' + retGeoStr(src) + ' --> Dst: ' + retGeoStr(dst)
        except:
            pass

def main():
    if not options.pcap_path:
        print parser.usage
        exit(0)
    f = open(options.pcap_path)
    printPcap(dpkt.pcap.Reader(f))

if __name__ == '__main__':
    main()
