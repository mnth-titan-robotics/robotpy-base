# https://github.com/therekrab/autopilot
# docs: https://therekrab.github.io/autopilot/
# Autopilot is a tool developed by FRC team 3414, designed to act as a powerful solution for autonomous robot motion control.
#
# The primary goal of Autopilot is not to follow some trajectory or avoid obstacles, or even to move the robot in the fastest manner from point A 
# to point B. Instead, Autopilot excels at robot motion control on the fly, where the exact path cannot be predetermined, but constraints still need 
# to be in place.


from dataclasses import dataclass, replace
from math import hypot, log, sqrt
from typing import Optional

from wpimath.geometry import Pose2d, Rotation2d, Translation2d
from wpimath.kinematics import ChassisSpeeds
from wpimath import units


# --------------------------- Constraints -------------------------------------

@dataclass
class APConstraints:
    """Kinematic limits for the autopilot controller (SI units)."""
    velocity: units.meters_per_second = 3.0  # max speed (m/s)
    acceleration: units.meters_per_second_squared = 4.0  # max accel (m/s^2)
    jerk: float = 10.0  # shaping term used for max velocity estimation (m/s^3)


# ----------------------------- Profile ---------------------------------------

@dataclass
class APProfile:
    """Tuning and acceptance parameters for how the autopilot approaches targets.

    errorXY: allowable translational error (meters)
    errorTheta: allowable rotational error (radians)
    beelineRadius: inside this distance, drive straight at the target ignoring entry angle (meters)
    constraints: APConstraints used by the controller
    """
    errorXY: units.meters = 0.02
    errorTheta: units.radians = units.degreesToRadians(1.0)
    beelineRadius: units.meters = 0.10
    constraints: APConstraints = APConstraints()


# ------------------------------ Target ---------------------------------------

@dataclass
class APTarget:
    """Represents the desired end pose and approach configuration."""
    reference: Pose2d
    entryAngle: Optional[Rotation2d] = None  # approach heading (None => 0)
    rotationRadius: Optional[units.meters] = None  # meters; inside this we aim at final heading
    velocity: units.meters_per_second = 0.0  # desired terminal linear velocity magnitude (m/s)

    # Fluent-style helpers
    def with_entry_angle(self, angle: Rotation2d):
        self.entryAngle = angle
        return self

    def with_rotation_radius(self, meters: Optional[float]):
        self.rotationRadius = meters
        return self

    def with_velocity(self, meters_per_second: float):
        self.velocity = meters_per_second
        return self

    def without_rotation_radius(self):
        return replace(self, rotationRadius=None)

    def without_entry_angle(self):
        return replace(self, entryAngle=None)


# ----------------------------- Result ----------------------------------------

@dataclass
class APResult:
    vx: units.meters_per_second  # field-relative x velocity (m/s)
    vy: units.meters_per_second  # field-relative y velocity (m/s)
    targetAngle: Rotation2d  # the angle we want the robot to face


# ---------------------------- Autopilot --------------------------------------

