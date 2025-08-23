from typing import TYPE_CHECKING
from enum import Enum, auto
from wpimath.kinematics import ChassisSpeeds
from commands2 import Command, cmd
from wpilib import SendableChooser, SmartDashboard
from wpimath.geometry import Transform2d

if TYPE_CHECKING: from robotcontainer import RobotContainer


class Auto:
  def __init__(
          self,
          robot: "RobotContainer"
  ) -> None:
    self._robot = robot

    self._auto = cmd.none()

    # Add Robot/Auto to SmartDashboard with options
    self._autos = SendableChooser()
    # Default 'None' auto, does nothing. The second parameter is a function that will be called in our onChange callback below
    self._autos.setDefaultOption("None", cmd.none)
    self._autos.addOption("[Center]", self.auto_center)
    # When the selected auto changes call the function (eg: cmd.none(), self.auto_center()) to get the command, then store it in self._auto
    self._autos.onChange(lambda auto: self.set(auto()))
    # Send the list of options to SmartDashboard
    SmartDashboard.putData("Robot/Auto", self._autos)

  def get(self) -> Command:
    return self._auto

  def set(self, auto: Command) -> None:
    self._auto = auto

  def auto_center(self) -> Command:
    # Move forward at 25% speed for 3.25s, then stop
    drive = self._robot.drive
    speeds = ChassisSpeeds(vx=0.25)
    return cmd.sequence(
      drive.driveCommand(speeds).withTimeout(3.25),
      drive.stopCommand()
    )
