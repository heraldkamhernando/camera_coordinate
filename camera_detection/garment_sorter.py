"""Hardware-independent orchestration for a garment-sorting workflow.

This module defines the sequence of operations, not camera, vision, or robot
control drivers. Supply a hardware adapter that implements
:class:`GarmentSorterHardware` before running it with real equipment.
"""

from dataclasses import dataclass
from typing import Optional, Protocol, Tuple


Position = Tuple[float, ...]


class GarmentSorterHardware(Protocol):
    """Operations the sorter needs from vision and robot hardware adapters."""

    def garments_remaining(self) -> bool:
        """Return whether the system believes there are garments left to sort."""
        ...

    def detect_garment(self) -> Optional[object]:
        """Return a detected garment, or None when no garment is visible."""
        ...

    def search_for_garments(self) -> None:
        """Adjust the search view or position when no garment is detected."""
        ...

    def estimate_grasp_point(self, garment: object) -> Position:
        """Estimate a grasp target in the coordinate frame expected by the arm."""
        ...

    def move_arm(self, position: Position) -> None:
        """Move the arm to a validated grasp target."""
        ...

    def close_gripper(self) -> None:
        ...

    def verify_grasp(self) -> bool:
        """Return whether the garment is securely held."""
        ...

    def retry_grasp(self) -> None:
        """Perform a bounded recovery/retry action after a failed grasp check."""
        ...

    def lift_garment(self) -> None:
        ...

    def classify_garment_color(self) -> str:
        """Return DARK, LIGHT, or another value for uncertain classifications."""
        ...

    def move_to_dark_basin(self) -> None:
        ...

    def move_to_light_basin(self) -> None:
        ...

    def move_to_uncertain_handling_position(self) -> None:
        ...

    def open_gripper(self) -> None:
        ...


@dataclass(frozen=True)
class SorterResult:
    """Summary of one bounded sorter run."""

    cycles: int
    sorted_count: int
    status: str


def run_sorting_loop(
    hardware: GarmentSorterHardware,
    max_cycles: int = 100,
) -> SorterResult:
    """Run the garment-sorting workflow for at most ``max_cycles`` iterations.

    A cycle is one search/handling attempt. The limit prevents an unattended
    loop from running forever if garment detection or the remaining-items
    signal is faulty. Hardware-specific motion constraints, emergency-stop
    behavior, and safe retry logic must be implemented by the adapter.
    """
    if max_cycles <= 0:
        raise ValueError("max_cycles must be greater than zero")

    cycles = 0
    sorted_count = 0

    while hardware.garments_remaining() and cycles < max_cycles:
        cycles += 1

        garment = hardware.detect_garment()
        if garment is None:
            hardware.search_for_garments()
            continue

        grasp_position = hardware.estimate_grasp_point(garment)
        hardware.move_arm(grasp_position)
        hardware.close_gripper()

        if not hardware.verify_grasp():
            hardware.retry_grasp()
            continue

        hardware.lift_garment()
        color = hardware.classify_garment_color().strip().upper()

        if color == "DARK":
            hardware.move_to_dark_basin()
        elif color == "LIGHT":
            hardware.move_to_light_basin()
        else:
            hardware.move_to_uncertain_handling_position()

        hardware.open_gripper()
        sorted_count += 1

    status = "complete" if not hardware.garments_remaining() else "cycle_limit"
    return SorterResult(cycles=cycles, sorted_count=sorted_count, status=status)
