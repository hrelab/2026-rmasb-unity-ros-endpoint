FROM ros:humble-ros-base
ENV DEBIAN_FRONTEND=noninteractive

# Create workspace
RUN mkdir -p /home/dev_ws/src
WORKDIR /home/dev_ws

# Install tools
RUN apt-get update && apt-get install -y \
    git python3-colcon-common-extensions python3-pip nano && \
    rm -rf /var/lib/apt/lists/*

# Copy repository packages into workspace src
COPY . /home/dev_ws/src/

# Build the workspace
RUN bash -lc "source /opt/ros/humble/setup.bash && colcon build --event-handlers console_direct+"

# Create entrypoint script
COPY entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh

ENTRYPOINT ["/ros_entrypoint.sh"]

# Default command: run both endpoints
CMD ["bash", "-c", "ros2 run ros_tcp_endpoint default_server_endpoint & ros2 run ros_tcp_endpoint command_interface"]
