#!/usr/bin/env python3
"""
Image Colorization Training Script - Fixed Version
Addresses matplotlib ImportError and numpy compatibility issues
"""

import sys
import warnings
import os
from typing import Optional, Tuple, Any

# ============================================================================
# DEPENDENCY MANAGEMENT AND VERSION CHECKING
# ============================================================================

def check_version_compatibility():
    """
    Check for numpy and matplotlib version compatibility.
    Returns a tuple of (numpy_ok, matplotlib_ok, error_messages)
    """
    errors = []
    numpy_ok = False
    matplotlib_ok = False
    
    # Check numpy
    try:
        import numpy as np
        numpy_version = np.__version__
        numpy_ok = True
        print(f"✓ NumPy version {numpy_version} loaded successfully")
        
        # Check for known problematic versions
        major, minor = map(int, numpy_version.split('.')[:2])
        if major < 1 or (major == 1 and minor < 19):
            warnings.warn(f"NumPy version {numpy_version} is old. Consider upgrading to 1.19+")
    except ImportError as e:
        errors.append(f"NumPy import failed: {e}")
    except Exception as e:
        errors.append(f"NumPy version check failed: {e}")
    
    # Check matplotlib (only if numpy succeeded)
    if numpy_ok:
        try:
            # Try importing matplotlib with explicit backend
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            import matplotlib.pyplot as plt
            matplotlib_version = matplotlib.__version__
            matplotlib_ok = True
            print(f"✓ Matplotlib version {matplotlib_version} loaded successfully")
        except ImportError as e:
            errors.append(f"Matplotlib import failed: {e}")
            print(f"⚠ Warning: Matplotlib not available - {e}")
        except Exception as e:
            errors.append(f"Matplotlib setup failed: {e}")
            print(f"⚠ Warning: Matplotlib issue - {e}")
    
    return numpy_ok, matplotlib_ok, errors


