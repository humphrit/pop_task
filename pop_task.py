import os
import time
import copy
import plotly
import numpy as np
import pandas as pd

import plotly.express as px

from enum import Enum
from typing import List, Tuple
from plotly import graph_objects as go


class WorldObject():
    col = None

    def __init__(self, obj_id, initx, inity):
        self.obj_id = obj_id
        self.posx = initx
        self.posy = inity

    def move(self, step_x, step_y):
        self.posx += step_x
        self.posy += step_y

    def update_state(self):
        raise NotImplementedError()

    def position(self):
        return self.posx, self.posy


class Bubble(WorldObject):
    col = "green"
    state = "floating"

    def __init__(self, obj_id, initx, inity):
        super().__init__(obj_id, initx, inity)

    def move_one_point_in_random_direction(self):
        direction = np.random.choice(["left", "right", "up", "down", "stay"])
        if direction == "left":
            self.move(-1, 0)
        elif direction == "right":
            self.move(1, 0)
        elif direction == "up":
            self.move(0, 1)
        elif direction == "down":
            self.move(0, -1)

    def update_state(self):
        if self.state == "floating":
            self.move_one_point_in_random_direction()
        else:
            self.col = "blue"

    def draw(self):
        return go.Scatter(x=[self.posx], y=[self.posy], mode="markers", marker={"color": self.col})

    def burst(self):
        if self.state == "floating":
            self.state = "burst"
            self.col = "red"


class Rock(WorldObject):
    col = "yellow"

    def move(self):
        pass

    def update_state(self):
        pass

    def draw(self):
        return go.Scatter(x=[self.posx], y=[self.posy], mode="markers", marker={"color": self.col})


class WorldGrid():
    def __init__(self, width: int, height: int, w_objects: List[WorldObject]):
        self.width = width
        self.height = height
        self.w_objects = w_objects
        self.rock_positions = [x.position() for x in self.w_objects if isinstance(x, Rock)]

    def update_state(self):
        for w_object in self.w_objects:
            w_object.update_state()


    def burst_bubbles(self):
        positions = self.object_positions()
        seen = set()
        duplicate_positions = [x for x in positions if x in seen or seen.add(x)]
        for w_object in self.w_objects:
            if w_object.position() in duplicate_positions and isinstance(w_object, Bubble):
                w_object.burst()

    def get_frame(self, frame_number: int):
        draw_objects = []
        for w_object in self.w_objects:
            draw_objects.append(w_object.draw())
        return go.Frame(data=draw_objects,
                        layout=go.Layout(title_text=f"Simulation frame {frame_number}"))

    def create_simulation(self, steps: int):
        frames = []
        for i in range(steps):
            self.update_state()
            frames.append(self.get_frame(i))

        fig = go.Figure(data=[w_obj.draw() for w_obj in self.w_objects],
            layout=go.Layout(xaxis=dict(range=[0, self.width], autorange=False),
                yaxis=dict(range=[0, self.height], autorange=False), title="Simulation",
                updatemenus=[dict(type="buttons",
                    buttons=[dict(label="Play", method="animate", args=[None])])]), frames=frames)
        fig.show()

    def object_positions(self):
        return [x.position() for x in self.w_objects if isinstance(x, Bubble) and x.state ==
                "floating"] + self.rock_positions



def simulate():
    bubbles = [Bubble(f"bubble_{i}_{j}", i, j) for i in range(5, 15, 2) for j in range(5, 15, 2)]
    rocks = [Rock("rock_2_2", 2, 2), Rock("rock_18_18", 18, 18), Rock("rock_3_15", 3, 15),

    ]
    world = WorldGrid(20, 20, bubbles + rocks)
    world.create_simulation(steps=50)

if __name__ == '__main__':

    simulate()

