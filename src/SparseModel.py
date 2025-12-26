from manim import *
from manim_slides.slide import ThreeDSlide
import random

random.seed(42)

random.seed(42)

# Consistent Colors
NEURON_COLOR = WHITE
ACTIVE_COLOR = YELLOW
CONNECTION_COLOR = GRAY
TEXT_COLOR = WHITE
POS_COLOR = BLUE
NEG_COLOR = RED
PATH_COLOR = YELLOW

def get_opacity(p_sparsity):
    """
    Returns a continuous opacity value.
    If p_sparsity is high, opacity tends towards 0 (dim/transparent).
    If p_sparsity is low, opacity tends towards 1 (bright/opaque).
    """
    # Determine if this element is "active" based on sparsity probability
    # High p -> Low chance of being active
    if random.random() > p_sparsity:
        # Active: High opacity (e.g., 0.7 to 1.0)
        return random.uniform(0.7, 1.0)
    else:
        # Sparse/Inactive: Low opacity (e.g., 0.05 to 0.3)
        # This gives the "middle" values you requested, not just 0 or 1
        return random.uniform(0.05, 0.3)

def create_mlp(layer_dims, p_sparsity):
    """
    Generates an MLP VGroup with dynamic spacing and sparsity-based opacity.
    """
    layers = VGroup()
    
    # Dynamic spacing: Calculate buffer to ensure it fits on screen (height ~8.0)
    # We use 6.0 as max usable height to leave room for footers/headers
    max_neurons = max(layer_dims)
    vertical_buff = min(0.8, 6.0 / max_neurons)
    
    # 1. Create Layers (Neurons)
    for dim in layer_dims:
        layer = VGroup(*[
            Dot(
                color=NEURON_COLOR, 
                fill_opacity=get_opacity(p_sparsity)
            ) for _ in range(dim)
        ]).arrange(DOWN, buff=vertical_buff)
        layers.add(layer)
    
    layers.arrange(RIGHT, buff=4)
    
    # 2. Create Connections (Weights)
    lines = VGroup()
    for i in range(len(layers) - 1):
        current_layer = layers[i]
        next_layer = layers[i+1]
        
        for u in current_layer:
            for v in next_layer:
                lines.add(
                    Line(
                        u.get_center(), 
                        v.get_center(), 
                        stroke_width=2, 
                        stroke_opacity=get_opacity(p_sparsity), 
                        color=CONNECTION_COLOR
                    )
                )
                
    return layers, lines

