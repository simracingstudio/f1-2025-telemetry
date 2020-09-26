"""
Test speedtrap event packets
"""
from f1_2020_telemetry.packets import unpack_udp_packet


def is_speedtrap(event_packet):
    """Returns true if packet is a speedtrap event packet"""

    return (
        event_packet.header.packetId == 3
        and event_packet.eventStringCode.decode() == "SPTP"
    )


def verify_speedtrap_members(
    speedtrap_details,
    speed: int,
    vehicle: int,
):
    """Returns true if fields of speedtrap data match expected values"""

    assert speedtrap_details.speed == speed
    assert speedtrap_details.vehicleIdx == vehicle


def test_packet_event_speedtrap():
    """Tests speedtrap event packet"""

    packet = unpack_udp_packet(
        b"\xe4\x07\x01\t\x01\x03J\x15Dl\n\xb5\xa77\xc8\x9e\x83C\x1b,\x00\x00\xff\xffSPTP\x038Y\xa6C\x00\x00"
    )

    assert is_speedtrap(packet)

    verify_speedtrap_members(
        speedtrap_details=packet.eventDetails.speedTrap,
        speed=332.697021484375,
        vehicle=3,
    )
