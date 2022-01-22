from opcua import ua, uamethod


class Calculator:
    idx = None
    rootnode = None
    methods = {}
    countcalls = {}
    callcounters = {}

    def __create_node__(self, name, method, parameter_types, results):
        method_obj = self.rootnode.add_method(self.idx, name, method, parameter_types, results)
        print(f"{name} = {str(method_obj)}")
        self.methods[name] = method_obj
        self.countcalls[name] = self.rootnode.add_variable(self.idx, f"count-{name}", False, ua.VariantType.Boolean)
        print(f"count-{name} = {self.countcalls[name]}")
        self.countcalls[name].set_writable()
        self.callcounters[name] = self.rootnode.add_variable(self.idx, f"{name}counter", False, ua.VariantType.Int32)
        print(f"{name}counter = {self.callcounters[name]}")
        self.callcounters[name].set_value(0)

    def __method_called__(self, name):
        if self.countcalls[name].get_value() is True:
            current = self.callcounters[name].get_value()
            self.callcounters[name].set_value(current + 1)

    def __init__(self, rootnode, idx):
        self.idx = idx
        self.rootnode = rootnode
        print(f"server created, idx = {self.idx} and root node = {self.rootnode}")
        self.__create_node__("add", self.add, [ua.VariantType.Float, ua.VariantType.Float], [ua.VariantType.Float])
        self.__create_node__("sub", self.sub, [ua.VariantType.Float, ua.VariantType.Float], [ua.VariantType.Float])
        self.__create_node__("div", self.div, [ua.VariantType.Float, ua.VariantType.Float], [ua.VariantType.Float])
        self.__create_node__("mul", self.mul, [ua.VariantType.Float, ua.VariantType.Float], [ua.VariantType.Float])

    @uamethod
    def add(self, parent, a, b):
        self.__method_called__("add")
        a = 0 if a is None else a
        b = 0 if b is None else b
        return a + b
    @uamethod
    def sub(self, parent, a, b):
        self.__method_called__("sub")
        a = 0 if a is None else a
        b = 0 if b is None else b
        return a - b
    @uamethod
    def div(self, parent, a, b):
        self.__method_called__("div")
        a = 0 if a is None else a
        b = 1 if b is None else b
        return a / b
    @uamethod
    def mul(self, parent, a, b):
        self.__method_called__("mul")
        a = 0 if a is None else a
        b = 0 if b is None else b
        return a * b
