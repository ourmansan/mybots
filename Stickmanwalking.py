import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

class Scene:
    def __init__(self, ax):
        self.ax = ax
        self.stickman, = ax.plot([], [], lw=2, color='black')
        self.head = plt.Circle((0, 0), 0.1, fill=False, lw=2, color='black')
        ax.add_patch(self.head)
        self.computer_screen = Rectangle((0, 0), 0, 0, fill=True, color='grey')
        ax.add_patch(self.computer_screen)
        self.text_editor = Rectangle((0, 0), 0, 0, fill=True, color='white')
        ax.add_patch(self.text_editor)
        self.yaml_text = ax.text(0, 0, '', fontsize=10, color='black', ha='left', va='top')
        self.kubectl_window = Rectangle((0, 0), 0, 0, fill=True, color='white')
        ax.add_patch(self.kubectl_window)
        self.kubectl_text = ax.text(0, 0, '', fontsize=10, color='black', ha='left', va='top')
    
    def init_draw(self):
        self.stickman.set_data([], [])
        self.head.center = (0, 0)
        self.computer_screen.set_xy((0, 0))
        self.computer_screen.set_width(0)
        self.computer_screen.set_height(0)
        self.text_editor.set_xy((0, 0))
        self.text_editor.set_width(0)
        self.text_editor.set_height(0)
        self.yaml_text.set_position((0, 0))
        self.yaml_text.set_text('')
        self.kubectl_window.set_xy((0, 0))
        self.kubectl_window.set_width(0)
        self.kubectl_window.set_height(0)
        self.kubectl_text.set_position((0, 0))
        self.kubectl_text.set_text('')
        return (self.stickman, self.head, self.computer_screen, self.text_editor, 
                self.yaml_text, self.kubectl_window, self.kubectl_text)

    def update(self, i):
        # Stickman
        if i < 20:
            # Initial stickman drawing
            x = [0.5, 0.5]
            y = [0.1, 0.7]
            self.head.center = (0.5, 0.8)
            self.stickman.set_data(x, y)
        elif i < 40:
            # Adding arms and legs
            arm_swing = 0.2 * np.sin(i / 5.0)
            left_arm_x = [0.5, 0.3]
            left_arm_y = [0.6, 0.6 + arm_swing]
            right_arm_x = [0.5, 0.7]
            right_arm_y = [0.6, 0.6 - arm_swing]
            leg_swing = 0.2 * np.cos(i / 5.0)
            left_leg_x = [0.5, 0.4]
            left_leg_y = [0.1, 0.1 - leg_swing]
            right_leg_x = [0.5, 0.6]
            right_leg_y = [0.1, 0.1 + leg_swing]
            self.stickman.set_data(
                [0.5, 0.5] + left_arm_x + right_arm_x + left_leg_x + right_leg_x, 
                [0.1, 0.7] + left_arm_y + right_arm_y + left_leg_y + right_leg_y)
        elif i < 60:
            # Computer screen
            self.computer_screen.set_xy((0.3, 0.2))
            self.computer_screen.set_width(0.4)
            self.computer_screen.set_height(0.4)
        elif i < 80:
            # Text editor window
            self.text_editor.set_xy((0.35, 0.25))
            self.text_editor.set_width(0.3)
            self.text_editor.set_height(0.3)
        elif i < 100:
            # YAML file content
            yaml_content = """apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mycontainer
    image: myimage"""
            self.yaml_text.set_position((0.36, 0.54))
            self.yaml_text.set_text(yaml_content)
        elif i < 120:
            # Kubectl window
            self.kubectl_window.set_xy((0.35, 0.1))
            self.kubectl_window.set_width(0.3)
            self.kubectl_window.set_height(0.1)
        elif i < 140:
            # Kubectl command
            kubectl_command = "kubectl apply -f mypod.yaml"
            self.kubectl_text.set_position((0.36, 0.15))
            self.kubectl_text.set_text(kubectl_command)
        return (self.stickman, self.head, self.computer_screen, self.text_editor, 
                self.yaml_text, self.kubectl_window, self.kubectl_text)

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

scene = Scene(ax)

# Create animation
ani = animation.FuncAnimation(fig, scene.update, frames=150, init_func=scene.init_draw, interval=100, blit=True)

# Save the animation as an mp4 file
ani.save('deployment_scene.mp4', writer='ffmpeg')

# Display the plot
plt.show()
