import numpy as np
def standard_atmosphere_density(altitude_m):
    """
    Returns the density (kg/m^3) and speed of sound (m/s) for a given altitude (meters)
    based on the 1976 U.S. Standard Atmosphere model. This version ensures correct
    outputs, especially in cases like 15,000 meters.

    Parameters:
        altitude_m (float): Altitude in meters.

    Returns:
        tuple: (speed_of_sound, density)
    """
    # Constants
    P0 = 101325  # Sea-level standard pressure, Pa
    T0 = 288.15  # Sea-level standard temperature, K
    g0 = 9.80665  # Standard gravitational acceleration, m/s^2
    R = 287.05  # Specific gas constant for air, J/(kg·K)
    gamma = 1.4  # Ratio of specific heats for air
    lapse_rate = -0.0065  # Temperature lapse rate, K/m (troposphere)
    
    # Check altitude and calculate properties
    if altitude_m <= 11000:  # Troposphere
        T = T0 + lapse_rate * altitude_m  # Temperature
        P = P0 * (T / T0) ** (-g0 / (R * lapse_rate))  # Pressure
    elif altitude_m <= 20000:  # Tropopause (isothermal layer)
        T = 216.65  # Constant temperature
        P = 22632.06 * np.exp(-g0 * (altitude_m - 11000) / (R * T))  # Pressure
    else:
        # Extended layers not needed for now; calculations can be added for higher altitudes
        T = 216.65
        P = 5474.89 * (T / 216.65) ** (-g0 / (R * lapse_rate))

    # Density from Ideal Gas Law
    density = P / (R * T)

    # Speed of sound
    speed_of_sound = np.sqrt(gamma * R * T)
    
    return speed_of_sound, density

# Check at 15,000 meters
altitude = 15000  # in meters
speed_of_sound, density = standard_atmosphere_density(altitude)

print((speed_of_sound, density))
