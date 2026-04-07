#!/usr/bin/env python3
import argparse
import time

import rclpy
from sensor_msgs.msg import JointState

START_Z = [0, 0.54, 0, -0.95, 0, 0, 0]
MIDDLE_Z = [0, 0.14, 0, -1.43, 0, 0, 0]
END_Z   = [0, -0.35, 0, -1.92, 0, 0, 0]

START_X = [0.16, -0.11, 0, -1.7, 0,0,0]
MIDDLE_X = [-0.18, -0.12, 0, -1.73, 0,0,0]
END_X = [-0.4, -0.02, 0, -1.63, 0,0,0]

START_Y = [0, -0.24, 0, -1.44, 0,0,0]
MIDDLE_Y = [0, -0.33, 0, -1.78, 0,0,0]
END_Y = [0, -0.29, 0, -2.07, 0,0,0]

DURATION = 4
RATE_HZ  = 50

JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7']

def lerp(a, b, t):
    return [a[i] + (b[i] - a[i]) * t for i in range(len(a))]


def get_trajectory(name):
    if name == 'X':
        if START_X is None or MIDDLE_X is None or END_X is None:
            raise ValueError('Trajectory X is not configured yet.')
        return [START_X, MIDDLE_X, END_X]
    if name == 'Y':
        if START_Y is None or MIDDLE_Y is None or END_Y is None:
            raise ValueError('Trajectory Y is not configured yet.')
        return [START_Y, MIDDLE_Y, END_Y]
    return [START_Z, MIDDLE_Z, END_Z]


def parse_args():
    parser = argparse.ArgumentParser(description='Publish joint trajectories for testing.')
    parser.add_argument(
        '--trajectory',
        default='Z',
        type=str.upper,
        choices=['X', 'Y', 'Z'],
        help='Trajectory to run: X, Y, or Z.',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    start_pose, middle_pose, end_pose = get_trajectory(args.trajectory)

    rclpy.init()
    node = rclpy.create_node('lerp_joint_publisher')
    pub = node.create_publisher(JointState, '/joint_states', 10)

    time.sleep(0.5)
    start = time.time()
    dt = 1.0 / RATE_HZ

    try:
        while True:
            phase = ((time.time() - start) / DURATION) % 2.0
            t = phase if phase <= 1.0 else 2.0 - phase
            if t <= 0.5:
                position = lerp(start_pose, middle_pose, t * 2.0)
            else:
                position = lerp(middle_pose, end_pose, (t - 0.5) * 2.0)

            msg = JointState()
            msg.header.stamp = node.get_clock().now().to_msg()
            msg.name = JOINT_NAMES
            msg.position = position
            pub.publish(msg)

            time.sleep(dt)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()