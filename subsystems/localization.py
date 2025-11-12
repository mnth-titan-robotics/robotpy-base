from commands2 import Subsystem
from ntcore import NetworkTableInstance
from wpilib import Timer
from wpimath.geometry import Pose3d
from services.questnav import QuestNav


class Localization(Subsystem):
    _pose = Pose3d()
    
    # Tracking variables for diagnostics
    total_frames_received = 0
    last_frame_count = 0
    frame_drops = 0
    start_time = Timer.getFPGATimestamp()
    frame_rate_samples = []
    last_frame_time = 0.0

    def __init__(self, questnav: QuestNav):
        self.questnav = questnav
        nt_instance = NetworkTableInstance.getDefault()
        self.nt_table = nt_instance.getTable("/Robot/Localization")
        self._pose_publisher = self.nt_table.getStructTopic("Pose", Pose3d).publish()
        
    def get_pose(self) -> Pose3d:
        return self._pose
    
    def _process_pose_frames(self):
        frames = self.questnav.get_all_unread_pose_frames()
        current_time = Timer.getFPGATimestamp()

        # Process each frame (like robot code would)
        for frame in frames:
            self.total_frames_received += 1

            # Detect frame drops (only check first frame in batch)
            if self.last_frame_count > 0 and frame == frames[0]:
                expected = self.last_frame_count + 1
                if frame.frame_count > expected:
                    drops = frame.frame_count - expected
                    self.frame_drops += drops
                    # if drops > 5:  # Only log significant drops
                    #     self._log(f"[WARN] Dropped {drops} frames")

            self.last_frame_count = frame.frame_count

            # Calculate frame rate
            if self.last_frame_time > 0:
                dt = current_time - self.last_frame_time
                if dt > 0:
                    fps = 1.0 / dt
                    self.frame_rate_samples.append(fps)
                    if len(self.frame_rate_samples) > 10:
                        self.frame_rate_samples.pop(0)

            self.last_frame_time = current_time

            # Update pose display with latest frame
            self._pose = frame.quest_pose_3d
    
    def periodic(self):
        # Process any pending commands for the questnav
        self.questnav.command_periodic()
        self._process_pose_frames()
        self._update_telemetry()

    def _update_telemetry(self):
        self._pose_publisher.set(self._pose)
        self.nt_table.getEntry("TotalFrames").setInteger(self.total_frames_received)
        self.nt_table.getEntry("FrameDrops").setInteger(self.frame_drops)
        self.nt_table.getEntry("LastFrameTime").setFloat(self.last_frame_time)