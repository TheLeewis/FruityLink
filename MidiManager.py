import pytemidi
import mido
import time

with pytemidi.Port("Porta Python Virtuale") as port:
    time.sleep(5)
    print(mido.get_output_names())
    print(mido.get_input_names())
    time.sleep(5)

print(mido.get_output_names())
print(mido.get_input_names())