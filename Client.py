from opcua import Client
import datetime
import time

the_time = datetime.datetime.now()

url = "opc.tcp://localhost:4840"

client = Client(url)

client.connect()
print("Client verbunden", the_time)

z1 = float(input("Bitte Zahl 1 eingeben "))
z2 = float(input("Bitte Zahl 2 eingeben "))

x1 = client.get_node("ns=2;i=2")
X1 = x1.set_value(z1)
x2 = client.get_node("ns=2;i=3")
X2 = x2.set_value(z2)

while True:
    Add = client.call_method("ns=2;i=6")
    print(Add)
    Addition = Add.call_method()
    print(Addition)

    time.sleep(1)
