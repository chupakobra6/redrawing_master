# Redrawing Master

A PyQt5 application that provides cursor projection functionality for digital art and tracing.

## Features

- Real-time cursor tracking and projection
- Image scaling and positioning
- Clipboard image support
- Translucent overlay window
- Cross-platform support (Windows, macOS, Linux)

## Requirements

- Python 3.6+
- PyQt5
- PIL/Pillow (for image handling)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## macOS Specific Setup

### macOS Permissions (Optional)

On some macOS systems, you may need to grant permissions for full functionality:

#### Accessibility Permissions
If cursor tracking doesn't work, you may need accessibility permissions:
1. Open System Preferences/Settings → Security & Privacy → Privacy
2. Select "Accessibility" from the left sidebar
3. Add Terminal.app or Python to the list

The application will work on most modern macOS systems without requiring special permissions.

### High DPI Support

The application automatically detects and configures High DPI support for Retina displays on macOS.

### Window Behavior

On macOS, the application window:
- Stays on top of other windows
- Accounts for the menu bar and dock positioning
- Maintains focus behavior appropriate for overlay applications
- Automatically polls clipboard for new images (no need to click the window)

### Clipboard Behavior on macOS

The application uses automatic polling to detect clipboard changes on macOS, so you don't need to click on the window after copying an image. However, if automatic detection doesn't work, you can:
- Press **Cmd+V** while the window is focused to manually update from clipboard
- Click on the window to ensure it receives focus

## Usage

1. **Cursor Tracking**: The red circle shows your cursor position projected onto the overlay
2. **Image Scaling**: Use mouse wheel to zoom in/out
3. **Cursor Size**: Hold Ctrl/Cmd + mouse wheel to adjust cursor size
4. **Image Positioning**: Click and drag to move the reference image
5. **Clipboard Support**: Copy any image to clipboard and it will automatically replace the current reference

## Controls

- **Mouse Wheel**: Zoom image in/out
- **Ctrl/Cmd + Mouse Wheel**: Adjust cursor size
- **Left Click + Drag**: Move reference image
- **Clipboard**: Automatically loads images from clipboard
- **Cmd+V / Ctrl+V**: Manually update image from clipboard (useful on macOS)

## Troubleshooting

### macOS Issues

**"App can't access cursor position"**
- Try granting accessibility permissions as described above
- Restart the application after granting permissions

**"Clipboard images don't update automatically"**
- Try using Cmd+V to manually update from clipboard
- The automatic polling should work on most macOS systems

**"Window doesn't stay on top"**
- This is expected behavior on macOS for accessibility
- The window will stay visible but may not always be the frontmost

**"App crashes on startup"**
- Check that the reference image (gojo.png) exists
- Verify PyQt5 is properly installed
- Check Console.app for detailed error messages

### General Issues

**"Image doesn't load"**
- Ensure the image file exists in the same directory as main.py
- Check that the image format is supported (PNG, JPG, etc.)
- Try copying a different image to clipboard

**"Window positioning is wrong"**
- The app positions itself on the right half of your primary display
- For multi-monitor setups, ensure your primary display is set correctly

## File Structure

```
redrawing_master/
├── main.py          # Main application file
├── requirements.txt # Python dependencies
├── README.md       # This file
├── logo.png        # Application icon
└── gojo.png        # Default reference image
```

## License

This project is open source and available under the MIT License.
