# redrawing_master

## Overview

redrawing_master is a PyQt5 application that displays an image on the right half of the screen and projects the cursor
position from the left half onto the image area.

## Features

- **Image Display:** Shows an image on the right side of the screen.
- **Cursor Projection:** Displays a red circle indicating the cursor's position from the left side.
- **Zoom:** Scale the image in and out using the mouse wheel.
- **Adjustable Projection Radius:** Change the size of the cursor projection by holding `Ctrl` and using the mouse
  wheel.
- **Drag Image:** Move the image within the window by clicking and dragging with the left mouse button.
- **Clipboard Integration:** Automatically updates the displayed image when an image is copied to the clipboard.

## Controls

- **Zoom In/Out:**
    - **Action:** Scroll the mouse wheel.
    - **Effect:** Increases or decreases the scale of the displayed image.

- **Adjust Projection Radius:**
    - **Action:** Hold `Ctrl` and scroll the mouse wheel.
    - **Effect:** Increases or decreases the size of the cursor projection circle.

- **Move Image:**
    - **Action:** Click and hold the left mouse button on the image, then drag.
    - **Effect:** Moves the image within the window.

- **Change Displayed Image:**
    - **Action:** Copy an image to the clipboard (e.g., take a screenshot or copy an image file).
    - **Effect:** The application automatically updates to display the new image.

## Requirements

- Python 3.6 or higher
- PyQt5

## Installation of Dependencies

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

This project is licensed under the MIT License.

## Contact

For any questions or support, please contact [igorpheik@gmail.com](mailto:igorpheik@gmail.com).