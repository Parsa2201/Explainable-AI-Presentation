from manim import *
from manim_slides.slide import ThreeDSlide

def ali(scene: ThreeDSlide):
    # ---------------------------
    # The Black Box Problem Scene
    # ---------------------------

    title = Text("The Black Box Problem", font_size=48, color=BLUE)
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
                Text("Age", font_size=18).next_to(ORIGIN, RIGHT, buff=0.3),
            ),
            VGroup(
                Circle(radius=0.2, color=GREEN, fill_opacity=0.3),
                Text("Income", font_size=18).next_to(ORIGIN, RIGHT, buff=0.3),
            ),
            VGroup(
                Circle(radius=0.2, color=GREEN, fill_opacity=0.3),
                Text("Credit", font_size=18).next_to(ORIGIN, RIGHT, buff=0.3),
            ),
            VGroup(
                Circle(radius=0.2, color=GREEN, fill_opacity=0.3),
                Text("History", font_size=18).next_to(ORIGIN, RIGHT, buff=0.3),
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

    black_box_label = Text("Black Box\nModel", font_size=24, color=WHITE)
    black_box_label.move_to(black_box.get_center() + UP * 0.8)

    question_mark = Text("?", font_size=80, color=YELLOW)
    question_mark.move_to(black_box.get_center() + DOWN * 0.3)

    # Output on the right
    outputs_label = Text("Output", font_size=32, color=RED).shift(RIGHT * 4.5 + UP * 2)

    output_box = VGroup(
        Rectangle(width=2, height=1.2, color=RED, fill_opacity=0.3),
        Text("Approve", font_size=24, color=GREEN).shift(UP * 0.2),
        Text("Reject", font_size=24, color=RED).shift(DOWN * 0.2),
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
    new_title = Text("From Black Box to Explainable AI", font_size=48, color=BLUE)
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
    
    transparent_box_label = Text("XAI\nModel", font_size=24, color=BLUE)
    transparent_box_label.move_to(transparent_box.get_center() + UP * 1.3)
    
    # Create explanation icons inside transparent box
    explanations = VGroup(
        Text("Age", font_size=16, color=WHITE),
        Text("Income", font_size=16, color=WHITE),
        Text("Decision Path", font_size=16, color=WHITE),
    ).arrange(DOWN, buff=0.3).move_to(transparent_box.get_center())
    
    # Feature importance labels on the right
    feature_importance_label = Text("Feature Importance", font_size=20, color=YELLOW)
    feature_importance_label.next_to(transparent_box, RIGHT, buff=0.3).shift(UP * 1)
    
    rules_label = Text("Decision Rules", font_size=20, color=YELLOW)
    rules_label.next_to(transparent_box, RIGHT, buff=0.3)
    
    highlights_label = Text("Key Factors", font_size=20, color=YELLOW)
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
    
    scene.wait(1)
    scene.next_slide()
    
    # Fade out everything for next slide
    scene.play(*[FadeOut(mob) for mob in scene.mobjects], run_time=1)
