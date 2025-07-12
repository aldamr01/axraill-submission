from app.config import Config
from app.models.ckstop import CKStop
from pydantic import ValidationError
import json


class CKStopCommand:
    COMMAND: str = "ckstop"
    
    def __init__(self):
        self.paths_found: list[list[str, int, int]] = []
        self.file_structure: CKStop

        with open(f"{Config.FILE_PATH}/{Config.FILE_NAME}", "r") as file:
            file_data = json.load(file)

        try:
            file_structure = CKStop(**file_data)
            self.file_structure = file_structure
        except ValidationError as invalidFormat:
            print(invalidFormat.errors())
            raise Exception("Invalid format of the file")

    def find(self) -> list[list[str, int, int]]:
        start = self.file_structure.start
        finish = self.file_structure.end
        paths = self.file_structure.paths

        start_paths = [path for path in paths if start in (path[0], path[1])]
        next_nodes = [
            [node[0], node[2]] if node[0] != start else [node[1], node[2]]
            for node in start_paths
        ]

        for next_node in next_nodes:
            dead_ends = []
            dead_ends.append(start)
            dead_ends.append(next_node[0])
            self.path_finder(
                next_node[0],
                finish,
                dead_ends,
                paths,
                f"{start} -> {next_node[0]}",
                next_node[1],
                1,
            )

        return self.paths_found

    def path_finder(
        self,
        current_node: int,
        end: int,
        dead_ends: list[int],
        paths: list[list[int]],
        tracer: str,
        distance: int,
        step: int,
    ) -> None:
        if current_node == end:
            self.paths_found.append([tracer, distance, step])
            return None

        available_paths = [path for path in paths if current_node in (path[0], path[1])]
        available_paths = [
            path
            for path in available_paths
            if (path[0] == current_node and path[1] not in dead_ends)
            or (path[1] == current_node and path[0] not in dead_ends)
        ]

        for path in available_paths:
            excluded_node = path[0] if path[0] != current_node else path[1]
            nd = dead_ends.copy()
            nd.append(excluded_node)
            self.path_finder(
                excluded_node,
                end,
                nd,
                paths,
                f"{tracer} -> {excluded_node}",
                distance + path[2],
                step + 1,
            )

        return None

    def find_shortest_path_with_distance(
        self, paths: list[list[str, int, int]]
    ) -> list[str, int, int]:
        return sorted(paths, key=lambda x: x[1])[0]

    def find_shortest_distance(
        self, paths: list[list[str, int, int]]
    ) -> list[str, int, int]:
        return sorted(paths, key=lambda x: x[2])[0]
    
    def find_shortest_path_with_max_steps(
        self, paths: list[list[str, int, int]]
    ) -> list[str, int, int]:
        max_steps = self.file_structure.max_steps
        return sorted(paths, key=lambda x: x[1])[0] if max_steps > 0 else None

    def start(self) -> None:
        paths = self.find()
        shortest_path = self.find_shortest_path_with_distance(paths)
        shortest_distance = self.find_shortest_distance(paths)
        shortest_path_with_max_steps = self.find_shortest_path_with_max_steps(paths)
     
        print(
            f"Shortest path: {shortest_path[0]} with {shortest_path[1]} value and {shortest_path[2]} steps"
        )
        print(
            f"Shortest distance: {shortest_distance[0]} with {shortest_distance[1]} value and {shortest_distance[2]} steps"
        )
        print(
            f"Shortest path with max steps: {shortest_path_with_max_steps[0]} with {shortest_path_with_max_steps[1]} value and {shortest_path_with_max_steps[2]} steps" if shortest_path_with_max_steps else "No path found with max steps"
        )
