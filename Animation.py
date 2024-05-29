import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the figure, axis, and plot element we want to animate
fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 100)
line, = ax.plot(x, np.sin(x))

# Initialization function: plot the background of each frame
def init():
    line.set_ydata(np.sin(x))
    return line,

# Animation function: this is called sequentially
def animate(i):
    line.set_ydata(np.sin(x + i / 10.0))  # Update the data
    return line,

# Call the animator
ani = animation.FuncAnimation(
    fig, animate, init_func=init, frames=200, interval=20, blit=True
)

# Save the animation as an mp4 file
ani.save('sine_wave.mp4', writer='ffmpeg')

# Display the plot
plt.show()
