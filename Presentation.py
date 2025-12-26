from manim import *
from manim_slides.slide import ThreeDSlide
import random

from util.slide_number import SlideNumber
from util.table_of_contents import show_toc
from src.Ali import ali
from src.Parsa import parsa

Text.set_default(font="Consolas") 

toc_items = [
    "1. The Black Box Problem",
    "2. Explainability Approaches",
    "3. Transformers & Attention",
    "4. Sparse Models & Sparsification",
    "5. Model Circuits & Interpretability"
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

        references_title = Tex(r"\section*{References}", font_size=48).to_edge(UP).scale(0.8)
        self.play(Write(references_title))

        ref1 = Tex(r"""
        \begin{flushleft}
        \hangindent=1.5em\hangafter=1
        [1] F. K. Došilović, M. Brčić, and N. Hlupić, ``Explainable artificial intelligence: A survey,'' in \textit{Proc. 41st Int. Conv. Information and Communication Technology, Electronics and Microelectronics (MIPRO)}, pp. 0210-0215, 2018.
        \end{flushleft}
        """, font_size=26)

        ref2 = Tex(r"""
        \begin{flushleft}
        \hangindent=1.5em\hangafter=1
        [2]  L. Bereska and E. Gavves, ``Mechanistic interpretability for AI safety—A review,'' \textit{arXiv preprint arXiv:2404.14082}, 2024.
        \end{flushleft}
        """, font_size=26)

        ref3 = Tex(r"""
        \begin{flushleft}
        \hangindent=1.5em\hangafter=1
        [3] L. Gao, A. Rajaram, J. Coxon, S. V. Govande, B. Baker, and D. Mossing, ``Weight-sparse transformers have interpretable circuits,'' \textit{arXiv preprint arXiv:2511.13653}, 2025.
        \end{flushleft}
        """, font_size=26)

        # Arrange references
        refs = VGroup(ref1, ref2, ref3).arrange(DOWN, aligned_edge=LEFT, buff=1).next_to(references_title, DOWN, buff=0.5)

        self.play(Write(refs))

        self.next_slide()

        