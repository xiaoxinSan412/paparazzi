/*
 * Copyright (C) 2011-2012 Team ATMOS
 *
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
 */

/** @file firmwares/rotorcraft/stabilization/stabilization_helpers.h
 *  Stabilization helper functions for rotorcrafts.
 */

#ifndef STABILIZATION_HELPERS_H
#define STABILIZATION_HELPERS_H

#include "math/pprz_algebra_int.h"

inline int32_t stabilization_compute_heading(struct Int32Eulers* ltp_to_rotation_axis);

//maybe put this in the state interface?
inline int32_t stabilization_compute_heading(struct Int32Eulers* ltp_to_rotation_axis) {
  int32_t sinTheta;
  PPRZ_ITRIG_SIN(sinTheta, ltp_to_rotation_axis->theta); //in ANG_FRAC
  return (int32_t)(ltp_to_rotation_axis->psi - ((sinTheta*ltp_to_rotation_axis->phi)>>INT32_TRIG_FRAC));
}

#endif /* STABILIZATION_HELPERS_H */
