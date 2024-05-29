from manim import *

class ServiceCreation(Scene):
    def construct(self):
        # Define icons
        api_server_icon = Rectangle(width=2, height=2, color=BLUE, fill_opacity=1)
        api_server_text = Text("API Server", color=WHITE).next_to(api_server_icon, DOWN)

        etcd_icon = Rectangle(width=2, height=2, color=RED, fill_opacity=1)
        etcd_text = Text("etcd", color=WHITE).next_to(etcd_icon, DOWN)

        cloud_icon = Circle(radius=1, color=LIGHT_GREY, fill_opacity=1)
        arrows = VGroup(
            Arrow(LEFT, RIGHT, color=WHITE),
            Arrow(UP, DOWN, color=WHITE),
            Arrow(DL, UR, color=WHITE),
            Arrow(DR, UL, color=WHITE),
        ).arrange(RIGHT, buff=0.2).move_to(cloud_icon)

        # Set positions
        api_server_icon.move_to(3 * LEFT)
        api_server_text.move_to(api_server_icon.get_center() + DOWN * 2)
        etcd_icon.move_to(3 * RIGHT)
        etcd_text.move_to(etcd_icon.get_center() + DOWN * 2)
        cloud_icon.move_to(UP * 2)

        # Animation
        self.play(GrowFromCenter(api_server_icon), Write(api_server_text))
        self.wait(0.5)
        self.play(GrowFromCenter(etcd_icon), Write(etcd_text))
        self.wait(0.5)
        self.play(FadeIn(cloud_icon), Create(arrows))
        self.wait(1)

if __name__ == "__main__":
    module = ServiceCreation()
    module.render()

