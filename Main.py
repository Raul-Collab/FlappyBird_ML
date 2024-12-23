import Game
import matplotlib.pyplot as plt
import numpy as np

MainGame = Game.Game(top_player=False)
MainGame.mainLoop()
xaxis = np.array([2, 8])
# Y axis parameter:
yaxis = np.array([4, 9])
plt.plot(xaxis, yaxis)
plt.show()