// Copyright 2024 Laboratoire des signaux et systèmes
//
// This program is free software: you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation, either version 3 of
// the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
//
// Author: Aarsh Thakker <aarsh.thakker@centralesupelec.fr>

#ifndef NN_FILTER_H
#define NN_FILTER_H

#include <NatNetTypes.h>
#include <cmath>
#include <vector>
#include "natnet_ros2/object_data.hpp"

float distance(float &x1,float &y1,float &z1,float &x2,float &y2,float &z2);

int nn_filter(std::vector<object_data> &object_list, sMarker &data, float &E, float &E_x, float &E_y, float E_z, bool &individual_error, float &error_amp);

#endif
