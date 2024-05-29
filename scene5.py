from manim import *
import os
import sys
import random

class PodCreationOnWorkerNodes(Scene):
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

        # Pod creation components
        kubelet_icon = Square(side_length=0.5, color=PURPLE, fill_opacity=1)
        kubelet_text = Text("Kubelet", color=WHITE).scale(0.3).next_to(kubelet_icon, DOWN)

        container_runtime_icon = Square(side_length=0.5, color=ORANGE, fill_opacity=1)
        container_runtime_text = Text("Container Runtime", color=WHITE).scale(0.3).next_to(container_runtime_icon, DOWN)

        container_image_registry_icon = Circle(radius=0.5, color=GREY, fill_opacity=1)
        container_image_registry_text = Text("Image Registry", color=WHITE).scale(0.3).next_to(container_image_registry_icon, DOWN)

        # Set positions
        api_server_icon.move_to(3 * LEFT + 2 * UP)
        api_server_text.move_to(api_server_icon.get_center() + DOWN * 0.75)
        notification.move_to(api_server_icon.get_center() + RIGHT * 2)
        notification_text.next_to(notification, DOWN)
        scheduler_icon.move_to(notification.get_center() + RIGHT * 2)
        scheduler_text.move_to(scheduler_icon.get_center() + DOWN * 0.75)
        kubelet_icon.next_to(worker_nodes[2], UP, buff=1)
        kubelet_text.next_to(kubelet_icon, DOWN)
        container_runtime_icon.next_to(kubelet_icon, RIGHT, buff=1)
        container_runtime_text.next_to(container_runtime_icon, DOWN)
        container_image_registry_icon.next_to(container_runtime_icon, RIGHT, buff=1.5)
        container_image_registry_text.next_to(container_image_registry_icon, DOWN)

        # Animation
        self.play(GrowFromCenter(api_server_icon), Write(api_server_text))
        self.wait(0.5)
        self.play(GrowFromCenter(notification), Write(notification_text))
        self.wait(0.5)
        self.play(GrowFromCenter(scheduler_icon), Write(scheduler_text))
        self.wait(0.5)
        self.play(GrowFromCenter(worker_nodes), Write(worker_text))
        self.wait(0.5)
        self.play(
            notification.animate.shift(scheduler_icon.get_center() - notification.get_center()),
            run_time=2
        )
        self.play(FadeOut(notification), FadeOut(notification_text))

        # Select a random worker node
        selected_node_index = random.randint(0, len(worker_nodes) - 1)
        worker_nodes[selected_node_index][0].set_color(GREEN)
        checkmark = Text("✓", color=GREEN).scale(0.5).next_to(worker_nodes[selected_node_index][0], UP)
        self.play(
            ApplyMethod(worker_nodes[selected_node_index][0].set_color, GREEN),
            Write(checkmark),
            run_time=1
        )
        self.wait(1)

        # Show Kubelet and Container Runtime interaction
        self.play(GrowFromCenter(kubelet_icon), Write(kubelet_text))
        self.play(GrowFromCenter(container_runtime_icon), Write(container_runtime_text))

        # Arrow from API Server to chosen worker node
        arrow_to_worker = Arrow(api_server_icon.get_right(), worker_nodes[selected_node_index][0].get_top(), buff=0.1)
        self.play(Create(arrow_to_worker), run_time=2)

        # Arrow from Container Image Registry to Container Runtime
        arrow_to_runtime = Arrow(container_image_registry_icon.get_left(), container_runtime_icon.get_right(), buff=0.1)
        self.play(GrowFromCenter(container_image_registry_icon), Write(container_image_registry_text), run_time=2)
        self.play(Create(arrow_to_runtime), run_time=2)

        # Image moving from Container Image Registry to Container Runtime with label
        container_image = Rectangle(width=0.2, height=0.2, color=WHITE, fill_opacity=1)
        container_image_label = Text("Image", color=RED).scale(0.2).next_to(container_image, UP)
        container_image.move_to(container_image_registry_icon.get_center() + LEFT * 0.75)
        self.play(GrowFromCenter(container_image), Write(container_image_label), run_time=2)
        self.play(container_image.animate.move_to(container_runtime_icon.get_center()), container_image_label.animate.move_to(container_runtime_icon.get_center() + UP * 0.2), run_time=4)

        # Container image converts to pods inside the selected worker node
        pod_container = VGroup()
        for i in range(10):
            pod = Rectangle(width=0.1, height=0.1, color=WHITE, fill_opacity=1)
            pod_label = Text("Pod", color=RED).scale(0.1).move_to(pod.get_center())
            pod_container.add(VGroup(pod, pod_label))
        
        self.play(
            FadeOut(container_image),
            *[FadeIn(pod_container[i]) for i in range(10)],
            run_time=3
        )

        # Move pods into the selected worker node
        for i, pod in enumerate(pod_container):
            self.play(pod.animate.move_to(worker_nodes[selected_node_index][1][i].get_center()), run_time=2)

        # Animation of square packets sent by Kubelet back to the API Server
        packets = VGroup()
        for i in range(10):
            packet = Square(side_length=0.1, color=BLUE, fill_opacity=1)
            packets.add(packet)

        packets.arrange(RIGHT, buff=0.1)
        packets.next_to(api_server_icon, DOWN, buff=0.5)
        self.play(FadeIn(packets), run_time=2)
        self.wait(1)

if __name__ == "__main__":
    module_name = os.path.abspath(sys.argv[0])
    interactive = "-i" in sys.argv
    if interactive:
        sys.argv.remove("-i")
    if len(sys.argv) > 1 and sys.argv[1] == "PodCreationOnWorkerNodes":
        sys.argv.pop(1)
        module = __import__(module_name.split("/")[-1].replace(".py", ""))
        scene = module.PodCreationOnWorkerNodes()
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
            scenes = [module.PodCreationOnWorkerNodes]
            for Scene in scenes:
                scene = Scene()
                scene.render()
