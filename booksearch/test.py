import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
plt.style.use('default')
sns.set_palette("husl")

# Set up the plotting style for professional-looking figures
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['grid.alpha'] = 0.3

# 1. Neural Network Architecture Visualization
def create_network_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Define layer positions and sizes
    layers = [784, 128, 10]  # Input, Hidden, Output
    layer_names = ['Input Layer\n(784 pixels)', 'Hidden Layer\n(128 neurons)', 'Output Layer\n(10 classes)']
    layer_positions = [1, 3, 5]
    
    # Colors for different layers
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    # Draw neurons
    for i, (layer_size, pos, color, name) in enumerate(zip(layers, layer_positions, colors, layer_names)):
        # For input layer, show more neurons; for others, show representative sample
        if i == 0:
            neurons_to_show = min(20, layer_size)
        else:
            neurons_to_show = min(10, layer_size)
        
        y_positions = np.linspace(-2, 2, neurons_to_show)
        
        for y in y_positions:
            circle = plt.Circle((pos, y), 0.1, color=color, alpha=0.7)
            ax.add_patch(circle)
        
        # Add dots if we're not showing all neurons
        if neurons_to_show < layer_size:
            ax.text(pos, -2.5, f'... ({layer_size} total)', ha='center', fontsize=10)
        
        # Layer labels
        ax.text(pos, -3, name, ha='center', fontsize=12, weight='bold')
    
    # Draw connections between layers
    for i in range(len(layer_positions) - 1):
        start_pos = layer_positions[i]
        end_pos = layer_positions[i + 1]
        
        # Draw sample connections
        for start_y in np.linspace(-1.5, 1.5, 5):
            for end_y in np.linspace(-1, 1, 3):
                ax.plot([start_pos + 0.1, end_pos - 0.1], [start_y, end_y], 
                       'k-', alpha=0.1, linewidth=0.5)
    
    # Add mathematical annotations
    ax.text(2, 3, r'$z^{[1]} = W^{[1]}x + b^{[1]}$', fontsize=14, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    ax.text(2, 2.5, r'$a^{[1]} = ReLU(z^{[1]})$', fontsize=14,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    ax.text(4, 3, r'$z^{[2]} = W^{[2]}a^{[1]} + b^{[2]}$', fontsize=14,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))
    ax.text(4, 2.5, r'$a^{[2]} = softmax(z^{[2]})$', fontsize=14,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))
    
    ax.set_xlim(0, 6)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Neural Network Architecture: From Mathematics to Recognition', 
                fontsize=16, weight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('neural_network_architecture.png', dpi=300, bbox_inches='tight')
    plt.show()

