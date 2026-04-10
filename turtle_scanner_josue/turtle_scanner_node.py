#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


class TurtleScannerNode(Node):
    def __init__(self):
        # Partie 2 - Question 1 :
        # Creation du noeud Python turtle_scanner_node.py dans le package.
        super().__init__("turtle_scanner_node")

        # Partie 2 - Questions 2 et 3 :
        # Attributs qui stockent en permanence la pose de la tortue scanner et la pose de la tortue cible.
        self.pose_scanner = Pose()
        self.pose_target = Pose()

        # Partie 2 - Question 2 :
        # Souscription au topic /turtle1/pose de type turtlesim/msg/Pose.
        self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.pose_scanner_callback,
            10,
        )

        # Partie 2 - Question 3 :
        # Souscription au topic /turtle_target/pose de type turtlesim/msg/Pose.
        self.create_subscription(
            Pose,
            "/turtle_target/pose",
            self.pose_target_callback,
            10,
        )

        self.get_logger().info("Turtle scanner node started")

    def pose_scanner_callback(self, msg):
        # Partie 2 - Question 2 :
        # Mise a jour de l'attribut self.pose_scanner a chaque message recu.
        self.pose_scanner = msg

    def pose_target_callback(self, msg):
        # Partie 2 - Question 3 :
        # Mise a jour de l'attribut self.pose_target a chaque message recu.
        self.pose_target = msg


def main(args=None):
    rclpy.init(args=args)
    node = TurtleScannerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
