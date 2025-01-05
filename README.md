# redrawing_master

## Overview

redrawing_master is a PyQt5 application that displays an image on the right half of the screen and projects the cursor
position from the left half onto the image area.

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
