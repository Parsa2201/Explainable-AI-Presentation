from manim import *
from manim_slides.slide import ThreeDSlide

from util.slide_number import SlideNumber

def ali(scene: ThreeDSlide, slide_number: SlideNumber):
    # ---------------------------
    # The Black Box Problem Scene
    # ---------------------------

    title = Tex(r"\section*{The Black Box Problem}", font_size=48, color=BLUE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title))
    scene.wait(0.5)

    # Input features on the left
    inputs_label = Text("Inputs", font_size=32, color=GREEN).shift(LEFT * 4.5 + UP * 2)

    # Create input features
    input_features = (
        VGroup(
            VGroup(
                Circle(radius=0.2, color=GREEN, fill_opacity=0.3),
                Tex(r"Age", font_size=18).next_to(ORIGIN, RIGHT, buff=0.3),
            ),
            VGroup(
                Circle(radius=0.2, color=GREEN, fill_opacity=0.3),
                Tex(r"Income", font_size=18).next_to(ORIGIN, RIGHT, buff=0.3),
            ),
            VGroup(
                Circle(radius=0.2, color=GREEN, fill_opacity=0.3),
                Tex(r"Credit", font_size=18).next_to(ORIGIN, RIGHT, buff=0.3),
            ),
            VGroup(
                Circle(radius=0.2, color=GREEN, fill_opacity=0.3),
                Tex(r"History", font_size=18).next_to(ORIGIN, RIGHT, buff=0.3),
            ),
        )
        .arrange(DOWN, buff=0.4)
        .shift(LEFT * 4.5 + DOWN * 0.5)
    )

    # Black box in the middle
    black_box = Rectangle(
        width=3,
        height=3.5,
        color=WHITE,
        fill_color=GRAY,
        fill_opacity=0.8,
        stroke_width=3,
    ).shift(ORIGIN + DOWN * 0.2)

    black_box_label = Tex(r"Black Box\\Model", font_size=24, color=WHITE)
    black_box_label.move_to(black_box.get_center() + UP * 0.8)

    question_mark = Text("?", font_size=80, color=YELLOW)
    question_mark.move_to(black_box.get_center() + DOWN * 0.3)

    # Output on the right
    outputs_label = Tex(r"\textbf{Output}", font_size=32, color=RED).shift(RIGHT * 4.5 + UP * 2)

    output_box = VGroup(
        Rectangle(width=2, height=1.2, color=RED, fill_opacity=0.3),
        Tex("Approve", font_size=24, color=GREEN).shift(UP * 0.2),
        Tex("Reject", font_size=24, color=RED).shift(DOWN * 0.2),
    ).shift(RIGHT * 4.5 + DOWN * 0.2)

    # Arrows
    input_arrows = VGroup()
    for feature in input_features:
        arrow = Arrow(
            start=feature.get_right() + RIGHT * 0.2,
            end=black_box.get_left() + LEFT * 0.1,
            color=GREEN,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        input_arrows.add(arrow)

    output_arrow = Arrow(
        start=black_box.get_right(),
        end=output_box.get_left(),
        color=RED,
        buff=0.2,
        stroke_width=4,
    )

    # Animate the scene
    scene.play(Write(inputs_label))
    scene.play(
        *[Create(feature[0]) for feature in input_features],
        *[Write(feature[1]) for feature in input_features],
        lag_ratio=0.2,
        run_time=2
    )
    scene.wait(0.3)

    scene.play(*[Create(arrow) for arrow in input_arrows], run_time=1)
    scene.wait(0.3)

    scene.play(DrawBorderThenFill(black_box), Write(black_box_label), run_time=1.5)
    scene.play(Write(question_mark), run_time=0.8)
    scene.wait(0.5)

    scene.play(Create(output_arrow), run_time=1)
    scene.play(Write(outputs_label))
    scene.play(
        Create(output_box[0]), Write(output_box[1]), Write(output_box[2]), run_time=1.5
    )

    scene.wait(1)
    scene.next_slide()

    # Fade out everything except the black box, its label, and question mark
    fade_out_objects = [
        title, inputs_label, outputs_label, output_box,
        *input_features, *input_arrows, output_arrow
    ]
    scene.play(*[FadeOut(mob) for mob in fade_out_objects], run_time=1)

    # ---------------------------
    # Black Box → Transparent Box Scene
    # ---------------------------

    # New title
    new_title = Tex(r"\section*{From Black Box to Explainable AI}", font_size=48, color=BLUE)
    new_title.to_edge(UP, buff=0.5)
    scene.play(Write(new_title))
    scene.wait(0.5)

    # Move black box to the left side
    scene.play(
        black_box.animate.shift(LEFT * 3),
        black_box_label.animate.shift(LEFT * 3),
        question_mark.animate.shift(LEFT * 3),
        run_time=1.5
    )
    scene.wait(0.3)

    # Create transparent box on the right
    transparent_box = Rectangle(
        width=3,
        height=3.5,
        color=BLUE,
        fill_color=BLUE,
        fill_opacity=0.2,
        stroke_width=3,
    ).shift(RIGHT * 3 + DOWN * 0.2)

    transparent_box_label = Tex(r"XAI\\Model", font_size=24, color=BLUE)
    transparent_box_label.move_to(transparent_box.get_center() + UP * 1.3)

    # Create explanation icons inside transparent box
    explanations = VGroup(
        Tex(r"Age", font_size=16, color=WHITE),
        Tex(r"Income", font_size=16, color=WHITE),
        Tex(r"Decision Path", font_size=16, color=WHITE),
    ).arrange(DOWN, buff=0.3).move_to(transparent_box.get_center())

    # Feature importance labels on the right
    feature_importance_label = Tex(r"Feature Importance", font_size=20, color=YELLOW)
    feature_importance_label.next_to(transparent_box, RIGHT, buff=0.3).shift(UP * 1)

    rules_label = Tex(r"Decision Rules", font_size=20, color=YELLOW)
    rules_label.next_to(transparent_box, RIGHT, buff=0.3)

    highlights_label = Tex(r"Key Factors", font_size=20, color=YELLOW)
    highlights_label.next_to(transparent_box, RIGHT, buff=0.3).shift(DOWN * 1)

    # Arrows from transparent box to explanations
    arrow_to_importance = Arrow(
        start=transparent_box.get_right() + UP * 1,
        end=feature_importance_label.get_left(),
        color=YELLOW,
        buff=0.1,
        stroke_width=2,
    )

    arrow_to_rules = Arrow(
        start=transparent_box.get_right(),
        end=rules_label.get_left(),
        color=YELLOW,
        buff=0.1,
        stroke_width=2,
    )

    arrow_to_highlights = Arrow(
        start=transparent_box.get_right() + DOWN * 1,
        end=highlights_label.get_left(),
        color=YELLOW,
        buff=0.1,
        stroke_width=2,
    )

    # Arrow from black box to transparent box (transformation arrow)
    transformation_arrow = Arrow(
        start=black_box.get_right(),
        end=transparent_box.get_left(),
        color=GREEN,
        buff=0.2,
        stroke_width=4,
    )

    # Animate the transformation
    scene.play(Create(transformation_arrow), run_time=1)
    scene.wait(0.3)

    scene.play(
        DrawBorderThenFill(transparent_box),
        Write(transparent_box_label),
        run_time=1.5
    )
    scene.wait(0.3)

    # Replace question mark with explanations
    scene.play(
        FadeOut(question_mark.copy().move_to(transparent_box.get_center())),
        *[Write(exp) for exp in explanations],
        run_time=1.5
    )
    scene.wait(0.5)

    # Show explanation arrows and labels
    scene.play(
        Create(arrow_to_importance),
        Create(arrow_to_rules),
        Create(arrow_to_highlights),
        run_time=1
    )
    scene.play(
        Write(feature_importance_label),
        Write(rules_label),
        Write(highlights_label),
        lag_ratio=0.2,
        run_time=1.5
    )

    scene.wait(0.5)
    scene.next_slide()

    scene.play(*[FadeOut(mob) for mob in scene.mobjects], run_time=1)

    # ---------------------------
    # Decision Tree Explainability Scene
    # ---------------------------
    dtree_slide(scene)
    scene.wait(0.5)
    scene.next_slide()

    scene.play(*[FadeOut(mob) for mob in scene.mobjects], run_time=1)

    # ---------------------------
    # Explainability vs Predictive Power Trade-off Scene
    # ---------------------------
    explain_predictive_slide(scene)

    scene.wait(0.5)
    scene.next_slide()
    scene.play(*[FadeOut(mob) for mob in scene.mobjects], run_time=1)

    # ---------------------------
    # Why XAI Matters Scene
    # ---------------------------
    xai_matters_slide(scene)

    scene.wait(0.5)
    scene.next_slide()
    scene.play(*[FadeOut(mob) for mob in scene.mobjects], run_time=1)

def dtree_slide(scene: ThreeDSlide):
    title = Tex(r"\section*{Inherently Explainable Models}", font_size=48, color=BLUE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title))
    scene.wait(0.5)

    # Create decision tree nodes
    # Root node
    root_node = RoundedRectangle(
        width=2.5,
        height=0.8,
        corner_radius=0.15,
        color=BLUE,
        fill_opacity=0.3,
        stroke_width=3,
    ).shift(UP * 2)

    root_label = Tex(r"Age $>$ 30?", font_size=24, color=WHITE)
    root_label.move_to(root_node.get_center())

    # Left child node (Income decision)
    left_node = RoundedRectangle(
        width=2.5,
        height=0.8,
        corner_radius=0.15,
        color=BLUE,
        fill_opacity=0.3,
        stroke_width=3,
    ).shift(LEFT * 3 + DOWN * 0.5)

    left_label = Tex(r"Income $>$ 50k?", font_size=24, color=WHITE)
    left_label.move_to(left_node.get_center())

    # Right child node (Reject)
    right_node = RoundedRectangle(
        width=2,
        height=0.8,
        corner_radius=0.15,
        color=RED,
        fill_opacity=0.4,
        stroke_width=3,
    ).shift(RIGHT * 3 + DOWN * 0.5)

    right_label = Tex(r"\textbf{Reject}", font_size=24, color=WHITE)
    right_label.move_to(right_node.get_center())

    # Left-left leaf (Approve)
    left_left_node = RoundedRectangle(
        width=2,
        height=0.8,
        corner_radius=0.15,
        color=GREEN,
        fill_opacity=0.4,
        stroke_width=3,
    ).shift(LEFT * 4.5 + DOWN * 3)

    left_left_label = Tex(r"\textbf{Approve}", font_size=24, color=WHITE)
    left_left_label.move_to(left_left_node.get_center())

    # Left-right leaf (Reject)
    left_right_node = RoundedRectangle(
        width=2,
        height=0.8,
        corner_radius=0.15,
        color=RED,
        fill_opacity=0.4,
        stroke_width=3,
    ).shift(LEFT * 1.5 + DOWN * 3)

    left_right_label = Tex(r"\textbf{Reject}", font_size=24, color=WHITE)
    left_right_label.move_to(left_right_node.get_center())

    # Create arrows
    # Root to left child
    arrow_root_left = Arrow(
        start=root_node.get_bottom() + LEFT * 0.6,
        end=left_node.get_top() + RIGHT * 0.3,
        color=GREEN,
        buff=0.1,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.2,
    )
    yes_label_1 = Tex("Yes", font_size=20, color=GREEN)
    yes_label_1.next_to(arrow_root_left, LEFT, buff=0.1)

    # Root to right child
    arrow_root_right = Arrow(
        start=root_node.get_bottom() + RIGHT * 0.6,
        end=right_node.get_top() + LEFT * 0.3,
        color=RED,
        buff=0.1,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.2,
    )
    no_label_1 = Tex("No", font_size=20, color=RED)
    no_label_1.next_to(arrow_root_right, RIGHT, buff=0.1)

    # Left node to left-left leaf
    arrow_left_left = Arrow(
        start=left_node.get_bottom() + LEFT * 0.6,
        end=left_left_node.get_top() + RIGHT * 0.3,
        color=GREEN,
        buff=0.1,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.2,
    )
    yes_label_2 = Tex("Yes", font_size=20, color=GREEN)
    yes_label_2.next_to(arrow_left_left, LEFT, buff=0.05)

    # Left node to left-right leaf
    arrow_left_right = Arrow(
        start=left_node.get_bottom() + RIGHT * 0.6,
        end=left_right_node.get_top() + LEFT * 0.3,
        color=RED,
        buff=0.1,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.2,
    )
    no_label_2 = Tex("No", font_size=20, color=RED)
    no_label_2.next_to(arrow_left_right, RIGHT, buff=0.05)

    # Animate the tree construction
    
    # Start with root node
    scene.play(DrawBorderThenFill(root_node), Write(root_label), run_time=0.5)

    # Show branches from root
    scene.play(
        Create(arrow_root_left),
        Write(yes_label_1),
        Create(arrow_root_right),
        Write(no_label_1),
        run_time=0.5,
    )

    # Show left and right children
    scene.play(
        DrawBorderThenFill(left_node),
        Write(left_label),
        DrawBorderThenFill(right_node),
        Write(right_label),
        run_time=0.5,
    )

    # Show branches from left node
    scene.play(
        Create(arrow_left_left),
        Write(yes_label_2),
        Create(arrow_left_right),
        Write(no_label_2),
        run_time=0.5,
    )

    # Show final leaves
    scene.play(
        DrawBorderThenFill(left_left_node),
        Write(left_left_label),
        DrawBorderThenFill(left_right_node),
        Write(left_right_label),
        run_time=0.5,
    )

    scene.wait(0.5)
    scene.next_slide()

    # Highlight a decision path (example: Age > 30 → Income > 50k → Approve)
    path_label = Tex(r"Example Decision:", font_size=28, color=YELLOW)
    path_label.next_to(right_node, DOWN, buff=1.5)
    scene.play(Write(path_label), run_time=0.3)
    scene.wait(0.2)

    # Highlight the path
    scene.play(
        root_node.animate.set_stroke(color=YELLOW, width=5),
        arrow_root_left.animate.set_color(YELLOW).set_stroke(width=6),
        run_time=0.6,
    )
    scene.wait(0.2)

    scene.play(
        left_node.animate.set_stroke(color=YELLOW, width=5),
        arrow_left_left.animate.set_color(YELLOW).set_stroke(width=6),
        run_time=0.6,
    )
    scene.wait(0.2)

    scene.play(left_left_node.animate.set_stroke(color=YELLOW, width=5), run_time=0.6)
    scene.wait(0.5)

    # Add explanation text
    explanation = Tex(
        r"Approved because Age $>$ 30 and Income $>$ 50k",
        font_size=24,
        color=YELLOW,
    )
    explanation.next_to(path_label, DOWN, buff=0.3)
    scene.play(Write(explanation), run_time=1)