class SparseModelSlides:
    def __init__(self, scene: ThreeDSlide):
        self.scene = scene
        self.mobjects = {}

    def play_slide_one(self):
        """
        Slide 1: Polysemantic vs. Sparse/Monosemantic
        """

        # --- Phase 1: Dense Model (Polysemantic) ---
        # User requested dimensions [3, 5, 3] for the generic MLP function
        dense_dims = [3, 5, 3]
        # Low sparsity (p=0.1) means most connections/neurons are visible
        dense_layers, dense_lines = create_mlp(dense_dims, p_sparsity=0.1)
        
        # Group them for easy animation
        dense_model = VGroup(dense_lines, dense_layers)
        
        # Footer text
        footer_dense = Text("Dense Model: Superposition", font_size=24, color=RED).to_edge(DOWN)

        self.scene.play(
            FadeIn(dense_model),
            Write(footer_dense)
        )
        self.scene.next_slide()

        # --- Phase 2: Demonstrate Polysemanticity ---
        # Pick the middle neuron in the hidden layer (layer index 1)
        # In a layer of 5, index 2 is the exact middle
        hidden_layer = dense_layers[1]
        target_neuron = hidden_layer[2]

        my_template = TexTemplate()
        my_template.add_to_preamble(r"\usepackage{fontawesome5}")

        # Concepts
        concepts = [
            (r"\faCat Cat", BLUE),
            (r"\faCar Car", RED),
            (r"\faBook Book", GREEN)
        ]

        # Create a stack of labels: "Below each other, on top of that neuron"
        # We create them all, arrange vertically, and place the group above the neuron
        concept_texts = VGroup()
        for text, color in concepts:
            concept_texts.add(Tex(text, tex_template=my_template, font_size=32, color=color))
        
        concept_texts.arrange(DOWN, buff=0.15)
        concept_texts.next_to(target_neuron, UP, buff=0.5)

        # Animate showing the concept stack
        self.scene.play(FadeIn(concept_texts))
        
        # Flash the neuron for each concept to show it activates for all
        for i, (text_str, color) in enumerate(concepts):
            # Highlight the specific text in the stack
            active_text = concept_texts[i]
            
            self.scene.play(
                Flash(target_neuron, color=color, flash_radius=0.3, line_length=0.2),
                target_neuron.animate.set_color(color),
                active_text.animate.scale(1.2), # Slight pop effect
                run_time=0.5
            )
            # self.scene.wait(0.2)
            # Reset
            # self.scene.play(
            #     active_text.animate.scale(1/1.2),
            #     run_time=0.1
            # )
            # self.scene.wait(0.2)
        self.scene.wait(2)
        self.scene.next_slide()
        target_neuron.set_color(NEURON_COLOR)

        # --- Phase 3: Transform to Sparse Model ---
        
        # Create Sparse MLP
        # Expand hidden layer to 10 neurons, High sparsity (p=0.7)
        sparse_dims = [3, 10, 3] 
        sparse_layers, sparse_lines = create_mlp(sparse_dims, p_sparsity=0.7)
        
        # Align the sparse model to the dense model's position to ensure smooth transform
        sparse_layers.move_to(dense_layers)
        
        sparse_model = VGroup(sparse_lines, sparse_layers).scale_to_fit_height(self.scene.camera.frame_height - 2.5)
        
        footer_sparse = Text("Sparse Model: Disentanglement", font_size=24, color=GREEN).to_edge(DOWN)

        self.scene.play(
            FadeOut(concept_texts), # Remove the stack
            Transform(dense_model, sparse_model), # Morph the network
            Transform(footer_dense, footer_sparse)
        )
        
        # Update references after transform
        # dense_model now looks like sparse_model, but we can use sparse_layers for reference
        current_hidden_layer = sparse_layers[1]

        self.scene.next_slide()

        # --- Phase 4: Monosemanticity ---
        # "Concepts shown on top of the neurons" (One per neuron)
        
        # Pick 3 distinct neurons from the larger hidden layer (size 10)
        neuron_cat = current_hidden_layer[1] # Top
        neuron_car = current_hidden_layer[5] # Middle
        neuron_book = current_hidden_layer[8] # Bottom

        mapping = [
            (r"\faCat Cat", BLUE, neuron_cat),
            (r"\faCar Car", RED, neuron_car),
            (r"\faBook Book", GREEN, neuron_book)
        ]
        labels = []
        for text, color, neuron in mapping:
            # Create label directly above the specific neuron
            label = Tex(text, tex_template=my_template, font_size=28, color=color)
            label.next_to(neuron, UP, buff=0.3)
            labels.append(label)
            
            self.scene.play(
                FadeIn(label),
                Flash(neuron, color=color, flash_radius=0.3, line_length=0.2),
                neuron.animate.set_color(color),
                run_time=0.5
            )
            self.scene.wait(0.2)

        self.scene.next_slide()

        self.scene.play(Unwrite(dense_model), Unwrite(sparse_model), Unwrite(footer_dense), Unwrite(footer_sparse), *[Unwrite(label) for label in labels])

    def play_slide_two(self):
        """
        Slide 2: Weight Matrix Sparsification (L0 Norm)
        """
        # 1. Create a Matrix of random weights
        rows, cols = 6, 6
        values = np.random.normal(0, 1, (rows, cols)).round(1)
        
        # Create DecimalMatrix
        matrix = DecimalMatrix(
            values, 
            element_to_mobject_config={"font_size": 24},
            h_buff=0.8, v_buff=0.5
        )
        
        footer = Text("Weight Matrix: L0 Norm Regularization", font_size=24).to_edge(DOWN)
        
        self.scene.play(Write(matrix), Write(footer))
        self.scene.next_slide()

        # 2. Prune: Set small values to 0
        threshold = 0.8
        new_values = values.copy()
        
        # Identify indices to zero out
        mask = np.abs(values) < threshold
        new_values[mask] = 0.0
        
        # Create target matrix
        target_matrix = DecimalMatrix(
            new_values,
            element_to_mobject_config={"font_size": 24},
            h_buff=0.8, v_buff=0.5
        )
        
        # Dim the zeros in the target matrix to emphasize sparsity
        for i in range(rows):
            for j in range(cols):
                if mask[i, j]:
                    # Find the mobject in the target matrix and dim it
                    mob = target_matrix.get_entries()[i * cols + j]
                    mob.set_opacity(0.3)

        self.scene.play(
            Transform(matrix, target_matrix),
            run_time=2
        )
        self.scene.next_slide()
        self.scene.play(FadeOut(matrix), FadeOut(footer))

    def play_slide_three(self):
        """
        Slide 3: Colored MLP & Magnitude Pruning
        """
        # 1. Create Colored MLP
        # Dimensions: 3 input, 6 hidden, 3 output
        layers, lines, all_elements = self.create_colored_mlp([3, 6, 3])
        mlp_group = VGroup(lines, layers)
        
        footer = Text("Pruning: Removing Weak Connections", font_size=24).to_edge(DOWN)
        
        self.scene.play(FadeIn(mlp_group), Write(footer))
        # self.scene.next_slide()
        
        # 2. Prune based on absolute value
        # We want to keep the "strongest" connections
        threshold = 0.7 # Prune anything with abs(value) < 0.4
        
        anims = []
        # other_mobs = []
        for mob in all_elements:
            if abs(mob.value) < threshold:
                # Option A: Fade out completely
                # anims.append(FadeOut(mob))
                # Option B: Reduce opacity drastically (ghosting)
                anims.append(mob.animate.set_opacity(0.3))
            # else:
            #     other_mobs.append(mob)
        
        self.scene.play(*anims, run_time=1.5)
        self.scene.next_slide()
        
        # Clean up
        self.scene.play(FadeOut(mlp_group), FadeOut(footer))

    def play_slide_four(self):
        """
        Slide 4: Subnetwork Extraction (The "Ticket")
        """
        # 1. Setup MLP with 3 Hidden Layers (Total 5 layers)
        # Dimensions tailored to support the requested indices:
        # Input: 3 (Need 3)
        # H1: 5 (Need indices 0, 3 -> size >= 4)
        # H2: 4 (Need index 1 -> size >= 2)
        # H3: 6 (Need indices 3, 4 -> size >= 5)
        # Output: 3 (Need index 1 -> size >= 2)
        dims = [3, 5, 4, 6, 3]
        layers, lines = self.create_mlp(dims, p_sparsity=0.0)
        mlp_group = VGroup(lines, layers)
        
        footer = Text("Subnetwork Extraction: Finding the Circuit", font_size=24).to_edge(DOWN)
        
        self.scene.play(FadeIn(mlp_group), Write(footer))
        self.scene.next_slide()

        # 2. Define the Custom Path (Indices)
        # Format: {layer_index: [list_of_active_node_indices]}
        active_indices = {
            0: [0, 1, 2],       # "from 3 of the input neurons"
            1: [0, 3],          # "1st and 4th neurons of 1st hidden layer"
            2: [1],             # "2nd neuron of 2nd hidden layer"
            3: [3, 4],          # "4th and 5th neurons of 3rd hidden layer"
            4: [1]              # "2nd neuron of the output layer"
        }

        # 3. Separate Active vs Inactive Elements
        active_group = VGroup()
        inactive_group = VGroup()
        
        # Check Neurons
        for layer_idx, layer in enumerate(layers):
            actives_in_this_layer = active_indices.get(layer_idx, [])
            for node_idx, dot in enumerate(layer):
                if node_idx in actives_in_this_layer:
                    active_group.add(dot)
                    dot.is_active = True # Mark for line checking
                else:
                    inactive_group.add(dot)
                    dot.is_active = False

        # Check Lines (Edges)
        # A line is active ONLY if it connects an active node to an active node
        for line in lines:
            if getattr(line.start_node, 'is_active', False) and \
               getattr(line.end_node, 'is_active', False):
                active_group.add(line)
            else:
                inactive_group.add(line)

        # 4. Animation: Fade inactive elements to "almost gone"
        self.scene.play(
            inactive_group.animate.set_opacity(0.1),
            run_time=1.5
        )
        self.scene.next_slide()

        # 5. Animation: Completely fade inactive, Flash the path
        self.scene.play(FadeOut(inactive_group))
        
        # Sequential Flash
        # We flash layer by layer to show the "flow"
        path_anims = []
        
        # Iterate through layers to create a sequential flow animation
        for i in range(len(dims) - 1):
            # Find lines connecting active nodes in layer i to layer i+1
            layer_lines = VGroup()
            for line in lines:
                # Check if this line is part of the active group and connects current layers
                if line in active_group:
                    if line.start_node.layer_index == i:
                        layer_lines.add(line)
            
            # Flash lines
            if len(layer_lines) > 0:
                self.scene.play(
                    ShowPassingFlash(
                        layer_lines.copy().set_color(PATH_COLOR).set_stroke(width=4),
                        time_width=0.5,
                        run_time=0.8
                    )
                )
                
                # Flash next nodes
                next_nodes = VGroup()
                for dot in layers[i+1]:
                    if dot in active_group:
                        next_nodes.add(dot)
                
                self.scene.play(
                    Flash(next_nodes, color=PATH_COLOR, flash_radius=0.2, line_length=0.1),
                    next_nodes.animate.set_color(PATH_COLOR),
                    run_time=0.3
                )

        self.scene.wait(1)
        self.scene.next_slide()
        self.scene.play(FadeOut(mlp_group), FadeOut(footer))

    def create_mlp(self, layer_dims, p_sparsity=0.0):
        """
        Creates an MLP and attaches metadata to mobjects for easy indexing.
        """
        layers = VGroup()
        max_neurons = max(layer_dims)
        vertical_buff = min(0.8, 6.0 / max_neurons)
        
        # 1. Create Dots with Metadata
        for i, dim in enumerate(layer_dims):
            layer = VGroup()
            for j in range(dim):
                dot = Dot(color=NEURON_COLOR, fill_opacity=get_opacity(p_sparsity))
                # Attach indices
                dot.layer_index = i
                dot.node_index = j
                layer.add(dot)
            layer.arrange(DOWN, buff=vertical_buff)
            layers.add(layer)
        
        layers.arrange(RIGHT, buff=3.0)
        
        # 2. Create Lines with Metadata
        lines = VGroup()
        for i in range(len(layers) - 1):
            current_layer = layers[i]
            next_layer = layers[i+1]
            
            for u in current_layer:
                for v in next_layer:
                    line = Line(
                        u.get_center(), v.get_center(), 
                        stroke_width=2, stroke_opacity=get_opacity(p_sparsity), 
                        color=CONNECTION_COLOR
                    )
                    # Attach start/end node references
                    line.start_node = u
                    line.end_node = v
                    lines.add(line)
                    
        return layers, lines

    def create_colored_mlp(self, layer_dims):
        """
        Creates an MLP where:
        - Neurons/Lines have a .value attribute (random -1 to 1).
        - Color is BLUE if positive, RED if negative.
        """
        layers = VGroup()
        max_neurons = max(layer_dims)
        vertical_buff = min(0.8, 6.0 / max_neurons)
        
        all_elements = [] # To store lines and dots for pruning later

        # 1. Create Layers (Neurons)
        for dim in layer_dims:
            layer_group = VGroup()
            for _ in range(dim):
                val = random.uniform(-1, 1)
                color = POS_COLOR if val > 0 else NEG_COLOR
                dot = Dot(color=color)
                dot.value = val # Attach value to mobject
                layer_group.add(dot)
                all_elements.append(dot)
            
            layer_group.arrange(DOWN, buff=vertical_buff)
            layers.add(layer_group)
        
        layers.arrange(RIGHT, buff=4)
        
        # 2. Create Connections (Weights)
        lines = VGroup()
        for i in range(len(layers) - 1):
            for u in layers[i]:
                for v in layers[i+1]:
                    val = random.uniform(-1, 1)
                    color = POS_COLOR if val > 0 else NEG_COLOR
                    # Thicker lines for larger magnitude
                    width = 1 + 4 * abs(val) 
                    
                    line = Line(u.get_center(), v.get_center(), stroke_width=width, color=color)
                    line.value = val # Attach value to mobject
                    lines.add(line)
                    all_elements.append(line)
                    
        return layers, lines, all_elements
