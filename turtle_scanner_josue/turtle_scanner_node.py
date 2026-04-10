#!/usr/bin/env python3

import math

from geometry_msgs.msg import Twist
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
        self.pose_scanner_received = False
        self.pose_target_received = False

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

        # Partie 3 - Question 1 :
        # Publisher de commande en vitesse pour deplacer turtle1.
        self.cmd_vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        # Partie 3 - Question 1 :
        # Parametres du balayage en serpentin.
        self.nb_lignes = 5
        self.y_start = 1.0
        self.y_step = 2.0
        self.x_min = 1.0
        self.x_max = 10.0
        self.waypoint_tolerance = 0.3
        self.linear_speed_max = 2.0

        self.declare_parameter("Kp_ang", 6.0)
        self.declare_parameter("Kp_lin", 1.2)
        self.Kp_ang = self.get_parameter("Kp_ang").value
        self.Kp_lin = self.get_parameter("Kp_lin").value

        # Partie 3 - Question 1 :
        # Generation programmatique des waypoints du serpentin.
        self.waypoints = self.generate_serpentine_waypoints()
        self.current_waypoint_index = 0
        self.scan_completed = False

        # Partie 3 - Question 4 :
        # Timer ROS 2 appele regulierement pour executer une etape du balayage.
        self.create_timer(0.05, self.scan_step)


        self.get_logger().info("Turtle scanner node started")

    def pose_scanner_callback(self, msg):
        # Partie 2 - Question 2 :
        # Mise a jour de l'attribut self.pose_scanner a chaque message recu.
        self.pose_scanner = msg
        self.pose_scanner_received = True

    def pose_target_callback(self, msg):
        # Partie 2 - Question 3 :
        # Mise a jour de l'attribut self.pose_target a chaque message recu.
        self.pose_target = msg
        self.pose_target_received = True

    def generate_serpentine_waypoints(self):
        waypoints = []

        for index in range(self.nb_lignes):
            y_value = self.y_start + index * self.y_step

            # Partie 3 - Question 1 :
            # Les lignes paires vont vers x_max et les lignes impaires vers x_min.
            if index % 2 == 0:
                waypoints.append((self.x_max, y_value))
            else:
                waypoints.append((self.x_min, y_value))

        return waypoints

    def compute_angle(self, point_a, point_b):
        # Partie 3 - Question 2 :
        # theta_desired = atan2(yB - yA, xB - xA)
        return math.atan2(point_b[1] - point_a[1], point_b[0] - point_a[0])

    def compute_distance(self, point_a, point_b):
        # Partie 3 - Question 3 :
        # Distance euclidienne entre A et B.
        return math.sqrt(
            (point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2
        )

    def publish_stop_command(self):
        self.cmd_vel_publisher.publish(Twist())

    def scan_step(self):
        # On attend d'abord la pose de la tortue scanner.
        if not self.pose_scanner_received:
            return

        # Partie 3 - Question 5 :
        # Lorsque tous les waypoints sont parcourus, on arrete la tortue.
        if self.scan_completed:
            self.publish_stop_command()
            return

        if self.current_waypoint_index >= len(self.waypoints):
            self.scan_completed = True
            self.publish_stop_command()
            self.get_logger().info("Balayage termine")
            return

        current_position = (self.pose_scanner.x, self.pose_scanner.y)
        current_waypoint = self.waypoints[self.current_waypoint_index]

        # Partie 3 - Question 4.a :
        # Calcul de la distance au waypoint courant.
        distance = self.compute_distance(current_position, current_waypoint)

        # Partie 3 - Question 4.b :
        # Si la distance est inferieure au seuil, on passe au waypoint suivant.
        if distance < self.waypoint_tolerance:
            self.current_waypoint_index += 1

            if self.current_waypoint_index >= len(self.waypoints):
                self.scan_completed = True
                self.publish_stop_command()
                self.get_logger().info("Balayage termine")

            return

        desired_theta = self.compute_angle(current_position, current_waypoint)

        # Partie 3 - Question 4.c :
        # e = atan( tan( (theta_desired - theta) / 2 ) )
        heading_error = math.atan(
            math.tan((desired_theta - self.pose_scanner.theta) / 2.0)
        )

        command = Twist()
        command.angular.z = self.Kp_ang * heading_error
        command.linear.x = min(self.Kp_lin * distance, self.linear_speed_max)

        # Partie 3 - Question 4.d :
        # Publication de la commande sur /turtle1/cmd_vel.
        self.cmd_vel_publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleScannerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
