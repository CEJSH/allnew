a = int(input("Input the First Number : "))
b = int(input("Input the Second Number : "))

print("Max is %d" % a) if a > b else print("Max is %d" % b)

max_value = a if a > b else b
print(f"Max is {max_value}")

