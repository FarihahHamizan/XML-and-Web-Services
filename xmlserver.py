from xmlrpc.server import SimpleXMLRPCServer

def is_warm_cold(temp):
    if temp in range(0,11):
        return 'Cold'
    elif temp in range(11,21):
        return 'Warm'
        
# RPC Server
server = SimpleXMLRPCServer(('localhost',8001))
print('Listening on port 8001!!!')
server.register_function(is_warm_cold, 'is_warm_cold')
server.serve_forever()