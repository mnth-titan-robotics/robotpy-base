#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import enum
import commands2
from subsystems.drive import Drive
from commands.auto import Auto
from commands.game import Game

# Create an alias to simplify usage
cmd = commands2.cmd


class RobotContainer:
  """This class is where the bulk of the robot should be declared. Since Command-based is a
  "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
  periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
  subsystems, commands, and button mappings) should be declared here.
  """

  # The enum used as keys for selecting the command to run.
  class CommandSelector(enum.Enum):
    ONE = enum.auto()
    TWO = enum.auto()
    THREE = enum.auto()

  # An example selector method for the selectcommand.
  def select(self) -> CommandSelector:
    """Returns the selector that will select which command to run.
    Can base this choice on logical conditions evaluated at runtime.
    """
    return self.CommandSelector.ONE

  def __init__(self) -> None:
    self._initSubsystems()
    self._initCommands()
    # Configure the button bindings
    self._initTriggers()
    
  def _initSubsystems(self):
    """Initializes subsystems. Should only be called from __init__"""
    self.drive = Drive()
  
  def _initCommands(self):
    """Initializes commands. Should only be called from __init__"""
    self.game = Game(self)
    self.auto = Auto(self)

  def _initTriggers(self) -> None:
    """Use this method to define your button->command mappings."""
    self._configureDriverBindings()
    self._configureOperatorBindings()

  def _configureDriverBindings(self) -> None:
    # All possible XBOX controller inputs are included below for easy reference.
    # Leaving unused, commented lines helps us keep track of what inputs aren't being used.
    # self.driver.rightStick().whileTrue(cmd.none())
    # self.driver.leftStick().whileTrue(cmd.none())
    # self.driver.leftTrigger().whileTrue(cmd.none())
    # self.driver.rightTrigger().whileTrue(cmd.none())
    # self.driver.rightBumper().whileTrue(cmd.none())
    # self.driver.leftBumper().whileTrue(cmd.none())
    # self.driver.povUp().whileTrue(cmd.none())
    # self.driver.povDown().whileTrue(cmd.none())
    # self.driver.povLeft().whileTrue(cmd.none())
    # self.driver.povRight().whileTrue(cmd.none())
    # self.driver.a().whileTrue(cmd.none())
    # self.driver.b().whileTrue(cmd.none())
    # self.driver.y().whileTrue(cmd.none())
    # self.driver.x().whileTrue(cmd.none())
    # self.driver.start().whileTrue(cmd.none())
    # self.driver.back().whileTrue(cmd.none())
    pass

  def _configureOperatorBindings(self) -> None:
    # All possible XBOX controller inputs are included below for easy reference.
    # Leaving unused, commented lines helps us keep track of what inputs aren't being used.
    # self.operator.rightStick().whileTrue(cmd.none())
    # self.operator.leftStick().whileTrue(cmd.none())
    # self.operator.leftTrigger().whileTrue(cmd.none())
    # self.operator.rightTrigger().whileTrue(cmd.none())
    # self.operator.rightBumper().whileTrue(cmd.none())
    # self.operator.leftBumper().whileTrue(cmd.none())
    # self.operator.povUp().whileTrue(cmd.none())
    # self.operator.povDown().whileTrue(cmd.none())
    # self.operator.povLeft().whileTrue(cmd.none())
    # self.operator.povRight().whileTrue(cmd.none())
    # self.operator.a().whileTrue(cmd.none())
    # self.operator.b().whileTrue(cmd.none())
    # self.operator.y().whileTrue(cmd.none())
    # self.operator.x().whileTrue(cmd.none())
    # self.operator.start().whileTrue(cmd.none())
    # self.operator.back().whileTrue(cmd.none())
    pass

  def getAutonomousCommand(self) -> commands2.Command:
    """Use this to pass the autonomous command to the main {Robot} class.

    :returns: the command to run in autonomous
    """
    return self.auto.get()
