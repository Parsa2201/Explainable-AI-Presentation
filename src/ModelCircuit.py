from manim import *
import random
import numpy as np
from manim_slides.slide import ThreeDSlide

random.seed(42)
np.random.seed(42)

# --- Configuration ---
NEURON_COLOR = WHITE
CONNECTION_COLOR = GRAY
TEXT_COLOR = WHITE
POS_COLOR = BLUE
NEG_COLOR = RED
PATH_COLOR = YELLOW
CODE_COLOR = "#A0A0A0"     # Light gray for comments
TOKEN_BOX_COLOR = "#C59942" # Gold/Brownish

class ModelCircuitSlides:
    def __init__(self, scene: ThreeDSlide):
        self.scene = scene

    def show_circuit_from_pdf(self):
        bracket_detector_circuit = ImageMobject("assets/bracket_detector_circuit.png").scale(0.8)
        self.scene.play(FadeIn(bracket_detector_circuit))
        self.scene.next_slide()
        self.scene.play(FadeOut(bracket_detector_circuit))

    def create_token(self, char, color=WHITE):
        """Creates a visual token box used in the diagram."""
        box = RoundedRectangle(corner_radius=0.1, height=0.6, width=0.5, color=TOKEN_BOX_COLOR, stroke_width=2)
        lbl = Text(str(char), font_size=24, color=color)
        return VGroup(box, lbl)

    def create_code_block(self, lines_text, font_size=18):
        """Creates syntax-highlighted code blocks."""
        code_group = VGroup()
        for line in lines_text:
            if line.strip().startswith("#"):
                color = GRAY
            elif "values" in line:
                color = WHITE
            elif "print" in line:
                color = BLUE
            else:
                color = WHITE
            text = Text(line, font="Monospace", font_size=font_size, color=color)
            code_group.add(text)
        code_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        return code_group

    def construct_circuit(self):
        """Recreates the Double Bracket Circuit diagram."""
        
        # 1. Top Section: Input Tokens
        top_text = Text("values = ", font="Monospace", font_size=24)
        t_br1 = self.create_token("[")
        t_br2 = self.create_token("[")
        t_5 = self.create_token("5")
        t_3 = self.create_token("3")
        
        input_group = VGroup(top_text, t_br1, t_br2, t_5, t_3).arrange(RIGHT, buff=0.2)
        input_group.to_edge(UP, buff=1.0)
        
        # 2. Residual Stream (Central Dashed Line)
        stream_line = DashedLine(
            start=input_group.get_bottom() + DOWN*0.2,
            end=input_group.get_bottom() + DOWN*6.0,
            color=WHITE
        )

        # 3. Layer 2: Open Bracket Detector
        # Branch point from stream
        y_l2 = stream_line.get_start()[1] - 1.0
        branch_l2 = np.array([stream_line.get_center()[0], y_l2, 0])
        
        # RMSNorm boxes
        rms1 = Rectangle(height=0.4, width=1.0, color=WHITE).move_to(branch_l2 + LEFT*1.5)
        rms1_lbl = Text("rmsnorm", font_size=12).move_to(rms1)
        
        # Attention Head Box
        attn_box = Rectangle(height=0.8, width=1.2, color=WHITE).next_to(rms1, DOWN, buff=0.5)
        attn_lbl = Text("2.attn", font_size=16).move_to(attn_box)
        
        # Wiring L2
        wire_l2_in = Line(branch_l2, rms1.get_right(), color=TOKEN_BOX_COLOR)
        wire_l2_mid = Line(rms1.get_bottom(), attn_box.get_top(), color=TOKEN_BOX_COLOR)
        
        # Add Operation (+)
        plus_circle = Circle(radius=0.15, color=WHITE).move_to([branch_l2[0], attn_box.get_center()[1], 0])
        plus_txt = Text("+", font_size=20).move_to(plus_circle)
        wire_l2_out = Line(attn_box.get_right(), plus_circle.get_left(), color=TOKEN_BOX_COLOR)

        # Annotations L2
        code_l2 = self.create_code_block([
            "# Open bracket detector",
            "values = [[7, 2, 2, 10..."
        ]).next_to(attn_box, LEFT, buff=0.5)
        
        dashed_l2 = DashedLine(LEFT*3, RIGHT*3, color=WHITE).next_to(input_group, DOWN, buff=0.5)
        dashed_l2_lbl = Text("2.attn", font="Monospace", font_size=16).next_to(dashed_l2, RIGHT)

        group_l2 = VGroup(rms1, rms1_lbl, attn_box, attn_lbl, plus_circle, plus_txt, 
                          wire_l2_in, wire_l2_mid, wire_l2_out, code_l2, dashed_l2, dashed_l2_lbl)

        # 4. Layer 4: Mechanism (Q, K, Softmax)
        y_l4 = y_l2 - 3.0
        branch_l4 = np.array([stream_line.get_center()[0], y_l4, 0])
        
        # Q K Cross
        q_node = Circle(radius=0.2, color=WHITE).move_to(branch_l4 + DOWN*0.5 + RIGHT*0.4)
        q_lbl = Text("Q", font_size=14).next_to(q_node, UP, buff=0.05)
        k_node = Circle(radius=0.2, color=WHITE).move_to(branch_l4 + DOWN*0.5 + LEFT*0.4)
        k_lbl = Text("K", font_size=14).next_to(k_node, UP, buff=0.05)
        
        cross_qk = Circle(radius=0.2, color=WHITE).move_to(branch_l4 + DOWN*0.5)
        cross_txt = MathTex(r"\times", font_size=20).move_to(cross_qk)
        
        # Softmax
        soft_box = Rectangle(height=0.4, width=1.2, color=WHITE).next_to(cross_qk, DOWN, buff=0.3)
        soft_lbl = Text("softmax", font_size=16).move_to(soft_box)
        
        # V Cross
        v_cross = Circle(radius=0.2, color=WHITE).next_to(soft_box, DOWN, buff=0.3)
        v_txt = MathTex(r"\times", font_size=20).move_to(v_cross)
        v_lbl = Text("V", font_size=14).next_to(v_cross, LEFT, buff=0.1)

        # Output Bars (Orange bars from PDF)
        bar1 = Rectangle(height=0.2, width=1.0, color=TOKEN_BOX_COLOR, fill_opacity=1).next_to(v_cross, RIGHT, buff=0.5)
        bar2 = Rectangle(height=0.2, width=0.3, color=TOKEN_BOX_COLOR, fill_opacity=1).next_to(bar1, DOWN, buff=0.1, aligned_edge=LEFT)
        out_token1 = self.create_token("]").next_to(v_cross, DOWN, buff=0.3)
        out_token2 = self.create_token("]").next_to(out_token1, DOWN, buff=0.1)

        # Annotations L4
        dashed_l4 = DashedLine(LEFT*3, RIGHT*3, color=WHITE).move_to(branch_l4 + UP*0.8)
        dashed_l4_lbl = Text("4.attn", font="Monospace", font_size=16).next_to(dashed_l4, RIGHT)
        
        code_l4 = self.create_code_block([
            "# Nesting depth",
            "values = [[1, 9, 3...",
            "",
            "# Nested list",
            "values = [[5, 3, 11..."
        ]).to_edge(LEFT).match_y(soft_box)
        
        note_right = self.create_code_block([
            "# Don't get distracted: [",
            "values = [5, 3, 11, 3, 12]]"
        ], font_size=14).to_edge(RIGHT).match_y(dashed_l4)

        group_l4 = VGroup(
            q_node, q_lbl, k_node, k_lbl, cross_qk, cross_txt, 
            soft_box, soft_lbl, v_cross, v_txt, v_lbl, 
            bar1, bar2, out_token1, out_token2,
            dashed_l4, dashed_l4_lbl, code_l4, note_right
        )

        # Animation Sequence
        self.scene.play(FadeIn(input_group), Create(stream_line))
        self.scene.play(FadeIn(group_l2))
        self.scene.play(FadeIn(group_l4))
        self.scene.wait(2)