class Autopilot:
    """Stateless 2D target-drive helper.

    Mirrors the semantics of the provided Java implementation.
    """

    def __init__(self, profile: APProfile):
        self._profile = profile
        self._dt = 0.020  # 20ms periodic

    # ---------------------------- Public API ---------------------------------

    def calculate(self, current: Pose2d, robotRelativeSpeeds: ChassisSpeeds, target: APTarget) -> APResult:
        """Compute the next field-relative velocity (vx, vy) and the angle to face.

        Args:
            current: current robot pose (field coordinates)
            robotRelativeSpeeds: current robot-relative ChassisSpeeds
            target: desired target configuration

        Returns:
            APResult with vx, vy (m/s, field-relative) and targetAngle (Rotation2d)
        """
        # Vector from current to goal in field frame, then into target entry-angle frame
        offset_field = target.reference.Translation() - current.Translation()
        offset = self._to_target_coordinate_frame(offset_field, target)

        if offset == Translation2d():
            return APResult(0.0, 0.0, target.reference.rotation())

        # Convert current robot-relative speeds to field, then into target frame
        field_rel_speeds = Translation2d(robotRelativeSpeeds.vx, robotRelativeSpeeds.vy).rotateBy(current.rotation())
        initial = self._to_target_coordinate_frame(field_rel_speeds, target)

        disp = offset.norm()
        # Beeline logic (no entry-angle shaping when close or no entry angle provided)
        if target.entryAngle is None or disp < self._profile.beelineRadius:
            towards_target = offset / disp
            goal = towards_target * self._calculate_max_velocity(disp, target.velocity)
            out = self._correct(initial, goal)
            velo = self._to_global_coordinate_frame(out, target)
            rot = self._get_rotation_target(current.rotation(), target, disp)
            return APResult(velo.X(), velo.Y(), rot)

        # Swirly approach using entry angle
        goal = self._calculate_swirly_velocity(offset, target)
        out = self._correct(initial, goal)
        velo = self._to_global_coordinate_frame(out, target)
        rot = self._get_rotation_target(current.rotation(), target, disp)
        return APResult(velo.X(), velo.Y(), rot)

    def at_target(self, current: Pose2d, target: APTarget) -> bool:
        goal = target.reference
        ok_xy = hypot(current.X() - goal.X(), current.Y() - goal.Y()) <= self._profile.errorXY
        ok_theta = abs((current.rotation() - goal.rotation()).radians()) <= self._profile.errorTheta
        return ok_xy and ok_theta

    # ---------------------------- Internals ----------------------------------

    def _get_rotation_target(self, current: Rotation2d, target: APTarget, dist: float) -> Rotation2d:
        if target.rotationRadius is None:
            return target.reference.rotation()
        radius = target.rotationRadius
        if radius > dist:
            return target.reference.rotation()
        else:
            return current

    def _to_target_coordinate_frame(self, coords: Translation2d, target: APTarget) -> Translation2d:
        entry = target.entryAngle or Rotation2d()
        return coords.rotateBy(-entry)

    def _to_global_coordinate_frame(self, coords: Translation2d, target: APTarget) -> Translation2d:
        entry = target.entryAngle or Rotation2d()
        return coords.rotateBy(entry)

    def _calculate_max_velocity(self, dist: float, endVelo: float) -> float:
        # Matches: ( (4.5 * dist^2) * jerk )^(1/3) + endVelo
        return ((4.5 * (dist ** 2.0)) * self._profile.constraints.jerk) ** (1.0 / 3.0) + endVelo

    def _correct(self, initial: Translation2d, goal: Translation2d) -> Translation2d:
        # Rotate frame so goal lies on +X (I) axis
        angle_offset = Rotation2d()
        if goal != Translation2d():
            angle_offset = Rotation2d(goal.X(), goal.Y())
        adjusted_goal = goal.rotateBy(-angle_offset)
        adjusted_initial = initial.rotateBy(-angle_offset)
        initial_i = adjusted_initial.X()
        goal_i = adjusted_goal.X()

        # Cap goal along I since we'd rather adjust now than overshoot
        goal_i = min(goal_i, self._profile.constraints.velocity)

        # Adjust I component with acceleration-limited push
        adjusted_i = min(goal_i, self._push(initial_i, goal_i, self._profile.constraints.acceleration))

        # Return back to original frame (no lateral Y component in this simple corrector)
        return Translation2d(adjusted_i, 0.0).rotateBy(angle_offset)

    def _push(self, start: float, end: float, accel: float) -> float:
        max_change = accel * self._dt
        if abs(start - end) < max_change:
            return end
        if start > end:
            return start - max_change
        return start + max_change

    def _calculate_swirly_velocity(self, offset: Translation2d, target: APTarget) -> Translation2d:
        disp = offset.norm()
        theta = Rotation2d(offset.X(), offset.Y())
        rads = theta.radians()
        dist = self._calculate_swirly_length(rads, disp)

        # Tangent field of spiral-like approach:
        vx = theta.cos() - rads * theta.sin()
        vy = rads * theta.cos() + theta.sin()
        out = Translation2d(vx, vy)
        # normalize and scale to path length-derived velocity
        mag = hypot(out.X(), out.Y())
        if mag == 0:
            return Translation2d()
        scale = self._calculate_max_velocity(dist, target.velocity) / mag
        return out * scale

    def _calculate_swirly_length(self, theta: float, radius: float) -> float:
        if theta == 0:
            return radius
        theta = abs(theta)
        hypot_term = hypot(theta, 1.0)
        u1 = radius * hypot_term
        u2 = radius * (log(theta + hypot_term) / theta)
        return 0.5 * (u1 + u2)


def _sample():
    constraints = APConstraints(acceleration=5.0, jerk=2.0)
    profile = APProfile(
        constraints=constraints,
        errorXY=units.centimeters(2),
        errorTheta=units.degrees(0.5),
        beelineRadius=units.centimeters(8))
    autopilot = Autopilot(profile)
    target = APTarget(Pose2d(x=units.meters(50), y=units.meters(50), rot=units.degrees(90)))
    current_speeds = ChassisSpeeds()
    current_pose = Pose2d()
    result = autopilot.calculate(current_pose, current_speeds, target)
    
    # This would be passed to drive()
    output_speeds = ChassisSpeeds(vx=result.vx, vy=result.vy, omega=result.targetAngle.radians())