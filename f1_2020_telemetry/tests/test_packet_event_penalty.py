"""
Test event packet features related to penalties
"""
from f1_2020_telemetry.packets import unpack_udp_packet


def is_penalty(event_packet):
    """Returns true if packet is a penalty event packet"""

    return (
        event_packet.header.packetId == 3
        and event_packet.eventStringCode.decode() == "PENA"
    )


def verify_penalty_members(
    penalty_details,
    infringement: int,
    lap: int,
    penalty: int,
    places: int,
    other_vehicle: int,
    vehicle: int,
    time: int,
):
    """Returns true if fields of penalty data match expected values"""

    assert penalty_details.infringementType == infringement
    assert penalty_details.lapNum == lap
    assert penalty_details.penaltyType == penalty
    assert penalty_details.placesGained == places
    assert penalty_details.otherVehicleIdx == other_vehicle
    assert penalty_details.vehicleIdx == vehicle
    assert penalty_details.time == time


def test_packet_event_penalty():
    """Tests penalty event packet"""

    # Penalty 5, Infringement 27, lapNum 2, otherVehicleId = 255, placesGained = 0, time = 255, vehicleIdx = 14
    packet = unpack_udp_packet(
        b"\xe4\x07\x01\x08\x01\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PENA\x05\x1b\x0e\xff\xff\x02\x00"
    )

    assert is_penalty(packet)

    verify_penalty_members(
        penalty_details=packet.eventDetails.penalty,
        infringement=27,
        lap=2,
        penalty=5,
        places=0,
        other_vehicle=255,
        vehicle=14,
        time=255,
    )


def test_packet_event_penalty_alt():
    """Tests an alternative penalty event packet"""

    # Penalty 5, Infringement 7, lapNum 5, otherVehicleId = 255, placesGained = 0, time = 255, vehicleIdx = 4
    packet = unpack_udp_packet(
        b"\xe4\x07\x01\t\x01\x03\xa3\x80\x9atC\xc0\x8e}:\x11\tD\xab\\\x00\x00\xff\xffPENA\x05\x07\x04\xff\xff\x05\x00"
    )

    assert is_penalty(packet)

    verify_penalty_members(
        penalty_details=packet.eventDetails.penalty,
        infringement=7,
        lap=5,
        penalty=5,
        places=0,
        other_vehicle=255,
        vehicle=4,
        time=255,
    )
