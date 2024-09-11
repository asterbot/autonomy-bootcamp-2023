"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
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


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
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
        self.reached_waypoint = False  # True if drone has reached the designated waypoint
        self.final_landing_pad = location.Location(0, 0)  # placeholder
        self.found_landing_pad = False  # True if drone has found the landing pad to go to
        # (ie. no need for computing it again)

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
        def in_range(loc1: location.Location, loc2: location.Location) -> bool:
            """
            Returns bool which denotes whether loc1 is in the acceptance radius of loc2
            """
            rel_x = loc1.location_x - loc2.location_x
            rel_y = loc1.location_y - loc2.location_y
            distance_squared = (rel_x * rel_x) + (rel_y * rel_y)
            return distance_squared <= (self.acceptance_radius) * (self.acceptance_radius)

        def dist_squared(loc1: location.Location, loc2: location.Location) -> float:
            """
            Finds distance squared between the two locations
            """
            rel_x = loc1.location_x - loc2.location_x
            rel_y = loc1.location_y - loc2.location_y
            return (rel_x * rel_x) + (rel_y * rel_y)

        status = report.status
        if not self.reached_waypoint:
            rel_x = self.waypoint.location_x - report.position.location_x
            rel_y = self.waypoint.location_y - report.position.location_y
            if in_range(report.position, self.waypoint):
                if status == drone_status.DroneStatus.HALTED:
                    self.reached_waypoint = True
                else:
                    command = commands.Command.create_halt_command()
            else:
                command = commands.Command.create_set_relative_destination_command(rel_x, rel_y)
        else:
            if not self.found_landing_pad:
                # This is only so we don't have to do this computation over and over (which could be potentially expensive)
                self.final_landing_pad = landing_pad_locations[0]
                for landing_pad in landing_pad_locations:
                    if dist_squared(report.position, landing_pad) < dist_squared(
                        report.position, self.final_landing_pad
                    ):
                        # For positive quantities, (x^2 < y^2) implies (x < y) and distance is a positive quantity
                        self.final_landing_pad = landing_pad
                self.found_landing_pad = True
            else:
                rel_x = self.final_landing_pad.location_x - report.position.location_x
                rel_y = self.final_landing_pad.location_y - report.position.location_y
                if in_range(report.position, self.final_landing_pad):
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
