import matplotlib.pyplot as plt

x = range(1,10)
y = []
for value in x:
	y.append(value * 3 + 2)
plt.plot(range(1,10),y)
plt.plot(range(1,10),y,color='red',linewidth=2,linestyle=':')
plt.show()
