from manim import *
from manim_slides.slide import ThreeDSlide

from util.slide_number import SlideNumber
from src.Transformer import TransformerSlides
from src.SparseModel import SparseModelSlides
from src.ModelCircuit import ModelCircuitSlides

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
    slide_number.incr()
    s.play_slide_two()
    slide_number.incr()
    s.play_slide_three()
    slide_number.incr()
    s.play_slide_four()
    slide_number.incr()

    m = ModelCircuitSlides(scene)
    m.show_circuit_from_pdf()

