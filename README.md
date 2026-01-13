🚀 Futuristic Voxel Studio (Hand-Tracking & AR Drawing)
A high-tech, real-time augmented reality drawing application built with OpenCV and MediaPipe. This studio allows users to create 2D/3D-style voxel art in mid-air using hand gestures.

✨ Features
Pinch-to-Draw Interaction: Use your thumb and index finger to trigger the drawing process.

Intelligent Voxel Streaming: Once the "lock-on" circle completes, move your hand to draw continuous lines of voxels effortlessly.

Ghost Silhouette Mode: A real-time preview of the target grid cell before you start drawing.

Futuristic HUD: A sleek, minimal user interface with premium color palettes (Electric Blue, Crimson Red, etc.).

HD Support: Optimized for high-resolution camera feeds (1280x720).

Smart Skeleton Tracking: Precise hand landmark detection for an elite "Iron Man" style experience.

🛠️ Tech Stack
Python 3.10+

OpenCV: Image processing and UI rendering.

MediaPipe: High-performance ML-based hand tracking.

NumPy: Efficient coordinate and grid calculations.
🚀 Getting StartedPrerequisitesEnsure you have Python installed, then install the required libraries:Bashpip install opencv-python mediapipe numpy
Installation & UsageClone the repository:Bashgit clone https://github.com/yourusername/futuristic-voxel-studio.git
Navigate to the project folder:Bashcd futuristic-voxel-studio
Run the application:Bashpython voxel_studio.py
🎮 ControlsKeyActionPinch (Thumb + Index)Activate Radar & Start DrawingMove Hand (While Pinching)Stream/Draw continuous voxelsRCycle through premium colorsCClear the entire canvasQQuit the application📺 PreviewThe application detects your hand and overlays a "Tech Radar" on your index finger. Hold the pinch for 1.5 seconds to initiate the Stream Mode, allowing you to paint across the screen in real-time.
