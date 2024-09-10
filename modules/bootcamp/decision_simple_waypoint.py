"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...

        status = report.status
        rel_x = self.waypoint.location_x - report.position.location_x
        rel_y = self.waypoint.location_y - report.position.location_y

        # Logic: If drone is not in range, keep moving towards the waypoint
        if self.in_range(report):
            if status == drone_status.DroneStatus.HALTED:
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_halt_command()
        else:
            command = commands.Command.create_set_relative_destination_command(rel_x, rel_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def in_range(self, report: drone_report.DroneReport) -> bool:
        """
        Returns bool which denotes whether the waypoint location is in range (by self.acceptance radius)
        of the drones current location
        """
        rel_x = self.waypoint.location_x - report.position.location_x
        rel_y = self.waypoint.location_y - report.position.location_y
        distance_squared = (rel_x * rel_x) + (rel_y * rel_y)
        return distance_squared <= (self.acceptance_radius) * (self.acceptance_radius)
