from queue import PriorityQueue
import json
import math
import os

def load_data(source_file):
    """Reading JSON from the file and deserializing it
    :param source_file: JSON map of tram stops (str)
    :return: obj (array)
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '..', source_file)) as file:
        return json.load(file)


class State:
    """ State lets you trace back the route from the last stop
    :attr stop: Code of the stop (str)
    :attr previous: Previous state of the route (State)
    """
    def __init__(self, stop, time, cost, previous=None):
        self.stop = stop
        self.time = time
        self.cost = cost
        self.previous = previous

    """ Returns route as a string from the last stop to the beginning. 
        Format: 1030423 -> 1010420 -> 1010427 
    """
    def __str__(self):
        result = self.stop
        state = self.previous
        while state is not None:
            result += " -> " + state.stop
            state = state.previous

        return result
    
    def __lt__(self, other):
        return (self.time + self.h) < (other.time + other.h)

    def heuristic(self, citymap, goal):
        stop1 = citymap.stops[self.stop]
        stop2 = citymap.stops[goal]
        dx = stop1["x"] - stop2["x"]
        dy = stop1["y"] - stop2["y"]
        distance = math.sqrt(dx*dx + dy*dy)
        return distance / 260

    def get_stop(self):
        return self.stop

    def get_previous(self):
        return self.previous


class CityMap:
    """Storage of the tram network stops
    :attr data: (obj)
    :attr stops: dictionary {stop_code: stop}
    """
    def __init__(self, source_file):
        self.data = load_data(source_file)
        self.stops = {}
        for stop in self.data:
            self.stops[stop["code"]] = stop

    def get_neighbors(self, stop_code):
        """Returns dictionary containing all neighbor stops """
        return self.stops.get(stop_code)["neighbors"]

    def get_neighbors_codes(self, stop_code):
        """Returns codes of all neighbor stops """
        return list(self.stops.get(stop_code)["neighbors"].keys())

    def travel_time(self, from_stop, to_stop, departure_time):
        travel = 1
        wait = (10 - (departure_time % 10)) % 10
        return travel + wait

    def search(self, start, goal, departure_time=0):
        """A* search. Return the answer as a linked list of States
        where the first node contains the goal stop code and each node is linked to the previous node in the path.
        The last node in the list is the starting stop and its previous node is None.

        :param start: Code of the initial stop (str)
        :param goal: Code of the last stop (str)
        :returns (obj)
        """

        pq = PriorityQueue()
        start_state = State(start, departure_time, 0, None)
        start_state.h = start_state.heuristic(self, goal)
        pq.put((start_state.cost + start_state.h, start_state))

        visited = {}

        while not pq.empty():
            _, current = pq.get()
            current_stop = current.stop

            if current_stop == goal:
                return current

            if current_stop in visited and visited[current_stop] <= current.cost:
                continue
            visited[current_stop] = current.cost

            for neighbor in self.get_neighbors(current_stop):
                transition_time = self.travel_time(current_stop, neighbor, current.time)
                new_time = current.time + transition_time
                new_cost = current.cost + transition_time

                new_state = State(neighbor, new_time, new_cost, current)
                new_state.h = new_state.heuristic(self, goal)
                pq.put((new_cost + new_state.h, new_state))

        return None
