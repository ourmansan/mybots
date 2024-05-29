import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

class Scene:
    def __init__(self, ax):
        self.ax = ax
        # Computer screen and components
        self.computer_screen = Rectangle((0.1, 0.1), 0.8, 0.8, fill=True, color='grey')
        ax.add_patch(self.computer_screen)
        self.text_editor = Rectangle((0.15, 0.5), 0.7, 0.35, fill=True, color='white')
        ax.add_patch(self.text_editor)
        self.yaml_text = ax.text(0.18, 0.82, '', fontsize=10, color='black', ha='left', va='top')
        self.kubectl_window = Rectangle((0.15, 0.2), 0.7, 0.2, fill=True, color='white')
        ax.add_patch(self.kubectl_window)
        self.kubectl_text = ax.text(0.18, 0.35, '', fontsize=10, color='black', ha='left', va='top')
    
    def init_draw(self):
        self.yaml_text.set_text('')
        self.kubectl_text.set_text('')
        return self.yaml_text, self.kubectl_text

    def update(self, i):
        if i < 100:
            # YAML file content
            yaml_content = """apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mycontainer
    image: myimage"""
            self.yaml_text.set_text(yaml_content)
        elif i < 150:
            # Highlight kubectl window
            self.kubectl_text.set_text('kubectl apply -f mypod.yaml')
        return self.yaml_text, self.kubectl_text

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

scene = Scene(ax)

# Create animation
ani = animation.FuncAnimation(fig, scene.update, frames=200, init_func=scene.init_draw, interval=50, blit=True)

# Save the animation as an mp4 file
ani.save('yaml_deployment_animation.mp4', writer='ffmpeg')

# Display the plot
plt.show()
