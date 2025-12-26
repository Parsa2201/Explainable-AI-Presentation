from manim import *
import numpy as np
import random

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
    def __init__(self, scene: Scene, title: Text):
        self.scene = scene
        self.title = title

    def play_slide_one(self, n_dims=8, num_flashes=20, anim_run_time=3):
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

        self.scene.play(self.sentence_and_underline.animate.next_to(self.title, DOWN))
        
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

        # Play number sliding and curve flashing at the same time
        self.scene.play(
            *self.number_change_anims,
            LaggedStart(*self.flash_anims, lag_ratio=0.1),
            run_time=anim_run_time
        )
        self.scene.next_slide()

        return 
    
    def play_slide_two(self):
        """
        Plays the animation for the third slide, showing the
        architecture of a single Transformer decoder block.
        """
        # 1. Clean up the previous slide's objects
        self.scene.play(Unwrite(self.sentence_and_underline), FadeOut(self.final_embeddings, self.initial_embeddings))
        self.scene.next_slide()

        # 2. Define the components of our diagram
        input_vec = self.final_embeddings[0].copy().scale(0.8).to_edge(LEFT, buff=1)
        
        # Attention Block
        attention_box = RoundedRectangle(height=2, width=3, corner_radius=0.2, color=ATTENTION_COLOR)
        attention_label = Text("Attention", font_size=24).move_to(attention_box)
        attention_block = VGroup(attention_box, attention_label)

        # MLP Block (created with a helper function)
        mlp_block = self.create_mlp_diagram(n_inputs=4, n_outputs=4, color=MLP_COLOR)
        
        # Output
        output_label = Text("Output\nVector", font_size=24).to_edge(RIGHT, buff=1)

        # Arrange all components from left to right
        VGroup(input_vec, attention_block, mlp_block, output_label).arrange(RIGHT, buff=1)
        
        # 3. Animate the creation of the diagram
        arrow1 = Arrow(input_vec.get_right(), attention_block.get_left(), buff=0.1)
        arrow2 = Arrow(attention_block.get_right(), mlp_block.get_left(), buff=0.1)
        arrow3 = Arrow(mlp_block.get_right(), output_label.get_left(), buff=0.1)
        
        self.scene.play(FadeIn(input_vec))
        self.scene.play(Create(arrow1), FadeIn(attention_block))
        self.scene.next_slide()
        self.scene.play(Create(arrow2), FadeIn(mlp_block))
        self.scene.next_slide()

        # 4. Animate the data flow within the MLP
        mlp_lines = mlp_block[1] # Get the lines group
        self.scene.play(
            LaggedStart(*[
                ShowPassingFlash(line.copy().set_stroke(FLASH_COLOR, 3))
                for line in mlp_lines
            ], lag_ratio=0.05, run_time=2.5)
        )
        self.scene.next_slide()

        # 5. Show the final output
        self.scene.play(Create(arrow3), Write(output_label))
        self.scene.next_slide()


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

