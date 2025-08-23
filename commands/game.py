from typing import TYPE_CHECKING
from commands2 import Command, cmd
from wpilib import RobotBase

if TYPE_CHECKING: from robotcontainer import RobotContainer


class Game:
  def __init__(self, robot: "RobotContainer"):
    self._robot = robot

  # TODO: Add any composite commands (anything that involves multiple steps or multiple subsystems) here
  # This is an example from The Lady Cans (FRC 2881):
  # def intakeCoralFromGround(self) -> Command:
  #   return (
  #     cmd.sequence(
  #       cmd.parallel(
  #         self._robot.elevator.setPosition(constants.Game.Field.Targets.kTargetPositions[TargetPositionType.IntakeReady].elevator),
  #         self._robot.wrist.setPosition(constants.Game.Field.Targets.kTargetPositions[TargetPositionType.IntakeReady].wrist).withTimeout(2.0),
  #         self._robot.arm.setPosition(constants.Game.Field.Targets.kTargetPositions[TargetPositionType.IntakeReady].arm),
  #         self._robot.intake.intake()
  #       ).until(lambda: self.isIntakeHolding()),
  #       self.liftCoralFromIntake()
  #     )
  #     .onlyIf(lambda: not self.isGripperHolding())
  #     .withName("Game:IntakeCoralFromGround")
  #   )
