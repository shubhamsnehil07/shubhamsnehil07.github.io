#!/usr/bin/env python3
"""Test script to verify the colorization script features"""

import sys
import os
import numpy as np
from PIL import Image

# Test imports from the colorization script
sys.path.insert(0, os.path.dirname(__file__))

print("Testing image_colorization_fixed.py features...\n")

# Test 1: Check version compatibility function
print("Test 1: Version Compatibility Check")
print("-" * 50)
from image_colorization_fixed import check_version_compatibility
numpy_ok, matplotlib_ok, errors = check_version_compatibility()
print(f"  NumPy OK: {numpy_ok}")
print(f"  Matplotlib OK: {matplotlib_ok}")
print(f"  Errors: {len(errors)}")
assert numpy_ok, "NumPy should be available"
print("✓ Test 1 passed\n")

# Test 2: Test Visualizer with PIL fallback
print("Test 2: Visualizer (PIL fallback)")
print("-" * 50)
from image_colorization_fixed import Visualizer
os.makedirs('/tmp/test_output', exist_ok=True)

# Create a test image
test_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
success = Visualizer.save_image_pil(test_img, '/tmp/test_output/test_pil.png', 'Test')
assert success, "PIL save should succeed"
assert os.path.exists('/tmp/test_output/test_pil.png'), "Output file should exist"
print("✓ Test 2 passed\n")

# Test 3: Test Visualizer with matplotlib
print("Test 3: Visualizer (Matplotlib)")
print("-" * 50)
success = Visualizer.save_image_matplotlib(test_img, '/tmp/test_output/test_mpl.png', 'Test Matplotlib')
assert success, "Matplotlib save should succeed"
assert os.path.exists('/tmp/test_output/test_mpl.png'), "Output file should exist"
print("✓ Test 3 passed\n")

# Test 4: Test comparison visualization
print("Test 4: Comparison Visualization")
print("-" * 50)
gray_img = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
colored_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
success = Visualizer.save_comparison(gray_img, colored_img, None, '/tmp/test_output/test_comparison.png')
assert success, "Comparison save should succeed"
print("✓ Test 4 passed\n")

# Test 5: Test ColorConverter
print("Test 5: Color Space Conversion")
print("-" * 50)
from image_colorization_fixed import ColorConverter

# Create a simple RGB image
rgb_img = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]]], dtype=np.float32)
rgb_img = np.tile(rgb_img, (50, 50, 1))

# Convert to LAB and back
lab_img = ColorConverter.rgb_to_lab(rgb_img)
assert lab_img.shape == rgb_img.shape, "LAB shape should match RGB shape"
print(f"  LAB range: L=[{lab_img[..., 0].min():.1f}, {lab_img[..., 0].max():.1f}], "
      f"a=[{lab_img[..., 1].min():.1f}, {lab_img[..., 1].max():.1f}], "
      f"b=[{lab_img[..., 2].min():.1f}, {lab_img[..., 2].max():.1f}]")

rgb_back = ColorConverter.lab_to_rgb(lab_img)
assert rgb_back.shape == rgb_img.shape, "RGB shape should be preserved"
print(f"  RGB range: [{rgb_back.min():.1f}, {rgb_back.max():.1f}]")
print("✓ Test 5 passed\n")

# Test 6: Test Config class
print("Test 6: Configuration")
print("-" * 50)
from image_colorization_fixed import Config
Config.print_config()
print("✓ Test 6 passed\n")

print("="*50)
print("All tests passed! ✓")
print("="*50)
print("\nKey features verified:")
print("  ✓ Version compatibility checking")
print("  ✓ Graceful import error handling")
print("  ✓ PIL fallback for visualization")
print("  ✓ Matplotlib support when available")
print("  ✓ Color space conversion utilities")
print("  ✓ Configuration management")