def xai_matters_slide(scene: ThreeDSlide):

    # ---------------------------
    # Why XAI Matters Scene
    # ---------------------------

    title = Tex(r"\section*{Why XAI Matters}", font_size=48, color=BLUE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title))
    scene.wait(0.5)

    # Create two-column structure
    # Left column: Decision Understanding
    left_title = Tex(r"\textbf{Decision Understanding}", font_size=32, color=GREEN)
    left_title.shift(LEFT * 3.5 + UP * 1.5)

    # Icons and text for left column (using Text for icons and explanations)
    understanding_icon = Text("👁", font_size=40).shift(LEFT * 5 + UP * 0.3)
    understanding_text = Tex(r"Understanding", font_size=22, color=WHITE)
    understanding_text.next_to(understanding_icon, RIGHT, buff=0.3)

    debug_icon = Text("🛠", font_size=40).shift(LEFT * 5 + DOWN * 0.8)
    debug_text = Tex(r"Debugging", font_size=22, color=WHITE)
    debug_text.next_to(debug_icon, RIGHT, buff=0.3)

    bias_icon = Text("⚖", font_size=40).shift(LEFT * 5 + DOWN * 1.9)
    bias_text = Tex(r"Bias Detection", font_size=22, color=WHITE)
    bias_text.next_to(bias_icon, RIGHT, buff=0.3)

    left_group = VGroup(
        left_title,
        understanding_icon,
        understanding_text,
        debug_icon,
        debug_text,
        bias_icon,
        bias_text,
    )

    # Right column: Model Selection
    right_title = Tex(r"\textbf{Model Selection}", font_size=32, color=ORANGE)
    right_title.shift(RIGHT * 3.5 + UP * 1.5)

    # Model A: High accuracy, no explanation (black box)
    # Dark filled rectangle
    model_a_box = Rectangle(
        width=2.5, height=1.4, color=GRAY, fill_color=DARK_GRAY, fill_opacity=0.95, stroke_width=3
    ).shift(RIGHT * 3.5 + UP * 0.3)

    # Label next to the box
    model_a_title = Tex(r"\textbf{Model A}", font_size=24, color=WHITE)
    model_a_title.next_to(model_a_box, LEFT, buff=0.2)

    # Question marks inside the dark box
    model_a_questions = VGroup(
        Text("?", font_size=40, color=GRAY_B),
        Text("?", font_size=40, color=GRAY_B),
        Text("?", font_size=40, color=GRAY_B),
    ).arrange(RIGHT, buff=0.3).move_to(model_a_box.get_center())

    # Caption below
    model_a_caption = Tex(r"High accuracy", font_size=20, color=GREEN)
    model_a_caption.next_to(model_a_box, DOWN, buff=0.2)

    # Model B: Slightly lower accuracy, explainable
    # Light/semi-transparent rectangle
    model_b_box = Rectangle(
        width=2.5, height=1.4, color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=3
    ).shift(RIGHT * 3.5 + DOWN * 2)

    # Label above the box
    model_b_title = Tex(r"\textbf{Model B}", font_size=24, color=WHITE)
    model_b_title.next_to(model_b_box, LEFT, buff=0.2)

    # Visible elements inside: feature names, rules, decision path
    model_b_contents = VGroup(
        Tex(r"\textbf{Features:}", font_size=14, color=WHITE),
        Tex(r"Age, Income, Credit", font_size=12, color=BLUE_B),
        Tex(r"\textbf{Rules:}", font_size=14, color=WHITE),
        Tex(r"If Age $>$ 30 $\land$ Income $>$ 50k", font_size=10, color=BLUE_B),
        Tex(r"\textbf{Decision Path}", font_size=14, color=WHITE),
    ).arrange(DOWN, buff=0.1).move_to(model_b_box.get_center())

    # Caption below
    model_b_caption = Tex(r"Slightly lower accuracy", font_size=20, color=YELLOW)
    model_b_caption.next_to(model_b_box, DOWN, buff=0.2)

    # Arrow pointing to Model B
    chosen_arrow = Arrow(
        start=model_b_box.get_right() + RIGHT * 0.5,
        end=model_b_box.get_right(),
        color=YELLOW,
        buff=0.1,
        stroke_width=6,
    )

    chosen_label = Tex(r"Chosen\\Model", font_size=20, color=YELLOW)
    chosen_label.next_to(chosen_arrow, RIGHT, buff=0.2)

    right_group = VGroup(
        right_title, 
        model_a_box, model_a_title, model_a_questions, model_a_caption,
        model_b_box, model_b_title, model_b_contents, model_b_caption
    )

    # Animate left column
    scene.play(Write(left_title), run_time=0.8)
    scene.wait(0.3)

    scene.play(FadeIn(understanding_icon), Write(understanding_text), run_time=0.8)
    scene.wait(0.2)

    scene.play(FadeIn(debug_icon), Write(debug_text), run_time=0.8)
    scene.wait(0.2)

    scene.play(FadeIn(bias_icon), Write(bias_text), run_time=0.8)
    scene.wait(0.5)

    # Animate right column
    scene.play(Write(right_title), run_time=0.8)
    scene.wait(0.3)

    # Animate Model A (black box)
    scene.play(
        DrawBorderThenFill(model_a_box),
        Write(model_a_title),
        run_time=1.2
    )
    scene.wait(0.3)
    
    scene.play(
        *[FadeIn(q) for q in model_a_questions],
        run_time=0.8
    )
    scene.wait(0.2)
    
    scene.play(Write(model_a_caption), run_time=0.6)
    scene.wait(0.3)

    # Animate Model B (explainable)
    scene.play(
        DrawBorderThenFill(model_b_box),
        Write(model_b_title),
        run_time=1.2
    )
    scene.wait(0.3)
    
    scene.play(
        *[Write(content) for content in model_b_contents],
        lag_ratio=0.2,
        run_time=1.5
    )
    scene.wait(0.2)
    
    scene.play(Write(model_b_caption), run_time=0.6)
    scene.wait(0.5)

    # Show the choice
    scene.play(Create(chosen_arrow), Write(chosen_label), run_time=1)
    scene.wait(0.3)

    # Highlight Model B with a pulse effect
    scene.play(model_b_box.animate.set_stroke(color=YELLOW, width=5), run_time=0.8)
    scene.wait(0.3)

    scene.play(model_b_box.animate.set_stroke(color=GREEN, width=3), run_time=0.8)


