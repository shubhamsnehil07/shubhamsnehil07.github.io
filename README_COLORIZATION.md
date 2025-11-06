# Image Colorization Training Script - Fixed Version

This script provides a robust implementation of an image colorization system with comprehensive error handling for matplotlib ImportError and numpy compatibility issues.

## Features

### 1. **Dependency Management**
- ✅ Explicit version compatibility checks for numpy and matplotlib
- ✅ Graceful handling of import errors with helpful suggestions
- ✅ Automatic detection of missing dependencies
- ✅ Clear error messages with installation instructions

### 2. **Import Error Handling**
- ✅ Try-except blocks around all problematic imports
- ✅ Checks numpy version compatibility before importing matplotlib
- ✅ Fallback options when matplotlib is unavailable
- ✅ Warnings for old package versions

### 3. **Environment Setup**
- ✅ Automatic check for numpy/matplotlib version conflicts
- ✅ Detailed suggestions for fixing import issues
- ✅ Option to reinstall packages with correct versions
- ✅ Support for multiple installation methods

### 4. **Visualization Options**
- ✅ Optional matplotlib usage with automatic fallback
- ✅ PIL-based visualization as backup
- ✅ Training can continue even if plotting fails
- ✅ High-quality image comparison outputs

## Installation

### Quick Start

```bash
# Install required dependencies
pip install numpy matplotlib Pillow

# For full functionality with training
pip install torch torchvision numpy matplotlib Pillow
```

### Recommended Installation (Compatible Versions)

```bash
# Use these versions if you encounter import errors
pip install numpy==1.21.0 matplotlib==3.5.0 Pillow==9.0.0
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Fresh Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install numpy matplotlib torch torchvision Pillow
```

## Usage

### Basic Usage

```bash
python image_colorization_fixed.py
```

### Expected Output

```
Checking dependencies...
✓ NumPy version 2.3.4 loaded successfully
✓ Matplotlib version 3.10.7 loaded successfully
✓ Visualization with matplotlib enabled
✓ PyTorch version 2.0.0 loaded successfully

======================================================================
IMAGE COLORIZATION TRAINING SCRIPT
======================================================================

======================================================================
CONFIGURATION
======================================================================
  Device: cuda
  Image size: 256x256
  Batch size: 16
  Learning rate: 0.001
  Epochs: 10
  Matplotlib available: True
======================================================================
```

## Architecture

### Model: ColorizationCNN
- **Input**: Grayscale image (L channel from LAB color space)
- **Output**: Color channels (a, b channels from LAB color space)
- **Architecture**: U-Net style encoder-decoder with skip connections
- **Layers**:
  - Encoder: 3 convolutional blocks with max pooling
  - Bottleneck: 512-channel feature extraction
  - Decoder: 3 upsampling blocks with skip connections
  - Output: 2-channel (a, b) color prediction

### Color Space Pipeline
1. Load RGB image
2. Convert to LAB color space
3. Split into L (grayscale) and ab (color) channels
4. Train model to predict ab from L
5. Combine predicted ab with input L
6. Convert back to RGB for visualization

## Error Handling

### Scenario 1: NumPy Import Error

```
======================================================================
DEPENDENCY ISSUES DETECTED
======================================================================
  • NumPy import failed: No module named 'numpy'

Suggested fixes:
  1. Reinstall numpy and matplotlib:
     pip install --upgrade --force-reinstall numpy matplotlib

  2. Use compatible versions:
     pip install numpy==1.21.0 matplotlib==3.5.0
...
```

### Scenario 2: Matplotlib Import Error

If matplotlib fails to import, the script automatically falls back to PIL:

```
⚠ Warning: Matplotlib not available - ImportError: ...
⚠ Running without matplotlib - visualizations will be saved as images only
```

Training continues normally, with images saved using PIL instead.

### Scenario 3: PyTorch Not Available

```
⚠ Warning: PyTorch not available - No module named 'torch'
  Install with: pip install torch torchvision

ERROR: PyTorch is required for training
Install with: pip install torch torchvision
```

