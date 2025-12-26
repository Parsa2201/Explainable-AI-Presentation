from manim import *
from manim_slides.slide import ThreeDSlide

from util.slide_number import SlideNumber
from src.Transformer import TransformerSlides
from src.SparseModel import SparseModelSlides

def parsa(scene: ThreeDSlide, slide_number: SlideNumber):
    title = Tex(r"\section*{What is Attention?}", font_size=48, color=BLUE).to_edge(UP)
    scene.play(Write(title))
    t = TransformerSlides(scene, title)
    t.play_slide_one()
    slide_number.incr()
    t.play_slide_two()
    slide_number.incr()

    s = SparseModelSlides(scene)
    s.play_slide_one()
    s.play_slide_two()
    s.play_slide_three()
    s.play_slide_four()