def suggest_fix_for_import_error(errors):
    """Provide helpful suggestions for fixing import errors."""
    print("\n" + "="*70)
    print("DEPENDENCY ISSUES DETECTED")
    print("="*70)
    
    for error in errors:
        print(f"  • {error}")
    
    print("\nSuggested fixes:")
    print("  1. Reinstall numpy and matplotlib:")
    print("     pip install --upgrade --force-reinstall numpy matplotlib")
    print("\n  2. Use compatible versions:")
    print("     pip install numpy==1.21.0 matplotlib==3.5.0")
    print("\n  3. Create a fresh virtual environment:")
    print("     python -m venv venv")
    print("     source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("     pip install numpy matplotlib torch torchvision Pillow")
    print("="*70 + "\n")


# ============================================================================
# SAFE IMPORTS WITH ERROR HANDLING
# ============================================================================

print("Checking dependencies...")
NUMPY_OK, MATPLOTLIB_OK, IMPORT_ERRORS = check_version_compatibility()

if not NUMPY_OK:
    suggest_fix_for_import_error(IMPORT_ERRORS)
    sys.exit(1)

# Core imports (required)
import numpy as np
from PIL import Image
import warnings

# Optional matplotlib imports with fallback
if MATPLOTLIB_OK:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    print("✓ Visualization with matplotlib enabled")
else:
    plt = None
    print("⚠ Running without matplotlib - visualizations will be saved as images only")

# Try importing PyTorch
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    import torchvision.transforms as transforms
    TORCH_OK = True
    print(f"✓ PyTorch version {torch.__version__} loaded successfully")
except ImportError as e:
    TORCH_OK = False
    print(f"⚠ Warning: PyTorch not available - {e}")
    print("  Install with: pip install torch torchvision")

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Training configuration"""
    # Model settings
    input_channels = 1  # L channel (grayscale)
    output_channels = 2  # a, b channels (color)
    
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
    
    # Device
    @classmethod
    def get_device(cls):
        """Get the appropriate device for training"""
        try:
            if TORCH_OK and torch.cuda.is_available():
                return "cuda"
        except Exception:
            pass
        return "cpu"
    
    device = "cpu"  # Default, will be updated at runtime
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        # Update device at runtime
        cls.device = cls.get_device()
        
        print("\n" + "="*70)
        print("CONFIGURATION")
        print("="*70)
        print(f"  Device: {cls.device}")
        print(f"  Image size: {cls.image_size}x{cls.image_size}")
        print(f"  Batch size: {cls.batch_size}")
        print(f"  Learning rate: {cls.learning_rate}")
        print(f"  Epochs: {cls.num_epochs}")
        print(f"  Matplotlib available: {MATPLOTLIB_OK}")
        print("="*70 + "\n")


# ============================================================================
# VISUALIZATION UTILITIES
# ============================================================================

class Visualizer:
    """Handle visualization with optional matplotlib support"""
    
    @staticmethod
    def save_image_pil(image_array: np.ndarray, path: str, title: str = ""):
        """
        Save image using PIL (fallback method without matplotlib)
        
        Args:
            image_array: RGB image as numpy array [H, W, 3] in range [0, 255]
            path: Output path
            title: Optional title (not used in PIL mode)
        """
        try:
            # Ensure correct range and type
            image_array = np.clip(image_array, 0, 255).astype(np.uint8)
            
            # Convert to PIL Image
            img = Image.fromarray(image_array, mode='RGB')
            
            # Save
            img.save(path)
            print(f"✓ Saved image: {path}")
            return True
        except Exception as e:
            print(f"✗ Failed to save image {path}: {e}")
            return False
    
    @staticmethod
    def save_image_matplotlib(image_array: np.ndarray, path: str, title: str = ""):
        """
        Save image using matplotlib (preferred method with better quality)
        
        Args:
            image_array: RGB image as numpy array [H, W, 3] in range [0, 255]
            path: Output path
            title: Optional title
        """
        if not MATPLOTLIB_OK or plt is None:
            # Fallback to PIL
            return Visualizer.save_image_pil(image_array, path, title)
        
        try:
            fig, ax = plt.subplots(1, 1, figsize=(10, 10))
            ax.imshow(image_array.astype(np.uint8))
            ax.axis('off')
            if title:
                ax.set_title(title, fontsize=16)
            
            plt.tight_layout()
            plt.savefig(path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            print(f"✓ Saved image: {path}")
            return True
        except Exception as e:
            print(f"⚠ Matplotlib failed: {e}, trying PIL fallback")
            return Visualizer.save_image_pil(image_array, path, title)
    
    @staticmethod
    def save_comparison(gray_img: np.ndarray, colored_img: np.ndarray, 
                       target_img: Optional[np.ndarray], path: str):
        """
        Save side-by-side comparison of images
        
        Args:
            gray_img: Grayscale input [H, W] or [H, W, 1]
            colored_img: Colorized output [H, W, 3]
            target_img: Optional ground truth [H, W, 3]
            path: Output path
        """
        # Prepare grayscale image for display
        if gray_img.ndim == 2:
            gray_img_rgb = np.stack([gray_img] * 3, axis=-1)
        elif gray_img.shape[-1] == 1:
            gray_img_rgb = np.repeat(gray_img, 3, axis=-1)
        else:
            gray_img_rgb = gray_img
        
        if MATPLOTLIB_OK and plt is not None:
            try:
                # Use matplotlib for better quality comparison
                num_images = 3 if target_img is not None else 2
                fig, axes = plt.subplots(1, num_images, figsize=(15, 5))
                
                if num_images == 2:
                    axes = [axes[0], axes[1]]
                
                axes[0].imshow(gray_img_rgb.astype(np.uint8))
                axes[0].set_title('Input (Grayscale)', fontsize=14)
                axes[0].axis('off')
                
                axes[1].imshow(colored_img.astype(np.uint8))
                axes[1].set_title('Colorized', fontsize=14)
                axes[1].axis('off')
                
                if target_img is not None:
                    axes[2].imshow(target_img.astype(np.uint8))
                    axes[2].set_title('Ground Truth', fontsize=14)
                    axes[2].axis('off')
                
                plt.tight_layout()
                plt.savefig(path, dpi=150, bbox_inches='tight')
                plt.close(fig)
                print(f"✓ Saved comparison: {path}")
                return True
            except Exception as e:
                print(f"⚠ Matplotlib comparison failed: {e}, using PIL")
        
        # Fallback: save as separate images or horizontal concatenation
        try:
            if target_img is not None:
                combined = np.hstack([gray_img_rgb, colored_img, target_img])
            else:
                combined = np.hstack([gray_img_rgb, colored_img])
            
            return Visualizer.save_image_pil(combined, path, "")
        except Exception as e:
            print(f"✗ Failed to save comparison: {e}")
            return False


# ============================================================================
# COLOR SPACE CONVERSION UTILITIES
# ============================================================================

class ColorConverter:
    """Convert between RGB and LAB color spaces"""
    
    @staticmethod
    def rgb_to_lab(rgb_img: np.ndarray) -> np.ndarray:
        """
        Convert RGB image to LAB color space
        
        Args:
            rgb_img: RGB image [H, W, 3] in range [0, 255]
        
        Returns:
            LAB image [H, W, 3] with L in [0, 100], a,b in [-128, 127]
        """
        # Normalize RGB to [0, 1]
        rgb = rgb_img.astype(np.float32) / 255.0
        
        # Convert to LAB (simplified conversion)
        # This is a simplified version - for production use cv2.cvtColor or skimage
        
        # RGB to XYZ
        rgb = np.where(rgb > 0.04045, 
                       np.power((rgb + 0.055) / 1.055, 2.4),
                       rgb / 12.92)
        
        # XYZ transformation matrix
        xyz = np.zeros_like(rgb)
        xyz[..., 0] = rgb[..., 0] * 0.4124564 + rgb[..., 1] * 0.3575761 + rgb[..., 2] * 0.1804375
        xyz[..., 1] = rgb[..., 0] * 0.2126729 + rgb[..., 1] * 0.7151522 + rgb[..., 2] * 0.0721750
        xyz[..., 2] = rgb[..., 0] * 0.0193339 + rgb[..., 1] * 0.1191920 + rgb[..., 2] * 0.9503041
        
        # Normalize by D65 white point
        xyz[..., 0] /= 0.95047
        xyz[..., 1] /= 1.00000
        xyz[..., 2] /= 1.08883
        
        # XYZ to LAB
        xyz = np.where(xyz > 0.008856,
                       np.power(xyz, 1/3),
                       (7.787 * xyz) + (16/116))
        
        lab = np.zeros_like(rgb)
        lab[..., 0] = (116 * xyz[..., 1]) - 16  # L
        lab[..., 1] = 500 * (xyz[..., 0] - xyz[..., 1])  # a
        lab[..., 2] = 200 * (xyz[..., 1] - xyz[..., 2])  # b
        
        return lab
    
    @staticmethod
    def lab_to_rgb(lab_img: np.ndarray) -> np.ndarray:
        """
        Convert LAB image to RGB color space
        
        Args:
            lab_img: LAB image [H, W, 3]
        
        Returns:
            RGB image [H, W, 3] in range [0, 255]
        """
        # LAB to XYZ
        fy = (lab_img[..., 0] + 16) / 116
        fx = lab_img[..., 1] / 500 + fy
        fz = fy - lab_img[..., 2] / 200
        
        xyz = np.stack([fx, fy, fz], axis=-1)
        xyz = np.where(np.power(xyz, 3) > 0.008856,
                       np.power(xyz, 3),
                       (xyz - 16/116) / 7.787)
        
        # Apply D65 white point
        xyz[..., 0] *= 0.95047
        xyz[..., 1] *= 1.00000
        xyz[..., 2] *= 1.08883
        
        # XYZ to RGB
        rgb = np.zeros_like(xyz)
        rgb[..., 0] = xyz[..., 0] * 3.2404542 + xyz[..., 1] * -1.5371385 + xyz[..., 2] * -0.4985314
        rgb[..., 1] = xyz[..., 0] * -0.9692660 + xyz[..., 1] * 1.8760108 + xyz[..., 2] * 0.0415560
        rgb[..., 2] = xyz[..., 0] * 0.0556434 + xyz[..., 1] * -0.2040259 + xyz[..., 2] * 1.0572252
        
        # Apply gamma correction
        rgb = np.where(rgb > 0.0031308,
                       1.055 * np.power(rgb, 1/2.4) - 0.055,
                       12.92 * rgb)
        
        # Clip and convert to [0, 255]
        rgb = np.clip(rgb * 255, 0, 255)
        
        return rgb


# ============================================================================
# MODEL ARCHITECTURE
# ============================================================================

if TORCH_OK:
    class ColorizationCNN(nn.Module):
        """
        CNN for image colorization
        Input: Grayscale image (L channel)
        Output: Color channels (a, b)
        """
        
        def __init__(self):
            super(ColorizationCNN, self).__init__()
            
            # Encoder
            self.enc_conv1 = nn.Sequential(
                nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.BatchNorm2d(64)
            )
            self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
            
            self.enc_conv2 = nn.Sequential(
                nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.BatchNorm2d(128)
            )
            self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
            
            self.enc_conv3 = nn.Sequential(
                nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.BatchNorm2d(256)
            )
            self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
            
            # Bottleneck
            self.bottleneck = nn.Sequential(
                nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.BatchNorm2d(512)
            )
            
            # Decoder
            self.upconv3 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
            self.dec_conv3 = nn.Sequential(
                nn.Conv2d(512, 256, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.BatchNorm2d(256)
            )
            
            self.upconv2 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
            self.dec_conv2 = nn.Sequential(
                nn.Conv2d(256, 128, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.BatchNorm2d(128)
            )
            
            self.upconv1 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
            self.dec_conv1 = nn.Sequential(
                nn.Conv2d(128, 64, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
                nn.ReLU(inplace=True),
                nn.BatchNorm2d(64)
            )
            
            # Output layer
            self.output = nn.Conv2d(64, 2, kernel_size=1, stride=1, padding=0)
        
        def forward(self, x):
            # Encoder
            enc1 = self.enc_conv1(x)
            pool1 = self.pool1(enc1)
            
            enc2 = self.enc_conv2(pool1)
            pool2 = self.pool2(enc2)
            
            enc3 = self.enc_conv3(pool2)
            pool3 = self.pool3(enc3)
            
            # Bottleneck
            bottleneck = self.bottleneck(pool3)
            
            # Decoder with skip connections
            up3 = self.upconv3(bottleneck)
            dec3 = torch.cat([up3, enc3], dim=1)
            dec3 = self.dec_conv3(dec3)
            
            up2 = self.upconv2(dec3)
            dec2 = torch.cat([up2, enc2], dim=1)
            dec2 = self.dec_conv2(dec2)
            
            up1 = self.upconv1(dec2)
            dec1 = torch.cat([up1, enc1], dim=1)
            dec1 = self.dec_conv1(dec1)
            
            # Output
            output = self.output(dec1)
            
            return output


# ============================================================================
# DATASET
# ============================================================================

if TORCH_OK:
    import glob  # Import here for use in ColorizationDataset
    
    class ColorizationDataset(Dataset):
        """Dataset for image colorization"""
        
        def __init__(self, image_dir: str, image_size: int = 256):
            """
            Args:
                image_dir: Directory containing color images
                image_size: Target size for images
            """
            self.image_dir = image_dir
            self.image_size = image_size
            
            # Get list of image files
            self.image_files = []
            if os.path.exists(image_dir):
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
                    self.image_files.extend(glob.glob(os.path.join(image_dir, ext)))
                    self.image_files.extend(glob.glob(os.path.join(image_dir, ext.upper())))
            
            print(f"Found {len(self.image_files)} images in {image_dir}")
            
            if len(self.image_files) == 0:
                print(f"⚠ Warning: No images found in {image_dir}")
                print("  The training will use synthetic data for demonstration")
        
        def __len__(self):
            return max(len(self.image_files), 100)  # Return at least 100 for demo
        
        def __getitem__(self, idx):
            if len(self.image_files) > 0:
                # Load real image
                img_path = self.image_files[idx % len(self.image_files)]
                img = Image.open(img_path).convert('RGB')
                img = img.resize((self.image_size, self.image_size), Image.BILINEAR)
                img_array = np.array(img).astype(np.float32)
            else:
                # Generate synthetic image for demonstration
                img_array = self._generate_synthetic_image()
            
            # Convert to LAB
            lab_img = ColorConverter.rgb_to_lab(img_array)
            
            # Split into L and ab channels
            L = lab_img[:, :, 0:1]  # [H, W, 1]
            ab = lab_img[:, :, 1:]  # [H, W, 2]
            
            # Normalize
            L = L / 50.0 - 1.0  # Normalize L to [-1, 1]
            ab = ab / 128.0  # Normalize ab to roughly [-1, 1]
            
            # Convert to tensors [C, H, W]
            L = torch.from_numpy(L.transpose(2, 0, 1))
            ab = torch.from_numpy(ab.transpose(2, 0, 1))
            
            return L, ab
        
        def _generate_synthetic_image(self):
            """Generate a synthetic colored image for demonstration"""
            img = np.zeros((self.image_size, self.image_size, 3), dtype=np.float32)
            
            # Create random colored shapes
            import random
            num_shapes = random.randint(3, 8)
            
            for _ in range(num_shapes):
                # Random color
                color = np.array([
                    random.randint(50, 255),
                    random.randint(50, 255),
                    random.randint(50, 255)
                ], dtype=np.float32)
                
                # Random position and size
                cx = random.randint(0, self.image_size)
                cy = random.randint(0, self.image_size)
                radius = random.randint(20, 60)
                
                # Draw circle
                y, x = np.ogrid[:self.image_size, :self.image_size]
                mask = (x - cx)**2 + (y - cy)**2 <= radius**2
                img[mask] = color
            
            return img


# ============================================================================
# TRAINING
# ============================================================================

if TORCH_OK:
    def train_model(model, train_loader, num_epochs, device, checkpoint_dir):
        """
        Train the colorization model
        
        Args:
            model: ColorizationCNN model
            train_loader: DataLoader for training data
            num_epochs: Number of training epochs
            device: Device to train on (cpu or cuda)
            checkpoint_dir: Directory to save checkpoints
        """
        model = model.to(device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=Config.learning_rate)
        
        print(f"\nStarting training on {device}...")
        print(f"Total batches per epoch: {len(train_loader)}")
        
        for epoch in range(num_epochs):
            model.train()
            epoch_loss = 0.0
            
            for batch_idx, (L, ab) in enumerate(train_loader):
                L = L.to(device)
                ab = ab.to(device)
                
                # Forward pass
                optimizer.zero_grad()
                predicted_ab = model(L)
                
                # Compute loss
                loss = criterion(predicted_ab, ab)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
                
                # Print progress
                if (batch_idx + 1) % 10 == 0:
                    print(f"  Epoch [{epoch+1}/{num_epochs}], "
                          f"Batch [{batch_idx+1}/{len(train_loader)}], "
                          f"Loss: {loss.item():.4f}")
            
            avg_loss = epoch_loss / len(train_loader)
            print(f"Epoch [{epoch+1}/{num_epochs}] completed - Average Loss: {avg_loss:.4f}")
            
            # Save checkpoint
            if (epoch + 1) % 5 == 0:
                checkpoint_path = os.path.join(checkpoint_dir, f"model_epoch_{epoch+1}.pth")
                torch.save({
                    'epoch': epoch + 1,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'loss': avg_loss,
                }, checkpoint_path)
                print(f"✓ Checkpoint saved: {checkpoint_path}")
        
        return model


    def test_colorization(model, test_image_path, output_dir, device):
        """
        Test the model on a single image
        
        Args:
            model: Trained ColorizationCNN model
            test_image_path: Path to test image
            output_dir: Directory to save results
            device: Device to run inference on
        """
        model.eval()
        
        # Load and preprocess image
        img = Image.open(test_image_path).convert('RGB')
        img = img.resize((Config.image_size, Config.image_size), Image.BILINEAR)
        img_array = np.array(img).astype(np.float32)
        
        # Convert to LAB
        lab_img = ColorConverter.rgb_to_lab(img_array)
        L = lab_img[:, :, 0:1]
        
        # Normalize
        L_norm = L / 50.0 - 1.0
        
        # Convert to tensor
        L_tensor = torch.from_numpy(L_norm.transpose(2, 0, 1)).unsqueeze(0).to(device)
        
        # Predict
        with torch.no_grad():
            predicted_ab = model(L_tensor)
        
        # Post-process
        predicted_ab = predicted_ab.cpu().numpy()[0].transpose(1, 2, 0)
        predicted_ab = predicted_ab * 128.0
        
        # Combine L and predicted ab
        colorized_lab = np.concatenate([L, predicted_ab], axis=-1)
        
        # Convert to RGB
        colorized_rgb = ColorConverter.lab_to_rgb(colorized_lab)
        
        # Save results
        basename = os.path.basename(test_image_path)
        output_path = os.path.join(output_dir, f"colorized_{basename}")
        
        # Save comparison
        gray_img = L[:, :, 0]
        Visualizer.save_comparison(gray_img, colorized_rgb, img_array, output_path)
        
        print(f"✓ Colorization complete: {output_path}")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main training script"""
    print("\n" + "="*70)
    print("IMAGE COLORIZATION TRAINING SCRIPT")
    print("="*70)
    
    # Print configuration
    Config.print_config()
    
    # Check if PyTorch is available
    if not TORCH_OK:
        print("ERROR: PyTorch is required for training")
        print("Install with: pip install torch torchvision")
        return 1
    
    # Create directories
    os.makedirs(Config.checkpoint_dir, exist_ok=True)
    os.makedirs(Config.output_dir, exist_ok=True)
    
    try:
        # Create dataset and dataloader
        print("\nPreparing dataset...")
        dataset = ColorizationDataset(Config.data_dir, Config.image_size)
        
        if len(dataset) == 0:
            print("⚠ Warning: Empty dataset, cannot train")
            return 1
        
        train_loader = DataLoader(
            dataset,
            batch_size=Config.batch_size,
            shuffle=True,
            num_workers=2,  # Use small number for better performance with error handling
            persistent_workers=False
        )
        
        # Create model
        print("\nInitializing model...")
        model = ColorizationCNN()
        print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
        
        # Train model
        print("\n" + "="*70)
        print("TRAINING")
        print("="*70)
        model = train_model(
            model,
            train_loader,
            Config.num_epochs,
            Config.device,
            Config.checkpoint_dir
        )
        
        print("\n" + "="*70)
        print("TRAINING COMPLETE")
        print("="*70)
        print(f"Model saved in: {Config.checkpoint_dir}")
        print(f"Outputs saved in: {Config.output_dir}")
        
        # Test on sample if available
        if len(dataset.image_files) > 0:
            print("\nTesting on sample image...")
            test_colorization(
                model,
                dataset.image_files[0],
                Config.output_dir,
                Config.device
            )
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\nERROR during training: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
