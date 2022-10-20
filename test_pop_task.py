import pytest

from pop_task import Bubble, Rock, WorldGrid, WorldObject


@pytest.fixture
def floating_bubble():
    return Bubble(1, 2, 3)

@pytest.fixture
def another_floating_bubble():
    return Bubble(2, 3, 3)

@pytest.fixture
def a_third_floating_bubble():
    return Bubble(3, 3, 3)

@pytest.fixture
def a_fourth_floating_bubble():
    return Bubble(4, 4, 4)

@pytest.fixture
def burst_bubble():
    bubble = Bubble(5, 2, 3)
    bubble.col = "blue"
    bubble.state = "burst"
    return bubble

@pytest.fixture
def good_old_rock_nothing_beats_that():
    return Rock(1, 4, 4)

@pytest.fixture
def rock_and_bubbles(burst_bubble, floating_bubble, another_floating_bubble,
                     a_third_floating_bubble, a_fourth_floating_bubble,
                     good_old_rock_nothing_beats_that):
    return [burst_bubble, floating_bubble, another_floating_bubble,
                     a_third_floating_bubble, a_fourth_floating_bubble,
                     good_old_rock_nothing_beats_that]


@pytest.fixture
def world_grid(rock_and_bubbles):
    return WorldGrid(5, 5, rock_and_bubbles)



class TestBubbles:

    def test_burst_floating_bubble(self, floating_bubble):
        floating_bubble.burst()
        assert floating_bubble.state == "burst"
        assert floating_bubble.col == "red"

    def test_burst_burst_bubble(self, burst_bubble):
        burst_bubble.burst()
        assert burst_bubble.state == "burst"
        assert burst_bubble.col == 'blue'

    def test_update_just_burst_bubble(self, floating_bubble):
        floating_bubble.burst()
        assert floating_bubble.state == "burst"
        assert floating_bubble.col == "red"
        floating_bubble.update_state()
        assert floating_bubble.state == "burst"
        assert floating_bubble.col == "blue"


class TestWorldGrid:

    def test_burst_bubbles(self, world_grid, floating_bubble, another_floating_bubble,
                           a_third_floating_bubble, a_fourth_floating_bubble, burst_bubble, good_old_rock_nothing_beats_that):
        world_grid.burst_bubbles()
        assert floating_bubble.state == "floating"
        assert floating_bubble.col == "green"
        assert burst_bubble.state == "burst"
        assert burst_bubble.col == "blue"
        for bubble in [another_floating_bubble, a_third_floating_bubble, a_fourth_floating_bubble]:
            assert bubble.state == "burst"
            assert bubble.col == "red"
        assert good_old_rock_nothing_beats_that.col == 'yellow'

