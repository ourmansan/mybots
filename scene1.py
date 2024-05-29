from manim import *
import os
import sys

class StickMan(VGroup):
    def __init__(self, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        self.head = Circle(radius=0.1, color=color, fill_opacity=1).shift(UP * 0.1)
        self.body = Line(UP * 0.1, DOWN * 0.5, color=color)
        self.left_leg = Line(DOWN * 0.5, DOWN * 0.8, color=color)
        self.right_leg = Line(DOWN * 0.5, DOWN * 0.8, color=color)
        self.left_leg.shift(LEFT * 0.05)
        self.right_leg.shift(RIGHT * 0.05)
        self.add(self.head, self.body, self.left_leg, self.right_leg)

    def walk(self, direction, distance):
        return self.animate(shift=direction * distance)

class UserInitiatesDeployment(Scene):
    def construct(self):
        # Define stickman representing the user
        stickman = StickMan(color=BLUE)
        stickman.move_to(3 * LEFT + UP * 1.5)
        stickman_text = Text("User", color=WHITE).next_to(stickman, DOWN)

        # Define text editor window
        text_editor_window = Rectangle(width=4, height=3, color=WHITE, fill_opacity=1)
        text_editor_label = Text("Text Editor", color=WHITE).next_to(text_editor_window, UP)

        # Define YAML code
        yaml_code = Text("""
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
""", color=RED).scale(0.2).move_to(text_editor_window)

        # Define Kubectl CLI icon
        kubectl_cli_icon = Circle(radius=0.5, color=RED, fill_opacity=1).move_to(3 * RIGHT)
        kubectl_cli_text = Text("Kubectl CLI", color=WHITE).scale(0.5).next_to(text_editor_window, DOWN)

        # Animation
        self.play(Create(stickman), Write(stickman_text))
        self.wait(1)
        self.play(Transform(stickman, text_editor_window), Write(text_editor_label))
        self.wait(1)
        self.play(FadeIn(kubectl_cli_icon), Write(kubectl_cli_text))
        self.wait(1)
        self.play(Write(yaml_code))  # Bring YAML code to foreground
        self.wait(2)

if __name__ == "__main__":
    module_name = os.path.abspath(sys.argv[0])
    interactive = "-i" in sys.argv
    if interactive:
        sys.argv.remove("-i")
    if len(sys.argv) > 1 and sys.argv[1] == "Scene":
        sys.argv.pop(1)
        module = __import__(module_name.split("/")[-1].replace(".py", ""))
        scene = module.UserInitiatesDeployment()
        if interactive:
            scene.interact()
        else:
            scene.render()
    else:
        if interactive:
            from manim import cli
            cli.main_window.main()
        else:
            module = __import__(module_name.split("/")[-1].replace(".py", ""))
            scenes = [module.UserInitiatesDeployment]
            for Scene in scenes:
                scene = Scene()
                scene.render()