# 2. Activation Functions Visualization
def create_activation_functions():
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    x = np.linspace(-5, 5, 1000)
    
    # ReLU function
    relu = np.maximum(0, x)
    axes[0,0].plot(x, relu, 'b-', linewidth=3, label='ReLU(x)')
    axes[0,0].plot(x, np.where(x > 0, 1, 0), 'r--', linewidth=2, label="ReLU'(x)")
    axes[0,0].set_title('ReLU Activation Function', fontsize=14, weight='bold')
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].legend()
    axes[0,0].set_xlabel('Input (z)')
    axes[0,0].set_ylabel('Output')
    axes[0,0].text(-4, 3, r'$f(z) = max(0, z)$', fontsize=12, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    # Sigmoid function
    sigmoid = 1 / (1 + np.exp(-x))
    sigmoid_derivative = sigmoid * (1 - sigmoid)
    axes[0,1].plot(x, sigmoid, 'g-', linewidth=3, label='Sigmoid(x)')
    axes[0,1].plot(x, sigmoid_derivative, 'r--', linewidth=2, label="Sigmoid'(x)")
    axes[0,1].set_title('Sigmoid Activation Function', fontsize=14, weight='bold')
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].legend()
    axes[0,1].set_xlabel('Input (z)')
    axes[0,1].set_ylabel('Output')
    axes[0,1].text(-4, 0.8, r'$f(z) = \frac{1}{1 + e^{-z}}$', fontsize=12,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
    
    # Softmax visualization (for 3 classes)
    z1, z2, z3 = 2, 1, 0.1
    z_values = np.array([z1, z2, z3])
    softmax_values = np.exp(z_values) / np.sum(np.exp(z_values))
    
    axes[1,0].bar(['Class 1', 'Class 2', 'Class 3'], softmax_values, 
                  color=['#3498db', '#e74c3c', '#2ecc71'], alpha=0.7)
    axes[1,0].set_title('Softmax Output (Probability Distribution)', fontsize=14, weight='bold')
    axes[1,0].set_ylabel('Probability')
    axes[1,0].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(softmax_values):
        axes[1,0].text(i, v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')
    axes[1,0].text(0.5, 0.8, r'$softmax(z_i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}$', 
                   fontsize=12, transform=axes[1,0].transAxes,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
    
    # Loss function visualization
    x_loss = np.linspace(0.001, 0.999, 1000)
    cross_entropy = -np.log(x_loss)
    axes[1,1].plot(x_loss, cross_entropy, 'purple', linewidth=3, label='Cross-Entropy Loss')
    axes[1,1].set_title('Cross-Entropy Loss Function', fontsize=14, weight='bold')
    axes[1,1].set_xlabel('Predicted Probability (for true class)')
    axes[1,1].set_ylabel('Loss')
    axes[1,1].grid(True, alpha=0.3)
    axes[1,1].legend()
    axes[1,1].text(0.6, 4, r'$L = -\log(\hat{y})$', fontsize=12,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="plum"))
    
    plt.tight_layout()
    plt.savefig('activation_functions.png', dpi=300, bbox_inches='tight')
    plt.show()

# 3. Training Progress Visualization
def create_training_progress():
    # Simulate training data based on the blog post results
    epochs = np.arange(0, 500, 10)
    
    # Simulated accuracy progression (starting at 23%, ending at 85%)
    accuracy = 23 + (85 - 23) * (1 - np.exp(-epochs / 150)) + np.random.normal(0, 1, len(epochs))
    accuracy = np.clip(accuracy, 0, 100)
    
    # Simulated loss progression (decreasing exponentially)
    loss = 2.3 * np.exp(-epochs / 100) + 0.1 + np.random.normal(0, 0.05, len(epochs))
    loss = np.clip(loss, 0.1, 3)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Accuracy plot
    ax1.plot(epochs, accuracy, 'b-', linewidth=3, label='Training Accuracy', marker='o', markersize=4)
    ax1.axhline(y=85, color='r', linestyle='--', linewidth=2, label='Final Accuracy (85%)')
    ax1.axhline(y=23, color='orange', linestyle='--', linewidth=2, label='Initial Accuracy (23%)')
    ax1.set_xlabel('Training Iterations', fontsize=12)
    ax1.set_ylabel('Accuracy (%)', fontsize=12)
    ax1.set_title('Model Accuracy Progression\nFrom Mathematical Understanding', fontsize=14, weight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_ylim(0, 100)
    
    # Add annotations for key improvements
    ax1.annotate('Learning rate optimization', xy=(150, 60), xytext=(200, 40),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    ax1.annotate('Weight initialization fix', xy=(50, 35), xytext=(100, 20),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    # Loss plot
    ax2.plot(epochs, loss, 'r-', linewidth=3, label='Training Loss', marker='s', markersize=4)
    ax2.set_xlabel('Training Iterations', fontsize=12)
    ax2.set_ylabel('Cross-Entropy Loss', fontsize=12)
    ax2.set_title('Loss Function Minimization\nThrough Gradient Descent', fontsize=14, weight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('training_progress.png', dpi=300, bbox_inches='tight')
    plt.show()

# 4. Gradient Flow Visualization
def create_gradient_flow():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Gradient magnitude through layers
    layers = ['Input', 'Hidden 1', 'Hidden 2', 'Output']
    
    # Good gradient flow
    good_gradients = [1.0, 0.8, 0.6, 0.4]
    # Poor gradient flow (vanishing)
    poor_gradients = [1.0, 0.1, 0.01, 0.001]
    
    x_pos = np.arange(len(layers))
    
    ax1.bar(x_pos - 0.2, good_gradients, 0.4, label='Healthy Gradients', 
            color='green', alpha=0.7)
    ax1.bar(x_pos + 0.2, poor_gradients, 0.4, label='Vanishing Gradients', 
            color='red', alpha=0.7)
    
    ax1.set_xlabel('Network Layers')
    ax1.set_ylabel('Gradient Magnitude')
    ax1.set_title('Gradient Flow Through Network Layers', fontsize=14, weight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(layers)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_yscale('log')
    
    # Weight update visualization
    iterations = np.arange(0, 100)
    # Simulate weight updates with different learning rates
    lr_high = 0.1
    lr_optimal = 0.01
    lr_low = 0.001
    
    # Simulated convergence curves
    high_lr = 0.5 + 0.3 * np.cos(iterations * 0.5) * np.exp(-iterations * 0.01)
    optimal_lr = 1.0 * np.exp(-iterations * 0.05)
    low_lr = 1.0 * np.exp(-iterations * 0.01)
    
    ax2.plot(iterations, high_lr, 'r-', linewidth=3, label=f'High LR ({lr_high})', alpha=0.8)
    ax2.plot(iterations, optimal_lr, 'g-', linewidth=3, label=f'Optimal LR ({lr_optimal})', alpha=0.8)
    ax2.plot(iterations, low_lr, 'b-', linewidth=3, label=f'Low LR ({lr_low})', alpha=0.8)
    
    ax2.set_xlabel('Training Iterations')
    ax2.set_ylabel('Loss Value')
    ax2.set_title('Learning Rate Impact on Convergence', fontsize=14, weight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('gradient_flow.png', dpi=300, bbox_inches='tight')
    plt.show()

# 5. Mathematical Concepts Visualization
def create_mathematical_concepts():
    fig = plt.figure(figsize=(16, 12))
    
    # Create a 2x3 subplot layout
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Matrix multiplication visualization
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Create sample matrices
    W = np.random.randn(3, 4)
    X = np.random.randn(4, 2)
    
    # Visualize matrices as heatmaps
    im1 = ax1.imshow(W, cmap='RdBu', aspect='auto')
    ax1.set_title('Weight Matrix W\n(3×4)', fontsize=12, weight='bold')
    ax1.set_xlabel('Input Features')
    ax1.set_ylabel('Hidden Neurons')
    plt.colorbar(im1, ax=ax1, shrink=0.6)
    
    # 2. Input matrix
    ax2 = fig.add_subplot(gs[0, 1])
    im2 = ax2.imshow(X, cmap='RdBu', aspect='auto')
    ax2.set_title('Input Matrix X\n(4×2)', fontsize=12, weight='bold')
    ax2.set_xlabel('Batch Samples')
    ax2.set_ylabel('Input Features')
    plt.colorbar(im2, ax=ax2, shrink=0.6)
    
    # 3. Forward propagation flow
    ax3 = fig.add_subplot(gs[1, :])
    
    # Create flow diagram
    steps = ['Input\n(784×m)', 'Linear Transform\nZ¹ = W¹X + b¹', 'ReLU\nA¹ = max(0,Z¹)', 
             'Linear Transform\nZ² = W²A¹ + b²', 'Softmax\nA² = softmax(Z²)', 'Output\n(10×m)']
    
    x_positions = np.linspace(0, 10, len(steps))
    y_position = 0
    
    for i, (step, x_pos) in enumerate(zip(steps, x_positions)):
        # Draw boxes
        rect = plt.Rectangle((x_pos-0.7, y_position-0.3), 1.4, 0.6, 
                           facecolor='lightblue', edgecolor='black', alpha=0.7)
        ax3.add_patch(rect)
        ax3.text(x_pos, y_position, step, ha='center', va='center', fontsize=10, weight='bold')
        
        # Draw arrows
        if i < len(steps) - 1:
            ax3.arrow(x_pos + 0.7, y_position, 
                     x_positions[i+1] - x_pos - 1.4, 0,
                     head_width=0.1, head_length=0.2, fc='red', ec='red')
    
    ax3.set_xlim(-1, 11)
    ax3.set_ylim(-1, 1)
    ax3.set_title('Forward Propagation: Mathematical Flow', fontsize=14, weight='bold')
    ax3.axis('off')
    
    # 4. Backpropagation visualization
    ax4 = fig.add_subplot(gs[2, :])
    
    # Backprop steps
    back_steps = ['Loss\nL = -log(ŷ)', 'Output Gradient\ndL/dZ²', 'Weight Gradient\ndL/dW²', 
                  'Hidden Gradient\ndL/dA¹', 'Hidden Gradient\ndL/dZ¹', 'Weight Gradient\ndL/dW¹']
    
    x_positions_back = np.linspace(10, 0, len(back_steps))
    
    for i, (step, x_pos) in enumerate(zip(back_steps, x_positions_back)):
        # Draw boxes
        rect = plt.Rectangle((x_pos-0.7, y_position-0.3), 1.4, 0.6, 
                           facecolor='lightcoral', edgecolor='black', alpha=0.7)
        ax4.add_patch(rect)
        ax4.text(x_pos, y_position, step, ha='center', va='center', fontsize=10, weight='bold')
        
        # Draw arrows (pointing backward)
        if i < len(back_steps) - 1:
            ax4.arrow(x_pos - 0.7, y_position, 
                     x_positions_back[i+1] - x_pos + 1.4, 0,
                     head_width=0.1, head_length=0.2, fc='blue', ec='blue')
    
    ax4.set_xlim(-1, 11)
    ax4.set_ylim(-1, 1)
    ax4.set_title('Backpropagation: Gradient Flow (Chain Rule)', fontsize=14, weight='bold')
    ax4.axis('off')
    
    plt.savefig('mathematical_concepts.png', dpi=300, bbox_inches='tight')
    plt.show()

# 6. Performance Comparison Visualization
def create_performance_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Comparison of different approaches
    approaches = ['Random\nGuessing', 'Basic\nImplementation', 'Optimized\nHyperparameters', 
                  'Final Model\n(From Scratch)', 'TensorFlow\nBaseline']
    accuracies = [10, 23, 65, 85, 87]
    colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
    
    bars = ax1.bar(approaches, accuracies, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Accuracy (%)', fontsize=12)
    ax1.set_title('Performance Comparison: Understanding vs Tools', fontsize=14, weight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{acc}%', ha='center', va='bottom', fontweight='bold')
    
    # Understanding vs Framework Knowledge
    categories = ['Debugging\nCapability', 'Mathematical\nIntuition', 'Custom\nSolutions', 
                  'Innovation\nPotential', 'Framework\nProficiency']
    
    from_scratch = [9, 10, 9, 10, 6]
    framework_only = [4, 3, 4, 4, 10]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, from_scratch, width, label='From Scratch Learning', 
                    color='lightblue', alpha=0.8)
    bars2 = ax2.bar(x + width/2, framework_only, width, label='Framework Only', 
                    color='lightcoral', alpha=0.8)
    
    ax2.set_ylabel('Skill Level (1-10)', fontsize=12)
    ax2.set_title('Skill Development: Mathematical Foundation vs Framework Focus', 
                  fontsize=14, weight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim(0, 11)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

# Execute all visualizations
if __name__ == "__main__":
    print("Creating Neural Network Architecture Visualization...")
    create_network_architecture()
    
    print("Creating Activation Functions Visualization...")
    create_activation_functions()
    
    print("Creating Training Progress Visualization...")
    create_training_progress()
    
    print("Creating Gradient Flow Visualization...")
    create_gradient_flow()
    
    print("Creating Mathematical Concepts Visualization...")
    create_mathematical_concepts()

    print("Creating Performance Comparison Visualization...")
    create_performance_comparison()
    
    print("All visualizations created successfully!")
    print("\nGenerated files:")
    print("- neural_network_architecture.png")
    print("- activation_functions.png") 
    print("- training_progress.png")
    print("- gradient_flow.png")
    print("- mathematical_concepts.png")
    print("- performance_comparison.png")