from opcua import Client
import datetime

ROOT_NODE = "ns=2;i=1"

NODE_ADD = "ns=2;i=2"
NODE_COUNT_ADD = "ns=2;i=5"
NODE_ADD_COUNTER = "ns=2;i=6"

NODE_SUB = "ns=2;i=7"
NODE_COUNT_SUB = "ns=2;i=10"
NODE_SUB_COUNTER = "ns=2;i=11"

NODE_DIV = "ns=2;i=12"
NODE_COUNT_DIV = "ns=2;i=15"
NODE_DIV_COUNTER = "ns=2;i=16"

NODE_MUL = "ns=2;i=17"
NODE_COUNT_MUL = "ns=2;i=20"
NODE_MUL_COUNTER = "ns=2;i=21"


the_time = datetime.datetime.now()

url = "opc.tcp://localhost:48400"

client = Client(url)

client.connect()
root_node = client.get_node(ROOT_NODE)

print("Client verbunden", the_time)
print("-------------------------------------------------------------")
z1 = float(input("Bitte Zahl 1 eingeben "))
z2 = float(input("Bitte Zahl 2 eingeben "))
print("-------------------------------------------------------------")
add_node = client.get_node(NODE_ADD)
sub_node = client.get_node(NODE_SUB)
div_node = client.get_node(NODE_DIV)
mul_node = client.get_node(NODE_MUL)

result_add = root_node.call_method(add_node, z1, z2)
print(f"{z1} + {z2} = {result_add} ==?== {z1 + z2}")
check_add = "correct" if result_add == (z1 + z2) else "wrong"
print(f"the result is {check_add}")

result_sub = root_node.call_method(sub_node, z1, z2)
print(f"{z1} - {z2} = {result_sub} ==?== {z1 - z2}")
check_sub = "correct" if result_sub == (z1 - z2) else "wrong"
print(f"the result is {check_sub}")

result_mul = root_node.call_method(mul_node, z1, z2)
print(f"{z1} * {z2} = {result_mul} ==?== {z1 * z2}")
check_mul = "correct" if result_mul == (z1 * z2) else "wrong"
print(f"the result is {check_mul}")

result_div = root_node.call_method(div_node, z1, z2)
print(f"{z1} / {z2} = {result_div} ==?== {z1 / z2}")
check_div = "correct" if result_div == (z1 / z2) else "wrong"
print(f"the result is {check_div}")
print("-------------------------------------------------------------")
client.get_node(NODE_COUNT_ADD).set_value(True)
client.get_node(NODE_COUNT_SUB).set_value(True)
client.get_node(NODE_COUNT_DIV).set_value(True)
client.get_node(NODE_COUNT_MUL).set_value(True)

for i in range(1000):
    result_add = root_node.call_method(add_node, z1, z2)
    result_sub = root_node.call_method(sub_node, z1, z2)
    result_mul = root_node.call_method(mul_node, z1, z2)
    result_div = root_node.call_method(div_node, z1, z2)

counter_add = client.get_node(NODE_ADD_COUNTER).get_value()
print(f"counter add = {counter_add}")

counter_sub = client.get_node(NODE_SUB_COUNTER).get_value()
print(f"counter sub = {counter_sub}")

counter_div = client.get_node(NODE_DIV_COUNTER).get_value()
print(f"counter div = {counter_div}")

counter_mul = client.get_node(NODE_MUL_COUNTER).get_value()
print(f"counter mul = {counter_mul}")

print("-------------------------------------------------------------")
## counters turned off
client.get_node(NODE_COUNT_ADD).set_value(False)
client.get_node(NODE_COUNT_SUB).set_value(False)
client.get_node(NODE_COUNT_DIV).set_value(False)
client.get_node(NODE_COUNT_MUL).set_value(False)

## try to reset counters - should fail because these nodes are not writeable
try:
    client.get_node(NODE_ADD_COUNTER).set_value(0)
except Exception as e:
    print(f"cannot reset add counter")

try:
    client.get_node(NODE_SUB_COUNTER).set_value(0)
except Exception as e:
    print(f"cannot reset sub counter")

try:
    client.get_node(NODE_MUL_COUNTER).set_value(0)
except Exception as e:
    print(f"cannot reset mul counter")

try:
    client.get_node(NODE_DIV_COUNTER).set_value(0)
except Exception as e:
    print(f"cannot reset div counter")

print("-------------------------------------------------------------")
## call methods 1000 times
for i in range(1000):
    result_add = root_node.call_method(add_node, z1, z2)
    result_sub = root_node.call_method(sub_node, z1, z2)
    result_mul = root_node.call_method(mul_node, z1, z2)
    result_div = root_node.call_method(div_node, z1, z2)

## read conters and print values
counter_add = client.get_node(NODE_ADD_COUNTER).get_value()
print(f"counter add = {counter_add}")

counter_sub = client.get_node(NODE_SUB_COUNTER).get_value()
print(f"counter sub = {counter_sub}")

counter_div = client.get_node(NODE_DIV_COUNTER).get_value()
print(f"counter div = {counter_div}")

counter_mul = client.get_node(NODE_MUL_COUNTER).get_value()
print(f"counter mul = {counter_mul}")

## random times



client.disconnect()
exit(0)