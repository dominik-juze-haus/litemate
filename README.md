# Litemate
Exposure and white balance change point detection plugin script for DaVinci Resolve editing software

##__About__ 

Litemate is an assistive tool for video correction post production for detection and correction of color changes in long static shots
best suitable for:
- talking heads
- podcasts
- recordings of theatre

## How to use
You must use Python 3.12 or greater

### Installation
1. Install ffmpeg v7.1 or greater (hardware acceleration enabled builds are recommended)
2. Add DaVinci Resolve Script API to system environment variables (check guide in dependencies folder)
2. Install the dependencies from the requirements.txt `pip install -r requirements.txt`
	- copy the build files to selected directory
	- add the bin folder to PATH
3. install cuda 13 SDK

- Make shure that Python 3.12 or greater is first version in Path. You can verify the DaVinci Python version in DaVinci scripting console.
- Make shure that scripting is enabled in Resolve
    - Preferences > General > External scripting using: Local



### Using the script
1. In DaVinci Resolve, select a desired clip and create a new timeline from that clip
2. Find a reference frame with the desired attributes and place a marker on top
    - label the marker: reference
3. Keep the timeline open and run the script
4. Select the desired analyses and parameters
5. Run the analysis
6. Preview the results and tweak the parameters
7. Send the markers to DaVinci Resolve
8. Preview the marked up timeline in Resolve

The software is in development!

 
