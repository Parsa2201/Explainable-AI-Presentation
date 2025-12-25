from manim import *

class SlideNumber:
    def __init__(self, scene, slide_count=1):
        self.slide_num = 1
        self.scene = scene
        self.slide_count = slide_count
        self.slide_text = Text(f"{self.slide_num}/{slide_count}", font_size=24, t2c={f"/{slide_count}": GRAY}).to_corner(DR)
        scene.add_fixed_in_frame_mobjects(self.slide_text)
        scene.play(Write(self.slide_text))

    def incr(self):
        self.slide_num += 1
        self.new_text = Text(f"{self.slide_num}/{self.slide_count}", font_size=24, t2c={f"/{self.slide_count}": GRAY}).to_corner(DR)
        self.scene.add_fixed_in_frame_mobjects(self.new_text)
        self.scene.remove(self.slide_text)
        self.scene.add(self.new_text)
        # self.scene.play(ReplacementTransform(self.slide_text, self.new_text))
        # self.scene.wait(0.5)
        self.slide_text = self.new_text  # update reference

    def end(self):
        self.scene.remove(self.slide_text)