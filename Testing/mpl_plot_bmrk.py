import numpy as np
import matplotlib.pyplot as plt
#tbs = Torch Battery Saver, tpi = Torch plugged in, trd = Torch random data // rtbs = TRT battery saver, rtpi = TRT plugged in, rtrd = TRT random data
data = {"Torch Low Power": 18.92, "Torch Charging": 28.15, "Torch Random": 17.86, "TRT Low Power": 137.32, 'TRT Charging': 191.95, 'TRT Random': 178.68}
tests = list(data.keys())
results = list(data.values())

fig = plt.figure(figsize= (10, 5))
plt.bar(tests[:3], results[:3], color='red', width=0.5)
plt.bar(tests[3:], results[3:], color='green', width=0.5)

plt.xlabel("Benchmarks")
plt.ylabel("Framerate")
plt.title("TensorRT vs Torch in Low Power, Plugged In, and Random Data.")
plt.show()
fig.savefig("tensorRT_benchmark.png")