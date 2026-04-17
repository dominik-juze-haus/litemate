#!/usr/bin/env python


import DaVinciResolveScript as dvr_script


resolve = dvr_script.scriptapp("Resolve")
fusion = resolve.Fusion()

##footage_path = "I:/CODING/LiteMate/Footage/pyxis_exposure_change.mov"


class SendToDaVinci:
    def __init__(self, footage_path, frameID):
        self.footage_path = footage_path #path to the analyzed footage
        self.frameID = frameID #list of frame numbers where markers should be placed
        
        # Get the main objects
        self.projectManager = resolve.GetProjectManager()  # Get the project manager
        self.mediaStorage = resolve.GetMediaStorage() # Get the media storage
        
        # CONCEPT: load the right project (user should be already loaded to the right project)
        #self.projectManager.GotoRootFolder()
        #self.projectManager.LoadProject(project_name)
        
        self.project = self.projectManager.GetCurrentProject() # Get the current project

        self.mediaPool = self.project.GetMediaPool() # Get the media pool
        self.clip =self.mediaStorage.AddItemListToMediaPool(self.footage_path) # Add the footage to the media pool


        self.timeline = self.project.GetCurrentTimeline() # Get the new timeline
        
        try:
            self.timelinethings = self.timeline.GetItemListInTrack("video", 1) # Get the items in the video track (for debugging)
            print(self.timelinethings[0].GetName()) # Print the items in the video track (for debugging)
        except:
            self.mediaPool.AppendToTimeline(self.clip) # Append the clip to the timeline

            for frame_id in self.frameID:
                print(frame_id)
                self.timeline.AddMarker(frame_id, 'Red', 'Marker Name', 'Notes', 1, 'Secret_Word') # Add markers to the timeline at the specified frame IDs
        
        
        
        

# Call the class - send data to DaVinci Resolve
##SendToDaVinci(footage_path, [25, 100, 150])
