from commands2 import Subsystem, Command
from typing import Callable
from wpimath.kinematics import ChassisSpeeds

# The Drive subsystem - responsible for moving our robot.

# The Subsystem base class 
class Drive(Subsystem):
  def __init__(self):
    # Calls the Subsystem __init__ method
    super().__init__()
    
    # TODO: Create the correct kinematics object
    # Kinematics provide a model of how the robot will move based on wheel motion.
    # DifferentialDriveKinematics - aka: "Tank Drive"
    # MecanumDriveKinematics - Wheel can only move forward and backward, but diagonal rollers allow moving side-to-side
    # SwerveDrive4Kinematics - Wheels can rotate (like shopping cart wheels), move forward and backward.
    
    # Create SparkMax, DifferentialModule or SwerveModule objects as needed here
    
    
  def driveCommand(self, input: Callable[[], ChassisSpeeds]) -> Command:
    """Returns a command that drives the robot"""
    # We can rewrite this more concisely by using a lambda. A lambda is just a convenient way to create a short one-line method:
    # return self.run(lambda: self._drive(input()))
    def action():
      self._drive(input())
    return self.run(action)

  def stopCommand(self) -> Command:
    """Returns a command that stops the robot"""
    return self.runOnce(lambda: self._drive(ChassisSpeeds()))
  
  def _drive(self, chassisSpeeds: ChassisSpeeds) -> None:
    """Private method that """
    # TODO: Implement Drive._drive method
    # This method should use self._kinematics to convert chassis speeds into wheel speeds, then set the wheel speeds
    pass
  
  def getChassisSpeeds(self) -> ChassisSpeeds:
    """Gets the velocity of the robot based solely on wheel odometry"""
    # TODO: Implement Drive.getChassisSpeeds
    pass