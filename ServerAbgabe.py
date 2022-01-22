import datetime
import time

from opcua import Server
from opcua import ua, uamethod



the_time = datetime.datetime.now()

# setup our server
myserver = Server()
url = "opc.tcp://localhost:4840"
myserver.set_endpoint(url)
myserver.set_security_policy([ua.SecurityPolicyType.NoSecurity])

name = "OPCUA Testserver"
idx = myserver.register_namespace(name)

# Node erstellen
node = myserver.get_objects_node()
myobj = node.add_object(idx, "Parameter")

x1 = myobj.add_variable(idx, "Eingabe 1", 0.0)
x2 = myobj.add_variable(idx, "Eingabe 2", 0.0)

x1.set_writable()
x2.set_writable()

X1 = x1.get_value()
X2 = x2.get_value()

class Calculator:
    idx = None
    rootnode = None
    methods = {}
    countcalls = {}
    callcounters = {}

    def __create_node__(self, name, method, parameter_types, results):
        method_obj = self.rootnode.add_method(self.idx, name, method, parameter_types, results)
        self.methods[name] = method_obj
        self.countcalls[name] = self.rootnode.add_variable(idx, f"count-{name}", False, ua.VariantType.Boolean)
        self.countcalls[name].set_writable()
        self.callcounters[name] = self.rootnode.add_variable(idx, f"{name}counter", False, ua.VariantType.Int32)
        self.callcounters[name].set_value(0)

    def __method_called__(self, name):
        if self.countcalls[name].get_value() is True:
            current = self.callcounters[name].get_value()
            self.callcounters[name].set_value(current + 1)

    def __init__(self, rootnode, idx):
        self.idx = idx
        self.rootnode = rootnode
        self.__create_node__("add", self.add, [ua.VariantType.Float, ua.VariantType.Float], [ua.VariantType.Float])
        self.__create_node__("sub", self.sub, [ua.VariantType.Float, ua.VariantType.Float], [ua.VariantType.Float])
        self.__create_node__("mul", self.div, [ua.VariantType.Float, ua.VariantType.Float], [ua.VariantType.Float])
        self.__create_node__("div", self.mul, [ua.VariantType.Float, ua.VariantType.Float], [ua.VariantType.Float])
        #self.methods.set_writable()
        #self.methods.set_value()

    @uamethod
    def add(self, parent, a, b):
        self.__method_called__("add")
        a = X1 if a is None else a
        b = X2 if b is None else b
        return a + b

    @uamethod
    def sub(self, parent, a, b):
        self.__method_called__("sub")
        a = X1 if a is None else a
        b = X2 if b is None else b
        return a - b

    @uamethod
    def mul(self, parent, a, b):
        self.__method_called__("mul")
        a = X1 if a is None else a
        b = X2 if b is None else b
        return a * b

    @uamethod
    def div(self, parent, a, b):
        self.__method_called__("div")
        a = X1 if a is None else a
        b = X2 if b is None else b
        return a / b

c = Calculator(myobj, idx)

myserver.start()
print("Server ist online {}".format(url), the_time)


