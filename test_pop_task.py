from unittest import mock
import pytest

from pop_task import Bubble, Rock, WorldGrid


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
def rock_and_bubbles(
    burst_bubble,
    floating_bubble,
    another_floating_bubble,
    a_third_floating_bubble,
    a_fourth_floating_bubble,
    good_old_rock_nothing_beats_that,
):
    return [
        burst_bubble,
        floating_bubble,
        another_floating_bubble,
        a_third_floating_bubble,
        a_fourth_floating_bubble,
        good_old_rock_nothing_beats_that,
    ]


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
        assert burst_bubble.col == "blue"

    def test_update_just_burst_bubble(self, floating_bubble):
        floating_bubble.burst()
        assert floating_bubble.state == "burst"
        assert floating_bubble.col == "red"
        floating_bubble.update_state()
        assert floating_bubble.state == "burst"
        assert floating_bubble.col == "blue"

    # TODO: test and code to ensure bubble doesn't move off plot or bursts at edge
    @pytest.mark.parametrize(
        "choice_return_value, new_position",
        [
            ("left", (1, 3)),
            ("right", (3, 3)),
            ("up", (2, 4)),
            ("down", (2, 2)),
            ("stay", (2, 3)),
        ],
    )
    @mock.patch("numpy.random.choice")
    def test_move_one_point_in_random_direction(
        self, mocked_choice, floating_bubble, choice_return_value, new_position
    ):
        mocked_choice.return_value = choice_return_value
        floating_bubble.move_one_point_in_random_direction()
        assert floating_bubble.position() == new_position


class TestWorldGrid:
    # TODO: refactoring into multiple single/double assertion tests for each function

    def test_burst_bubbles(
        self,
        world_grid,
        floating_bubble,
        another_floating_bubble,
        a_third_floating_bubble,
        a_fourth_floating_bubble,
        burst_bubble,
        good_old_rock_nothing_beats_that,
    ):
        world_grid.burst_bubbles()
        assert floating_bubble.state == "floating"
        assert floating_bubble.col == "green"
        assert burst_bubble.state == "burst"
        assert burst_bubble.col == "blue"
        for bubble in [
            another_floating_bubble,
            a_third_floating_bubble,
            a_fourth_floating_bubble,
        ]:
            assert bubble.state == "burst"
            assert bubble.col == "red"
        assert good_old_rock_nothing_beats_that.col == "orange"

    @mock.patch("pop_task.Bubble.move_one_point_in_random_direction")
    def test_update_state(
        self,
        mocked_bubble_move,
        world_grid,
        floating_bubble,
        another_floating_bubble,
        a_third_floating_bubble,
        a_fourth_floating_bubble,
        burst_bubble,
        good_old_rock_nothing_beats_that,
    ):
        world_grid.update_state()
        assert floating_bubble.state == "floating"
        assert floating_bubble.col == "green"
        assert burst_bubble.state == "burst"
        assert burst_bubble.col == "blue"
        for bubble in [
            another_floating_bubble,
            a_third_floating_bubble,
            a_fourth_floating_bubble,
        ]:
            assert bubble.state == "burst"
            assert bubble.col == "red"
        assert good_old_rock_nothing_beats_that.col == "orange"
