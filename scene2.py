from manim import *
import os
import sys

class ValidationAndStorage(Scene):
    def construct(self):
        # Define icons
        yaml_file_icon = Rectangle(width=1, height=1, color=WHITE, fill_opacity=1).scale(0.5)
        yaml_file_text = Text("YAML File", color=YELLOW).scale(0.5)
        api_server_icon = Rectangle(width=2, height=2, color=BLUE, fill_opacity=1)
        api_server_text = Text("API Server", color=WHITE).next_to(api_server_icon, DOWN)
        checkmark = Text("✓", color=GREEN).scale(2)
        etcd_icon = Rectangle(width=2, height=2, color=RED, fill_opacity=1)
        etcd_text = Text("etcd", color=WHITE).next_to(etcd_icon, DOWN)

        # Set positions
        yaml_file_icon.move_to(3 * LEFT)
        yaml_file_text.next_to(yaml_file_icon, DOWN)
        api_server_icon.move_to(2 * LEFT)
        checkmark.next_to(api_server_icon, RIGHT)
        etcd_icon.move_to(6 * RIGHT)
        etcd_text.next_to(etcd_icon, DOWN)

        # Animation
        self.play(Create(yaml_file_icon), Write(yaml_file_text))
        self.play(yaml_file_icon.animate.shift(ORIGIN - yaml_file_icon.get_left()))
        self.play(yaml_file_text.animate.move_to(yaml_file_icon))
        self.play(GrowFromCenter(api_server_icon), Write(api_server_text))
        self.play(GrowFromCenter(checkmark))
        self.play(GrowFromCenter(etcd_icon))
        self.play(Write(etcd_text))
        self.play(TransformFromCopy(yaml_file_icon, yaml_file_icon.copy().move_to(api_server_icon)))
        self.play(TransformFromCopy(yaml_file_icon, yaml_file_icon.copy().move_to(etcd_icon)))
        self.play(TransformFromCopy(yaml_file_text, yaml_file_text.copy().move_to(etcd_icon)))
        self.wait(1)

if __name__ == "__main__":
    module_name = os.path.abspath(sys.argv[0])
    interactive = "-i" in sys.argv
    if interactive:
        sys.argv.remove("-i")
    if len(sys.argv) > 1 and sys.argv[1] == "Scene":
        sys.argv.pop(1)
        module = __import__(module_name.split("/")[-1].replace(".py", ""))
        scene = module.ValidationAndStorage()
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
            scenes = [module.ValidationAndStorage]
            for Scene in scenes:
                scene = Scene()
                scene.render()
