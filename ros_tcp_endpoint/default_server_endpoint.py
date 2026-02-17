#!/usr/bin/env python

import rclpy

from ros_tcp_endpoint import TcpServer
from .command_interface import UnityCommandInterface


def main(args=None):
    rclpy.init(args=args)
    tcp_server = TcpServer("UnityEndpoint")

    tcp_server.start()

    tcp_server.setup_executor()

    tcp_server.destroy_nodes()
    node = UnityCommandInterface()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
