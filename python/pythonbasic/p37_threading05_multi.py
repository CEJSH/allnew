import threading

def example():
    for i in range(1, 10):
        print(i)

threading.Thread(target=example).start()
threading.Thread(target=example).start()