def explain_predictive_slide(scene: ThreeDSlide):

    title = Tex(
        r"\section*{Explainability vs Predictive Power}", font_size=48, color=BLUE
    )
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title))
    scene.wait(0.5)

    # Create axes
    axes = Axes(
        x_range=[0, 10, 2],
        y_range=[0, 10, 2],
        x_length=8,
        y_length=6,
        axis_config={"color": WHITE, "include_numbers": False},
        tips=True,
    ).shift(DOWN * 0.3)

    # Axis labels
    x_label = Tex(r"Explainability", font_size=28, color=GREEN)
    x_label.next_to(axes.x_axis, DOWN, buff=0.3)

    y_label = Tex(r"Predictive Power / Accuracy", font_size=28, color=RED)
    y_label.rotate(90 * DEGREES).next_to(axes.y_axis, LEFT, buff=0.3)

    # Draw axes
    scene.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
    scene.wait(0.5)

    # Define model positions (x: explainability, y: predictive power)
    # Scale: 0-10 where higher is better
    models_data = [
        ("Linear Regression", 8.5, 1, GREEN),
        ("Logistic Regression", 7.5, 1.5, GREEN),
        ("Decision Tree", 6.5, 2.5, GREEN),
        ("KNN", 5.5, 3.5, GREEN),
        ("Random Forest", 2.5, 6, ORANGE),
        ("Boosting / Ensemble", 3.0, 6.5, ORANGE),
        ("SVM", 2, 7, RED),
        ("Deep Learning", 1, 8, RED),
    ]

    # Create dots and labels for each model
    model_dots = VGroup()
    model_labels = VGroup()

    for name, x, y, color in models_data:
        point = axes.c2p(x, y)
        dot = Dot(point=point, radius=0.12, color=color, fill_opacity=0.9)
        label = Tex(name, font_size=16, color=color)
        label.next_to(dot, RIGHT, buff=0.15)
        model_dots.add(dot)
        model_labels.add(label)

    # Animate models appearing one by one
    scene.play(
        *[GrowFromCenter(dot) for dot in model_dots],
        *[Write(label) for label in model_labels],
        run_time=2
    )
