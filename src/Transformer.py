from manim import *
import numpy as np
import random
from manim_slides.slide import ThreeDSlide

# Define some consistent colors we might use across slides
EMBEDDING_COLOR = BLUE
FINAL_EMBEDDING_COLOR = GREEN
FLASH_COLOR = YELLOW
ATTENTION_COLOR = PURPLE
MLP_COLOR = MAROON

random.seed(42)
np.random.seed(42)

class TransformerSlides:
    """
    A class to hold the animation logic for different slides
    in a presentation about Transformers.
    """
    def __init__(self, scene: ThreeDSlide):
        self.scene = scene

    def play_slide_one(self, title, n_dims=8, num_flashes=20, anim_run_time=3):
        """
        Plays a visual-only animation of self-attention.
        1. Shows words and their initial embeddings.
        2. Animates an abstract "talking" process.
        3. Shows the embeddings transforming into their final, context-aware state.
        """
        # 1. Set up the sentence and position it at the top
        self.words_list = ["Parsa", "and", "Ali", "have", "data", "mining"]
        self.sentence = VGroup(*[Text(word, font_size=48) for word in self.words_list])
        self.placeholder = Text("presentation", font_size=48, fill_opacity=0)
        self.sentence.add(self.placeholder)
        self.sentence.arrange(RIGHT, buff=0.25)

        self.underline = Underline(self.placeholder, color=YELLOW, stroke_width=5)

        self.sentence_and_underline = VGroup(self.sentence, self.underline)

        self.scene.play(Create(self.underline), Write(self.sentence))

        # last_word = Text("presentation.")
        # words = [Text(w, font_size=32) for w in words_list]
        # words.append(underline)
        # sentence = VGroup(*[Text(w, font_size=32) for w in words_list])
        # sentence.arrange(RIGHT)
        # sentence = Text("Parsa and Ali have data mining presentation.", font_size=32)
        
        # self.scene.play(Write(sentence))
        self.scene.next_slide()

        self.scene.play(self.sentence_and_underline.animate.next_to(title, DOWN))
        
        # 2. Create and animate the initial embeddings appearing below the words
        # words = sentence.get_parts_by_text(" ") # This gets the individual words
        self.initial_embeddings = VGroup()
        for word in self.sentence:
            embedding = self.create_embedding_vector(n_dims=n_dims, color=EMBEDDING_COLOR)
            embedding.next_to(word, DOWN, buff=0.5)
            self.initial_embeddings.add(embedding)

        # Automatically scale to fit the screen
        if self.initial_embeddings.get_width() > self.scene.camera.frame_width - 1:
            self.initial_embeddings.scale_to_fit_width(self.scene.camera.frame_width - 1.5)
        
        self.scene.play(LaggedStart(*[FadeIn(emb, shift=DOWN) for emb in self.initial_embeddings], lag_ratio=0.1))
        self.scene.next_slide()

        # 3. The "Talking" Animation: Sliding Numbers + Flashing Curves
        # First, create the target state for the embeddings
        self.final_embeddings = self.initial_embeddings.copy()
        self.number_change_anims = []
        for i, emb in enumerate(self.final_embeddings):
            new_numbers = VGroup(*[
                DecimalNumber(np.random.uniform(-0.99, 0.99), num_decimal_places=2, font_size=24)
                for _ in range(n_dims)
            ]).arrange(DOWN, buff=0.15).move_to(emb[1])
            
            # Create the animation to slide each number to its new value
            for j in range(n_dims):
                anim = ChangeDecimalToValue(self.initial_embeddings[i][1][j], new_numbers[j].get_value())
                self.number_change_anims.append(anim)

        # Second, create the flashing curve animations
        self.flash_anims = []
        for _ in range(num_flashes):
            # Pick two random embeddings to connect
            idx1, idx2 = random.sample(range(len(self.initial_embeddings)), 2)
            emb1 = self.initial_embeddings[idx1]
            emb2 = self.initial_embeddings[idx2]
            
            # Create a curve below them
            arc = ArcBetweenPoints(
                emb1.get_bottom(), emb2.get_bottom(), 
                angle=-PI / 2, 
                color=FLASH_COLOR, 
                stroke_width=2
            )
            self.flash_anims.append(Succession(Create(arc, run_time=0.1), FadeOut(arc, run_time=0.2)))

        attention_formula = MathTex(r"\text{Attn}(X) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V")
        attention_details = MathTex(r"Q = X", "W_Q", ",\quad K = X", "W_K", ",\quad V = X", "W_V")
        attention_details[1].set_color(BLUE)
        attention_details[3].set_color(BLUE)
        attention_details[5].set_color(BLUE)
        attention_formulas = VGroup(attention_formula, attention_details).scale(0.7)
        attention_formulas.arrange(DOWN, buff=0.5).to_edge(DOWN)

        # Play number sliding and curve flashing at the same time
        self.scene.play(
            Write(attention_formulas),
            *self.number_change_anims,
            LaggedStart(*self.flash_anims, lag_ratio=0.1),
            run_time=anim_run_time
        )
        self.scene.next_slide()
        self.scene.play(Unwrite(self.sentence_and_underline), Unwrite(attention_formulas), FadeOut(self.final_embeddings, self.initial_embeddings))
    
    def play_slide_two(self):
        """
        Plays the animation for the third slide, showing the
        architecture of a single Transformer decoder block.
        """

        # 2. Define the components of our diagram
        self.input_vec = self.final_embeddings[0].copy().scale(0.8).to_edge(LEFT, buff=1)
        
        # Attention Block
        self.attention_box = RoundedRectangle(height=2, width=3, corner_radius=0.2, color=ATTENTION_COLOR)
        self.attention_label = Text("Attention", font_size=24).move_to(self.attention_box)
        self.attention_block = VGroup(self.attention_box, self.attention_label)

        # MLP Block (created with a helper function)
        self.mlp_block = self.create_mlp_diagram(n_inputs=4, n_outputs=4, color=MLP_COLOR)
        
        # Output
        self.output_label = Text("Output\nVector", font_size=24).to_edge(RIGHT, buff=1)

        # Arrange all components from left to right
        VGroup(self.input_vec, self.attention_block, self.mlp_block, self.output_label).arrange(RIGHT, buff=1)
        
        # 3. Animate the creation of the diagram
        self.arrow1 = Arrow(self.input_vec.get_right(), self.attention_block.get_left(), buff=0.1)
        self.arrow2 = Arrow(self.attention_block.get_right(), self.mlp_block.get_left(), buff=0.1)
        self.arrow3 = Arrow(self.mlp_block.get_right(), self.output_label.get_left(), buff=0.1)
        
        self.scene.play(FadeIn(self.input_vec))
        self.scene.play(Create(self.arrow1), FadeIn(self.attention_block))
        # self.scene.next_slide()
        self.scene.play(Create(self.arrow2), FadeIn(self.mlp_block))
        # self.scene.next_slide()

        # 4. Animate the data flow within the MLP
        self.mlp_lines = self.mlp_block[1] # Get the lines group
        self.scene.play(
            LaggedStart(*[
                ShowPassingFlash(line.copy().set_stroke(FLASH_COLOR, 3))
                for line in self.mlp_lines
            ], lag_ratio=0.05, run_time=2.5)
        )
        # self.scene.next_slide()

        # 5. Show the final output
        self.scene.play(Create(self.arrow3), Write(self.output_label))
        self.scene.next_slide()

        # self.scene.play(Uncreate(arrow1), Uncreate(arrow2), Uncreate(arrow3), Uncreate(input_vec), Uncreate(attention_block), Uncreate(mlp_block), Unwrite(output_label))

    def play_slide_three(self):
        """
        Continues the animation:
        1. Updates Input/Output text.
        2. Adds 5 more Transformer layers (Attention + MLP).
        3. Zooms out the camera to fit the deep network.
        4. Adds the final "Presentation" output.
        """
        
        # --- 1. Update Input and Output Text ---
        
        # Access the elements created in the previous slide
        # Assuming these are stored in self or you can pass them as arguments.
        # For this snippet, I will assume variables from the previous scope are available 
        # or re-retrieve them if they are class attributes.
        
        # Unwrite the old output label
        self.scene.play(Unwrite(self.output_label))

        # Change Input Embedding text
        new_input_text = Text("Parsa and Ali have data mining", font_size=20).next_to(self.arrow1, LEFT)
        self.scene.play(
            ReplacementTransform(self.input_vec, new_input_text)
        )
        
        # --- 2. Generate 5 More Layers ---
        
        new_layers = VGroup()
        # Start from the last component of the previous graph (the first MLP)
        current_align_target = self.mlp_block 
        
        for i in range(5):
            # Create arrows and blocks
            # Arrow from previous MLP to new Attention
            arrow_to_attn = Arrow(start=LEFT, end=RIGHT, buff=0.1)
            
            # Attention Block
            att_box = RoundedRectangle(height=2, width=3, corner_radius=0.2, color=ATTENTION_COLOR)
            att_lbl = Text("Attention", font_size=24).move_to(att_box)
            att_block = VGroup(att_box, att_lbl)
            
            # Arrow from Attention to MLP
            arrow_to_mlp = Arrow(start=LEFT, end=RIGHT, buff=0.1)
            
            # MLP Block
            mlp = self.create_mlp_diagram(n_inputs=4, n_outputs=4, color=MLP_COLOR)
            
            # Group this layer's components
            layer_group = VGroup(arrow_to_attn, att_block, arrow_to_mlp, mlp)
            
            # Arrange them relative to the previous block
            layer_group.arrange(RIGHT, buff=1)
            layer_group.next_to(current_align_target, RIGHT, buff=0.1)
            
            # Add to the main group for the camera zoom later
            new_layers.add(layer_group)
            
            # Update target for next iteration
            current_align_target = mlp

        # --- 3. Camera Movement & Revealing Layers ---
        
        # Calculate the total group to determine camera width
        # We include the original graph components + the new layers
        # (Assuming self.original_graph_group is the VGroup from slide 2)
        total_network = VGroup(new_input_text, self.arrow1, self.arrow2, self.arrow3, self.attention_block, self.mlp_block, new_layers)

        target_width = total_network.width * 1.1  # Add 10% padding
        new_zoom = config.frame_width / target_width
        shift_vector = -total_network.get_center()

        # Animate: Reveal new layers AND Zoom out simultaneously
        self.scene.move_camera(
            zoom=new_zoom,
            added_anims=[
                FadeIn(new_layers),
                total_network.animate.shift(shift_vector) # Centers the objects
            ],
            run_time=3
        )
        
        
        # --- 4. Final Output: "Presentation" ---
        
        # Create final arrow and text
        final_arrow = Arrow(start=LEFT, end=RIGHT, buff=0.1)
        final_text = Text("Presentation", font_size=36, color=YELLOW)
        
        final_group = VGroup(final_arrow, final_text).arrange(RIGHT, buff=0.1)
        final_group.next_to(current_align_target, RIGHT, buff=0.1)
        
        self.scene.play(
            Create(final_arrow),
            Write(final_text)
        )
        
        self.scene.next_slide()
        objects_to_remove = VGroup(
            self.input_vec,        # The text "Parsa and Ali..."
            self.attention_block,
            self.mlp_block,
            self.arrow1, self.arrow2, self.arrow3,        # Ensure these variables are accessible!
            new_input_text,
            new_layers,            # The 5 new modules
            final_group            # The "Presentation" output
        )

        # self.scene.play(
        #     *[Unwrite(m) if isinstance(m, (Text, Tex)) else FadeOut(m) for m in objects_to_remove],
        #     self.scene.camera.frame.animate.set_width(config.frame_width).move_to(ORIGIN) # Reset to default view
        # )
        self.scene.move_camera(
            zoom=1, # Resets zoom to default (100%)
            added_anims=[
                # Your cleanup animations go here
                *[Unwrite(m) if isinstance(m, (Text, Tex)) else FadeOut(m) for m in objects_to_remove]
            ]
        )



    def create_mlp_diagram(self, n_inputs, n_outputs, color):
        """Helper function to create a visual MLP block."""
        input_layer = VGroup(*[Dot(color=color) for _ in range(n_inputs)]).arrange(DOWN, buff=0.5)
        output_layer = VGroup(*[Dot(color=color) for _ in range(n_outputs)]).arrange(DOWN, buff=0.5)
        layers = VGroup(input_layer, output_layer).arrange(RIGHT, buff=1)

        lines = VGroup()
        for i_dot in input_layer:
            for o_dot in output_layer:
                lines.add(Line(i_dot, o_dot, stroke_width=1, color=GRAY))
        
        box = SurroundingRectangle(layers, buff=0.3, color=color, stroke_width=2, corner_radius=0.2)
        label = Text("Feed-Forward\nNetwork (MLP)", font_size=24).next_to(box, UP, buff=0.2)

        return VGroup(box, lines, layers, label)


    def create_embedding_vector(self, n_dims, color):
        """Helper function to create a single embedding vector visual."""
        # Create a column of random decimal numbers
        numbers = VGroup(*[
            DecimalNumber(
                np.random.uniform(-0.99, 0.99),
                num_decimal_places=2,
                font_size=24,
            ) for _ in range(n_dims)
        ])
        numbers.arrange(DOWN, buff=0.15)
        
        # Add a surrounding box
        box = SurroundingRectangle(numbers, buff=0.15, color=color, stroke_width=2, corner_radius=0.1)
        
        return VGroup(box, numbers)


# --- Example of how to use the TransformerSlides class ---

class SlideTwoScene(Scene):
    def construct(self):
        # Configure the camera for 1920x1080 resolution
        self.camera.background_color = BLACK
        
        slides = TransformerSlides(self)
        slides.play_slide_two()

