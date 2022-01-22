import datetime
import time

from opcua import Server
from opcua import ua, uamethod

from calculator import Calculator

the_time = datetime.datetime.now()

# setup our server
myserver = Server()
url = "opc.tcp://127.0.0.1:48400"
myserver.set_endpoint(url)
myserver.set_server_name("Calculator")
myserver.set_security_policy([ua.SecurityPolicyType.NoSecurity])

name = "OPCUA Testserver"
idx = myserver.register_namespace(name)

# Nodes erstellen
node = myserver.get_objects_node()
myobj = node.add_object(idx, "Calculator")
c = Calculator(myobj, idx)

myserver.start()
print("Server ist online {}".format(url), the_time)


