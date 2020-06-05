from MapsGenerator import ai_board
import numpy as np
from OrderedAlphaBetaPlayer import OrderedAlphaBetaPlayer
from AlphaBetaPlayer import AlphaBetaPlayer
from MinimaxPlayer import MinimaxPlayer
import matplotlib.pyplot as plt


times = []
depths = []
for t in np.linspace(0.1, 3, 50):
    player = MinimaxPlayer()
    player.set_game_params(ai_board.copy())
    d = player.make_move(t)
    times.append(t)
    depths.append(d)
plt.xlabel('time')
plt.ylabel('depths')
plt.title('MinimaxPlayer')
plt.scatter(times, depths)
plt.show()

times = []
depths = []
for t in np.linspace(0.1, 3, 50):
    player = AlphaBetaPlayer()
    player.set_game_params(ai_board.copy())
    d = player.make_move(t)
    times.append(t)
    depths.append(d)
plt.xlabel('time')
plt.ylabel('depths')
plt.title('AlphaBetaPlayer')
plt.scatter(times, depths)
plt.show()

times = []
depths = []
for t in np.linspace(0.1, 3, 50):
    player = OrderedAlphaBetaPlayer()
    player.set_game_params(ai_board.copy())
    d = player.make_move(t)
    times.append(t)
    depths.append(d)
plt.xlabel('time')
plt.ylabel('depths')
plt.title('OrderedAlphaBetaPlayer')
plt.scatter(times, depths)
plt.show()