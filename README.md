# NatNet 4 ROS 2 driver

## Acknowledgment

This package is adopted from and based on the [natnet_ros2](https://github.com/L2S-lab/natnet_ros2). The original work is licensed under the
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

Original repository: https://github.com/L2S-lab/natnet_ros2

Modifications in this fork include fixes to the command-line launch file
(`natnet_ros2.launch.py`) for correct parameter type handling, lifecycle
activation, and `libNatNet.so` installation.

## Introduction

This package contains a ROS 2 driver for the NatNet protocol used by the OptiTrack motion capture system. It supports NatNet versions 4.0 (Motive 2.2 and higher). The NatNet SDK provided by the optitrack can be found [here](https://optitrack.com/support/downloads/developer-tools.html#natnet-sdk). It will be downloaded under `deps/NatnetSDK` while building it for the first time. NatNet protocol is used for streaming live motion capture data (rigid bodies, skeletons etc) across the shared network.

This package is only tested with the Natnet 4.0 and ROS 2 (Foxy and Humble) but probably will work with the other versions of Motive and ROS 2 as well.

### Current Features:
  
 - Easy gui interface to control the node.
 - Rigid bodies are published as `geometry_msgs/PoseStamped` under name given in the Motive, i.e `/<body-name>/pose`. Plus those are also broadcasting as `tf` frame for rviz
 - Markers of the rigid bodies are published ad `geometry_msgs/PointStamped` unuder the name `/<body-name>/marker#/pose`
 - Unlabeled markers with the initial position and the name mentione in the `/config/initiate.yaml`are published as `geometry_msgs/PoseStamped` or `geometry_msgs/PointStamped` unuder the name `/<name-in-config-file>/pose`. Plus those are also broadcasting as `tf` frame for rviz. The marker position is updated based on Iterative closest point (nearest neighbour)
 - Unlabled markers can be also published as `sensor_msgs/PointCloud`
 - Different options for publishing and logging the data

### Work under progress: 

 - Include Skeleton and other devices in the system to make it package as whole.
 - Considering position and orientation for similar marker configurations (at least 3 markers)
 - Adding an option for the axis orientation (Z UP or Y UP)

## How to use it

#### Building the package
**requirements**
```
sudo apt install -y ros-$ROS_DISTRO-tf2* wget
```
Keep your system connected to the internet while building the package for the first time.
```
cd ~/ros2_ws/src
git clone https://github.com/L2S-lab/natnet_ros2
cd ..
colcon build --symlink-install
. install/setup.bash
```

#### Setup the Motive for this package
- Disable the firewall for the network on which the data is being published.
- Open the Motive app. 
- In the motive app, open the streaming panel.
- Disable the other streaming Engines like VRPN, Trackd etc.
- Under the OptiTrack Streaming Engine, turn on the Broadcast Frame.
- Select the correct IP address in the Local Interface.
- Select the Up Axis as Z.

Here is an example of how your streaming settings should look.

![alt text](https://github.com/L2S-lab/natnet_ros2/blob/main/img/streaming.png)


#### Option 1: Command-line launch (recommended)

Launch the node directly from the command line with all parameters specified as launch arguments.

**Basic usage (rigid body tracking):**
```bash
source install/setup.bash
ros2 launch natnet_ros2 natnet_ros2.launch.py serverIP:=<MOTIVE_PC_IP> clientIP:=<YOUR_PC_IP>
```

**Example:**
```bash
ros2 launch natnet_ros2 natnet_ros2.launch.py serverIP:=192.168.123.40 clientIP:=192.168.123.90
```

By default this publishes rigid bodies and activates the node immediately.

**With individual marker tracking:**
```bash
ros2 launch natnet_ros2 natnet_ros2.launch.py \
  serverIP:=192.168.123.40 \
  clientIP:=192.168.123.90 \
  pub_individual_marker:=true \
  conf_file:=initiate.yaml
```

**With unicast and custom ports:**
```bash
ros2 launch natnet_ros2 natnet_ros2.launch.py \
  serverIP:=192.168.123.40 \
  clientIP:=192.168.123.90 \
  serverType:=unicast \
  serverCommandPort:=1510 \
  serverDataPort:=1511
```

**Full list of launch arguments:**

| Argument | Default | Description |
|----------|---------|-------------|
| `serverIP` | `192.168.0.100` | IP address of the Motive host PC |
| `clientIP` | `192.168.0.103` | IP address of this PC |
| `serverType` | `multicast` | `multicast` or `unicast` |
| `multicastAddress` | `239.255.42.99` | Multicast group address (only used when serverType is multicast) |
| `serverCommandPort` | `1510` | NatNet command port |
| `serverDataPort` | `1511` | NatNet data port |
| `global_frame` | `world` | TF parent frame name |
| `remove_latency` | `false` | Subtract system latency from timestamps |
| `pub_rigid_body` | `true` | Publish rigid body poses |
| `pub_rigid_body_marker` | `false` | Publish markers of rigid bodies |
| `pub_individual_marker` | `false` | Publish unlabeled individual markers (requires conf_file) |
| `pub_pointcloud` | `false` | Publish all markers as a PointCloud |
| `log_internals` | `false` | Log internal NatNet details |
| `log_frames` | `false` | Log incoming frame data to terminal |
| `log_latencies` | `false` | Log latency information |
| `conf_file` | `initiate.yaml` | YAML config for individual marker names and initial positions |
| `node_name` | `natnet_ros2` | Name of the ROS 2 node |
| `activate` | `true` | Automatically activate the lifecycle node |
| `immt` | `PoseStamped` | Individual marker message type: `PoseStamped` or `PointStamped` |

#### Option 2: GUI launch

Use the GUI tool for interactive configuration. Follow the instructions in the output area.
```bash
ros2 launch natnet_ros2 gui_natnet_ros2.launch.py
```
![alt text](https://github.com/L2S-lab/natnet_ros2/blob/main/img/ui-1.png)

**Note:** When using the GUI, you must fill in at least one marker name in the "Single marker naming" tab before starting the node.

#### Configuring individual markers

To track unlabeled markers as named objects, edit `config/initiate.yaml` (or make a copy).
Each marker needs a name, an initial position (for nearest-neighbour matching), and a marker_config entry.

See `config/initiate.yaml` for the format. Then launch with:
```bash
ros2 launch natnet_ros2 natnet_ros2.launch.py \
  serverIP:=<IP> clientIP:=<IP> \
  pub_individual_marker:=true \
  conf_file:=your_config.yaml
```

To find initial marker positions, you can enable frame logging:
```bash
ros2 launch natnet_ros2 natnet_ros2.launch.py \
  serverIP:=<IP> clientIP:=<IP> \
  log_frames:=true
```

## License

This project is licensed under the **GNU General Public License v3.0** - see the
[LICENSE](LICENSE) file for details.
