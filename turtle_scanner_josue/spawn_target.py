#!/usr/bin/env python3

import random

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn


class SpawnTargetNode(Node):
    def __init__(self):
        # Partie 1 - Question 1 :
        # Creation du noeud Python spawn_target.py dans le package turtle_scanner_josue.
        super().__init__("spawn_target_node")

        # Partie 1 - Question 2 :
        # Utilisation du service ROS 2 /spawn de type turtlesim/srv/Spawn.
        self.client = self.create_client(Spawn, "/spawn")

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for /spawn service...")

        # Partie 1 - Question 2 :
        # Generation de coordonnees aleatoires dans l'espace TurtleSim
        # avec x et y dans l'intervalle [1, 10].
        self.target_x = random.uniform(1.0, 10.0)
        self.target_y = random.uniform(1.0, 10.0)

        request = Spawn.Request()
        request.x = self.target_x
        request.y = self.target_y
        request.theta = 0.0
        # Partie 1 - Question 2 :
        # Le nom demande pour la tortue cible est turtle_target.
        request.name = "turtle_target"

        # un client de service ROS 2 utilise call_async(request) puis attend le resultat.
        self.future = self.client.call_async(request)
        self.future.add_done_callback(self.spawn_response_callback)

    def spawn_response_callback(self, future):
        try:
            response = future.result()
            # Partie 1 - Question 3 :
            # Affichage des coordonnees de la cible apres un spawn reussi.
            self.get_logger().info(
                f"Target '{response.name}' spawned at "
                f"x={self.target_x:.2f}, y={self.target_y:.2f}"
            )
        except Exception as error:
            self.get_logger().error(f"Spawn failed: {error}")
        finally:
            self.destroy_node()
            rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = SpawnTargetNode()
    rclpy.spin(node)


if __name__ == "__main__":
    main()
