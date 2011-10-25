/*
 * This file is part of paparazzi.
 *
 * paparazzi is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * paparazzi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, write to
 * the Free Software Foundation, 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 */

#ifndef PPZUAVIMU_H
#define PPZUAVIMU_H

#include "std.h"
#include "subsystems/imu.h"

extern volatile bool_t gyr_valid;
extern volatile bool_t acc_valid;
extern volatile bool_t mag_valid;

/* must be defined in order to be IMU code: declared in imu.h
extern void imu_impl_init(void);
extern void imu_periodic(void);
*/

/* ADDED for moving average filter(s) */
#ifdef IMU_ACCEL_MA_FILTER_WINDOW
struct Imu_MA_Filter_Vect3 {
  int16_t cnt;
  int32_t sumX;
  int32_t sumY;
  int32_t sumZ;
  int32_t bufferX[IMU_ACCEL_MA_FILTER_WINDOW];
  int32_t bufferY[IMU_ACCEL_MA_FILTER_WINDOW];
  int32_t bufferZ[IMU_ACCEL_MA_FILTER_WINDOW];
};
#endif
/* ADDED end */

#define ImuEvent(_gyro_handler, _accel_handler, _mag_handler) {   \
    ppzuavimu_module_event();                \
    if (gyr_valid) {                         \
      gyr_valid = FALSE;                     \
      _gyro_handler();                                  \
    }                                                   \
    if (acc_valid) {                         \
      acc_valid = FALSE;                     \
      _accel_handler();                                 \
    }                                                   \
    if (mag_valid) {                         \
      mag_valid = FALSE;                     \
      _mag_handler();                                 \
    }                                                   \
}

/* Own Extra Functions */
extern void ppzuavimu_module_event( void );
extern void ppzuavimu_module_downlink_raw( void );
/* ADDED for moving average filter(s) */
#ifdef IMU_ACCEL_MA_FILTER_WINDOW
extern void ppzuavimu_module_update_ma_filter(struct Imu_MA_Filter_Vect3 *filter, int16_t new_x, int16_t new_y, int16_t new_z);
#endif
/* ADDED end */


#endif // PPZUAVIMU_H
