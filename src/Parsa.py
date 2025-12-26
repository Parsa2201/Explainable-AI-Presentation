from manim import *
from manim_slides.slide import ThreeDSlide

from util.slide_number import SlideNumber
from src.Transformer import TransformerSlides
from src.SparseModel import SparseModelSlides
from src.ModelCircuit import ModelCircuitSlides

class TitleUtil:
    def __init__(self, scene):
        self.scene = scene
        self.title = None

    def show(self, text):
        title = Tex(text, font_size=48, color=BLUE).to_edge(UP)

        if self.title is None:
            self.scene.play(Write(title))
        else:
            self.scene.play(ReplacementTransform(self.title, title))

        self.title = title

    def end(self):
        self.play(Unwrite(self.title))
        self.title = None

def parsa(scene: ThreeDSlide, slide_number: SlideNumber):
    # what_is_attention_title = Tex(r"\section*{What is Attention?}", font_size=48, color=BLUE).to_edge(UP)
    # scene.play(Write(what_is_attention_title))
    title_util = TitleUtil(scene)
    title_util.show(r"\section*{What is Attention?}")
    t = TransformerSlides(scene)
    t.play_slide_one(title_util.title)

    slide_number.incr()
    # transformer_title = Tex(r"\section*{Simplified Transformer}", font_size=48, color=BLUE).to_edge(UP)
    # scene.play(ReplacementTransform(what_is_attention_title, transformer_title))
    title_util.show(r"\section*{Simplified Transformer}")
    t.play_slide_two()

    slide_number.incr()
    # superposition_title = Tex(r"\section*{Solve superposition via sparsity}", font_size=48, color=BLUE).to_edge(UP)
    # scene.play(ReplacementTransform(transformer_title, superposition_title))
    title_util.show(r"\section*{Solve superposition via sparsity}")
    s = SparseModelSlides(scene)
    s.play_slide_one()

    slide_number.incr()
    # how_to_sparse_title = Tex(r"\section*{How to sparse a model?}", font_size=48, color=BLUE).to_edge(UP)
    # scene.play(ReplacementTransform(superposition_title, how_to_sparse_title))
    title_util.show(r"\section*{How to make the model sparse?}")
    s.play_slide_two()

    slide_number.incr()
    # extracting_circuit_title = Tex(r"\section*{Extracting circuit}", font_size=48, color=BLUE).to_edge(UP)
    # scene.play(ReplacementTransform(how_to_sparse_title, extracting_circuit_title))
    s.play_slide_three()

    slide_number.incr()
    title_util.show(r"\section*{Extracting circuit}")
    s.play_slide_four()

    slide_number.incr()
    title_util.show(r"\section*{From circuit to explanation example}")

    m = ModelCircuitSlides(scene)
    m.show_circuit_from_pdf()

    title_util.end()