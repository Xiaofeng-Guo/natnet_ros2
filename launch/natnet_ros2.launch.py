# Copyright 2024 Laboratoire des signaux et systèmes
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Original author: Aarsh Thakker <aarsh.thakker@centralesupelec.fr>
# Modified by: Xiaofan Guo
#
# natnet_ros2.launch.py - Command-line launch file for the NatNet ROS 2 node.
#
# This launch file creates a lifecycle node that connects to an OptiTrack
# Motive server via the NatNet SDK and publishes tracking data to ROS 2.
#
# Usage:
#   # Basic - publish rigid bodies (default):
#   ros2 launch natnet_ros2 natnet_ros2.launch.py serverIP:=192.168.123.40 clientIP:=192.168.123.90
#
#   # With individual marker tracking:
#   ros2 launch natnet_ros2 natnet_ros2.launch.py \
#     serverIP:=192.168.123.40 clientIP:=192.168.123.90 \
#     pub_individual_marker:=true conf_file:=initiate.yaml
#
#   # Unicast mode with frame logging:
#   ros2 launch natnet_ros2 natnet_ros2.launch.py \
#     serverIP:=192.168.123.40 clientIP:=192.168.123.90 \
#     serverType:=unicast log_frames:=true
#
# All boolean arguments accept: true/false, yes/no, 1/0 (case-insensitive).
# See generate_launch_description() at the bottom for the full argument list
# and their default values.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch.actions import OpaqueFunction
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import lifecycle_msgs.msg
from launch.actions import EmitEvent
from launch_ros.events.lifecycle import ChangeState
from launch.events.matchers import matches_action


def _str_to_bool(s):
    return s.strip().lower() in ('true', '1', 'yes')


def node_fn(context, *args, **kwargs):
    server_ip = LaunchConfiguration('serverIP').perform(context)
    client_ip = LaunchConfiguration('clientIP').perform(context)
    server_type = LaunchConfiguration('serverType').perform(context)
    multicast_address = LaunchConfiguration('multicastAddress').perform(context)
    server_command_port = int(LaunchConfiguration('serverCommandPort').perform(context))
    server_data_port = int(LaunchConfiguration('serverDataPort').perform(context))
    global_frame = LaunchConfiguration('global_frame').perform(context)
    remove_latency = _str_to_bool(LaunchConfiguration('remove_latency').perform(context))
    pub_rigid_body = _str_to_bool(LaunchConfiguration('pub_rigid_body').perform(context))
    pub_rigid_body_marker = _str_to_bool(LaunchConfiguration('pub_rigid_body_marker').perform(context))
    pub_individual_marker = _str_to_bool(LaunchConfiguration('pub_individual_marker').perform(context))
    pub_pointcloud = _str_to_bool(LaunchConfiguration('pub_pointcloud').perform(context))
    log_internals = _str_to_bool(LaunchConfiguration('log_internals').perform(context))
    log_frames = _str_to_bool(LaunchConfiguration('log_frames').perform(context))
    log_latencies = _str_to_bool(LaunchConfiguration('log_latencies').perform(context))
    conf_file = LaunchConfiguration('conf_file').perform(context)
    node_name = LaunchConfiguration('node_name').perform(context)
    activate = _str_to_bool(LaunchConfiguration('activate').perform(context))
    immt = LaunchConfiguration('immt').perform(context)

    params = [
        {
            "serverIP": server_ip,
            "clientIP": client_ip,
            "serverType": server_type,
            "multicastAddress": multicast_address,
            "serverCommandPort": server_command_port,
            "serverDataPort": server_data_port,
            "global_frame": global_frame,
            "remove_latency": remove_latency,
            "pub_rigid_body": pub_rigid_body,
            "pub_rigid_body_marker": pub_rigid_body_marker,
            "pub_individual_marker": pub_individual_marker,
            "pub_pointcloud": pub_pointcloud,
            "log_internals": log_internals,
            "log_frames": log_frames,
            "log_latencies": log_latencies,
            "individual_marker_msg_type": immt,
        }
    ]

    if pub_individual_marker:
        if len(conf_file) == 0 or not conf_file.endswith(".yaml"):
            raise RuntimeError("Provide yaml file for initial configuration")
        conf_file_path = os.path.join(
            get_package_share_directory('natnet_ros2'), 'config', conf_file)
        params.append(conf_file_path)

    ld = []
    node = LifecycleNode(
        package="natnet_ros2",
        executable="natnet_ros2_node",
        output="screen",
        name=node_name,
        namespace='',
        parameters=params,
    )
    ld.append(node)

    driver_configure = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(node),
            transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE,
        )
    )
    ld.append(driver_configure)

    if activate:
        driver_activate = EmitEvent(
            event=ChangeState(
                lifecycle_node_matcher=matches_action(node),
                transition_id=lifecycle_msgs.msg.Transition.TRANSITION_ACTIVATE,
            )
        )
        ld.append(driver_activate)

    return ld


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('serverIP', default_value="192.168.0.100"),
        DeclareLaunchArgument('clientIP', default_value="192.168.0.103"),
        DeclareLaunchArgument('serverType', default_value="multicast"),
        DeclareLaunchArgument('multicastAddress', default_value="239.255.42.99"),
        DeclareLaunchArgument('serverCommandPort', default_value="1510"),
        DeclareLaunchArgument('serverDataPort', default_value="1511"),
        DeclareLaunchArgument('global_frame', default_value="world"),
        DeclareLaunchArgument('remove_latency', default_value="false"),
        DeclareLaunchArgument('pub_rigid_body', default_value="true"),
        DeclareLaunchArgument('pub_rigid_body_marker', default_value="false"),
        DeclareLaunchArgument('pub_individual_marker', default_value="false"),
        DeclareLaunchArgument('pub_pointcloud', default_value="false"),
        DeclareLaunchArgument('log_internals', default_value="false"),
        DeclareLaunchArgument('log_frames', default_value="false"),
        DeclareLaunchArgument('log_latencies', default_value="false"),
        DeclareLaunchArgument('conf_file', default_value="initiate.yaml"),
        DeclareLaunchArgument('node_name', default_value="natnet_ros2"),
        DeclareLaunchArgument('activate', default_value="true"),
        DeclareLaunchArgument('immt', default_value="PoseStamped",
                              description="individual marker msg type: PoseStamped or PointStamped"),
        OpaqueFunction(function=node_fn)
    ])
