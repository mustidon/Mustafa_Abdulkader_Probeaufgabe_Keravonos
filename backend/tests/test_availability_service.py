from datetime import time

from app.services.availability_service import time_ranges_overlap


def test_overlapping_time_ranges_are_detected():
    existing_start = time(9, 0)
    existing_end = time(10, 0)

    requested_start = time(9, 30)
    requested_end = time(10, 30)

    result = time_ranges_overlap(
        requested_start=requested_start,
        requested_end=requested_end,
        existing_start=existing_start,
        existing_end=existing_end
    )

    assert result is True


def test_time_ranges_touching_at_the_border_do_not_overlap():
    existing_start = time(9, 0)
    existing_end = time(10, 0)

    requested_start = time(10, 0)
    requested_end = time(11, 0)

    result = time_ranges_overlap(
        requested_start=requested_start,
        requested_end=requested_end,
        existing_start=existing_start,
        existing_end=existing_end
    )

    assert result is False


def test_separate_time_ranges_do_not_overlap():
    existing_start = time(9, 0)
    existing_end = time(10, 0)

    requested_start = time(11, 0)
    requested_end = time(12, 0)

    result = time_ranges_overlap(
        requested_start=requested_start,
        requested_end=requested_end,
        existing_start=existing_start,
        existing_end=existing_end
    )

    assert result is False


def test_requested_time_range_inside_existing_range_overlaps():
    existing_start = time(9, 0)
    existing_end = time(12, 0)

    requested_start = time(10, 0)
    requested_end = time(11, 0)

    result = time_ranges_overlap(
        requested_start=requested_start,
        requested_end=requested_end,
        existing_start=existing_start,
        existing_end=existing_end
    )

    assert result is True