## Configuration

Edit the `Config` class to customize training:

```python
class Config:
    # Model settings
    input_channels = 1
    output_channels = 2
    
    # Training settings
    batch_size = 16
    learning_rate = 0.001
    num_epochs = 10
    
    # Data settings
    image_size = 256
    
    # Paths
    data_dir = "./data/images"
    checkpoint_dir = "./checkpoints"
    output_dir = "./outputs"
```

## Project Structure

```
.
├── image_colorization_fixed.py    # Main script with all fixes
├── data/
│   └── images/                    # Training images (RGB format)
├── checkpoints/                   # Model checkpoints (auto-created)
└── outputs/                       # Colorized results (auto-created)
```

## Key Components

### 1. Version Checking
```python
def check_version_compatibility():
    """Check numpy and matplotlib version compatibility"""
    # Returns (numpy_ok, matplotlib_ok, errors)
```

### 2. Visualizer Class
```python
class Visualizer:
    @staticmethod
    def save_image_pil(image_array, path, title=""):
        """Save using PIL (fallback)"""
    
    @staticmethod
    def save_image_matplotlib(image_array, path, title=""):
        """Save using matplotlib (preferred)"""
    
    @staticmethod
    def save_comparison(gray_img, colored_img, target_img, path):
        """Save side-by-side comparison"""
```

### 3. ColorConverter Class
```python
class ColorConverter:
    @staticmethod
    def rgb_to_lab(rgb_img):
        """Convert RGB to LAB color space"""
    
    @staticmethod
    def lab_to_rgb(lab_img):
        """Convert LAB to RGB color space"""
```

## Testing

A test script is provided to verify all features:

```bash
python test_colorization_features.py
```

Expected output:
```
Testing image_colorization_fixed.py features...

Test 1: Version Compatibility Check
✓ Test 1 passed

Test 2: Visualizer (PIL fallback)
✓ Test 2 passed

Test 3: Visualizer (Matplotlib)
✓ Test 3 passed

...

All tests passed! ✓
```

## Troubleshooting

### Issue: `numpy.core.multiarray failed to import`

**Cause**: Version mismatch between numpy and matplotlib

**Solution**:
```bash
pip uninstall numpy matplotlib
pip install numpy==1.21.0 matplotlib==3.5.0
```

### Issue: `ImportError: cannot import name 'Axes3D'`

**Cause**: Corrupted matplotlib installation

**Solution**:
```bash
pip install --upgrade --force-reinstall matplotlib
```

### Issue: Training is slow

**Solution**: Enable CUDA if available
```python
# The script auto-detects CUDA
# To force CPU: Config.device = "cpu"
# To force CUDA: Config.device = "cuda"
```

## Advanced Usage

### Custom Dataset

Place your RGB images in the data directory:
```bash
mkdir -p data/images
cp /path/to/your/images/*.jpg data/images/
```

### Resume Training

Modify the script to load a checkpoint:
```python
checkpoint = torch.load('checkpoints/model_epoch_5.pth')
model.load_state_dict(checkpoint['model_state_dict'])
```

### Inference Only

```python
from image_colorization_fixed import ColorizationCNN, test_colorization

model = ColorizationCNN()
model.load_state_dict(torch.load('checkpoints/best_model.pth')['model_state_dict'])
test_colorization(model, 'input.jpg', 'outputs/', 'cpu')
```

## Limitations

1. Simplified LAB conversion (for production, use cv2 or skimage)
2. Synthetic data generation if no images available (for demonstration)
3. Basic U-Net architecture (can be enhanced with attention, residual blocks, etc.)

## Future Enhancements

- [ ] Add support for video colorization
- [ ] Implement perceptual loss functions
- [ ] Add GAN-based colorization option
- [ ] Support for batch inference
- [ ] Web interface for easy testing
- [ ] Pre-trained model weights

## License

This script is provided as-is for educational and research purposes.

## Credits

- U-Net architecture inspired by Ronneberger et al.
- LAB color space conversion based on CIE standards
- Error handling patterns from production ML systems
