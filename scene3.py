import os
import sys
import random
from manim import *

class SchedulingPods(Scene):
    def construct(self):
        # Define icons
        api_server_icon = Rectangle(width=1, height=1, color=BLUE, fill_opacity=1)
        api_server_text = Text("API Server", color=WHITE).scale(0.5).next_to(api_server_icon, DOWN)
        
        notification = Rectangle(width=0.25, height=0.25, color=YELLOW, fill_opacity=1).next_to(api_server_icon, RIGHT, buff=1.5)
        notification_text = Text("Notification", color=WHITE).scale(0.3).next_to(notification, DOWN)
        
        scheduler_icon = Rectangle(width=1, height=1, color=GREEN, fill_opacity=1).next_to(notification, RIGHT, buff=1.5)
        scheduler_text = Text("Scheduler", color=WHITE).scale(0.5).next_to(scheduler_icon, DOWN)

        # Define worker nodes and pods
        worker_nodes = VGroup()
        for i in range(5):
            pods = VGroup(*[Rectangle(width=0.1, height=0.1, color=WHITE, fill_opacity=1) for _ in range(10)])
            pods.arrange_in_grid(rows=2, buff=0.05)
            node = Rectangle(width=1, height=1.5, color=BLACK, fill_opacity=1)
            node_group = VGroup(node, pods).arrange(DOWN, buff=0.1)
            worker_nodes.add(node_group)

        worker_nodes.arrange(RIGHT, buff=1.5)
        worker_nodes.to_edge(DOWN)
        worker_text = Text("Worker Nodes", color=WHITE).scale(0.5).next_to(worker_nodes, DOWN)

        # Animation
        self.play(GrowFromCenter(api_server_icon), Write(api_server_text))
        self.play(GrowFromCenter(notification), Write(notification_text))
        self.wait(0.5)
        self.play(GrowFromCenter(scheduler_icon), Write(scheduler_text))
        self.wait(0.5)
        self.play(GrowFromCenter(worker_nodes), Write(worker_text))
        self.wait(0.5)
        self.play(
            notification.animate.shift(scheduler_icon.get_center() - notification.get_center()),
            run_time=1.5
        )
        self.play(FadeOut(notification), FadeOut(notification_text))

        # Select a random worker node
        selected_node_index = random.randint(0, len(worker_nodes) - 1)
        worker_nodes[selected_node_index][0].set_color(GREEN)
        checkmark = Text("✓", color=GREEN).scale(0.5).next_to(worker_nodes[selected_node_index][0], UP)
        self.play(
            ApplyMethod(worker_nodes[selected_node_index][0].set_color, GREEN),
            Write(checkmark),
            run_time=0.5
        )
        self.wait(1)

if __name__ == "__main__":
    module_name = os.path.abspath(sys.argv[0])
    interactive = "-i" in sys.argv
    if interactive:
        sys.argv.remove("-i")
    if len(sys.argv) > 1 and sys.argv[1] == "SchedulingPods":
        sys.argv.pop(1)
        module = __import__(module_name.split("/")[-1].replace(".py", ""))
        scene = module.SchedulingPods()
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
            scenes = [module.SchedulingPods]
            for Scene in scenes:
                scene = Scene()
                scene.render()
