import matplotlib.pyplot as plt

# 2D log search
plt.plot([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], 
	[275,286,286.79,302,304,304.5,304.7,317.6,318.5,318.9,319,320.5,321.8,318.8,318.13], 'b--')

plt.annotate('2D Log Search', xy=(13,320), xytext=(13, 308), arrowprops=dict(facecolor='blue', shrink=0.05),)

# hierarchial search
plt.plot([4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], 
	[286.98,286.11,294,293.6,290,291.2,290,289.35,290.9,291,288.9,290.2,293.1,290,288.5,292.4], 'r--')
plt.annotate('Hierarchical Search', xy=(12.5, 290), xytext=(12.5, 275), arrowprops=dict(facecolor='red', shrink=0.05),)

plt.title('Experiment Results')
plt.axis([0, 20, 250, 350])
plt.xlabel('p')
plt.ylabel('execution time (seconds)')
plt.grid(True)

plt.show()
