#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading

class UnityCommandInterface(Node):
    def __init__(self):
        super().__init__('unity_command_interface')

        # Publisher and subscriber
        self.command_publisher = self.create_publisher(
            String, 
            '/unity_cmd',
            10
        )
        self.subscription = self.create_subscription(
            String, 
            '/unity_feedback',
            self.feedback_callback,
            10
        )

        self.get_logger().info("Unity Text Interface started.")
        self.get_logger().info("Type a command and press Enter to send to Unity.")
        self.get_logger().info("Type 'exit' or 'quit' to stop.")

        # Run input loop in a background thread
        threading.Thread(target=self.input_loop, daemon=True).start()

    def feedback_callback(self, msg):
        """Print feedback coming from Unity."""
        self.get_logger().info(f"[Unity]: {msg.data}")

    def input_loop(self):
        """Read console input and publish it."""
        while rclpy.ok():
            try:
                text = input("> ").strip()
                if not text:
                    continue

                msg = String()
                msg.data = text
                self.command_publisher.publish(msg)
                self.get_logger().info(f"Sent: {text}")
                if text.lower() in ["exit", "quit", "close"]:
                    self.get_logger().info("Exiting...")
                    rclpy.try_shutdown()
                    break

            except EOFError:
                rclpy.try_shutdown()
                break

def main(args=None):
    rclpy.init(args=args)
    node = UnityCommandInterface()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        _try_shutdown()

if __name__ == "__main__":
    main()
