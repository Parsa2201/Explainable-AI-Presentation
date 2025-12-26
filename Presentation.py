from manim import *
from manim_slides.slide import ThreeDSlide
import random

from util.slide_number import SlideNumber
from util.table_of_contents import show_toc
from src.Ali import ali
from src.Parsa import parsa

Text.set_default(font="Consolas") 

toc_items = [
    "1. Introduction",
    # new items come here
]

class Presentation(ThreeDSlide):
    def construct(self):
        t1 = Tex("Explainable AI", font_size=42)
        t2 = Tex("in Sparse Transformers", font_size=42).next_to(t1, DOWN, buff=0.5)
        t3 = Tex("Presenters: Parsa Salamatipour \& Ali Hasan Yazdi", font_size=20).next_to(t2, DOWN, buff=1)
        t4 = Tex("Professor: Dr. Nazerfard", font_size=20).next_to(t3, DOWN, buff=0.2)
        title = VGroup(
            t1, t2, t3, t4
        ).move_to(ORIGIN)

        # Create a small cube
        cube = Cube(side_length=0.5, fill_opacity=0.5).scale(4)
        # cube.to_edge(RIGHT + DOWN) 

        self.play(Write(title))
        self.wait(0.5)
        self.next_slide()

        self.play(Unwrite(title))
        self.wait(1)

        # self.next_slide()

        show_toc(self, toc_items)

        slide_number = SlideNumber(self)

        ali(self, slide_number)
        parsa(self, slide_number)

        slide_number.end()