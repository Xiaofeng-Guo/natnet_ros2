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

#include "natnet_ros2/nn_filter.hpp"

float distance(float &x1,float &y1,float &z1,float &x2,float &y2,float &z2)
{
    return pow((x2 - x1),2)+pow((y2 - y1),2)+pow((z2 - z1),2);
}

int nn_filter(std::vector<object_data> &object_list, sMarker &data, float &E, float &E_x, float &E_y, float E_z, bool &individual_error, float &error_amp)
{   int idx = -1;
    float d_min=10.0;
    for(int i=0; i<(int)object_list.size(); i++)
    {
        if(!individual_error)
        {   float dist = distance(object_list[i].x, object_list[i].y, object_list[i].z,
                                    data.x, data.y, data.z);
            if(dist<E*error_amp && dist<d_min)
                {   
                    d_min = dist;
                    idx = i;
                }
        }
        else
        {
            if(abs(object_list[i].x-data.x)<E_x*error_amp && abs(object_list[i].y-data.y)<E_y*error_amp && abs(object_list[i].z-data.z)<E_z*error_amp)
            {
                return i;
            }
        }
    }
    return idx;
}