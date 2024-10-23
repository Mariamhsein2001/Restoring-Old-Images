# Revivapix - Breathe New Life into Your Old Photos

Revivapix is an AI-powered tool designed to bring your old, damaged photos back to life. Whether it's scratches, smudges, or faded sections, Revivapix restores your images with precision and ease, giving them a second chance to shine. Using advanced machine learning techniques, this tool is perfect for anyone looking to preserve precious memories with a modern touch.

## Key Features

- **Automatic Scratch & Smudge Removal**: Revivapix uses state-of-the-art AI models to intelligently detect and repair damaged areas.
- **Simple Interface**: No need for technical expertise—just upload your image, and Revivapix handles the rest.
- **Fast Processing**: Get your restored images in seconds, thanks to efficient model inference and Docker optimization.

## Models Used
Revivapix relies on two powerful AI models:

pix2pix for handling scratches and smudges, based on the CycleGAN and pix2pix repository.
Deep Convolutional Neural Networks (DCNN) for restoring faded images.
These models have been fine-tuned for optimal performance on old and damaged photographs, ensuring the best possible restoration quality.

## Getting Started

Follow these steps to set up Revivapix and start restoring your images!

### 1. Clone the Repository

First, you'll need to clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/revivapix.git
cd revivapix
```

### 2. Add Model Checkpoints

To power the restoration process, Revivapix requires specific AI model checkpoints. Contact me to request the necessary files. Once you have them, place the checkpoints in the following directory:

```bash
revivapix/scratch_smudge_restoration/checkpoints/
```

### 3. Build and Run the Application

Revivapix uses Docker to streamline the setup process. Make sure Docker is installed, then run the following command to build the environment and start the service:

```bash
docker-compose up --build
```

### 4. Access the Restoration Tool

Once the Docker container is running, you can access Revivapix by navigating to:

```
http://localhost:5000
```

From here, you can upload old images and start restoring them instantly!

---

