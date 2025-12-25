from manim import *

def show_toc(scene, toc_items: list[str]):
    toc_title = Tex(r"\textbf{Table of Contents}", font_size=48).to_edge(UP).scale(0.8)

    toc_texts = VGroup(*[
        Text(item, font_size=28).to_edge(LEFT)
        for item in toc_items
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(toc_title, DOWN, buff=0.7)

    scene.play(Write(toc_texts), Write(toc_title))
    scene.wait(0.5)
    scene.next_slide()
    scene.play(Unwrite(toc_texts), Unwrite(toc_title))