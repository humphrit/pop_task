import pytest

from pop_task import Bubble, Rock, WorldGrid, WorldObject


@pytest.fixture
def floating_bubble():
    return Bubble(1, 2, 3)

@pytest.fixture
def burst_bubble():
    bubble = Bubble(2, 3, 3)
    bubble.col = "blue"
    bubble.state = "burst"


class TestBubbles:

    def test_burst_bubble(self, floating_bubble):
        floating_bubble.burst()
        assert floating_bubble.state == "burst"
        assert floating_bubble.col == "red"
