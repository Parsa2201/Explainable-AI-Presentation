from manim import *

class SlideNumber:
    def __init__(self, scene):
        self.slide_num = 1
        self.scene = scene
        self.slide_text = Text(f"{self.slide_num}/19", font_size=24, t2c={"/19": GRAY}).to_corner(DR)
        scene.add_fixed_in_frame_mobjects(self.slide_text)
        scene.play(Write(self.slide_text))

    def incr(self):
        self.slide_num += 1
        self.new_text = Text(f"{self.slide_num}/19", font_size=24, t2c={"/19": GRAY}).to_corner(DR)
        self.scene.add_fixed_in_frame_mobjects(self.new_text)
        self.scene.remove(self.slide_text)
        self.scene.add(self.new_text)
        # self.scene.play(ReplacementTransform(self.slide_text, self.new_text))
        # self.scene.wait(0.5)
        self.slide_text = self.new_text  # update reference

    def end(self):
        self.scene.remove(self.slide_text)