from src.demo.tasks import add
import time

result = add.delay(4, 4)
time.sleep(6)
print(result.ready())
print(result.get())
