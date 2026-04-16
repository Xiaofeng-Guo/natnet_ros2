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
# Author: Aarsh Thakker <aarsh.thakker@centralesupelec.fr>

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    marker_poses_server = Node(
        package="natnet_ros2",
        executable="marker_poses_server",
    )

    helper_node = Node(
        package="natnet_ros2",
        executable="helper_node_r2.py"
    )

    ld.add_action(marker_poses_server)
    ld.add_action(helper_node)

    return ld