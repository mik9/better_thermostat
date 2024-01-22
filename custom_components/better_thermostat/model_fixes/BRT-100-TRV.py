from homeassistant.components.climate.const import HVACAction

from custom_components.better_thermostat.utils.const import CalibrationMode
from custom_components.better_thermostat.utils.helpers import heating_power_valve_position

def fix_local_calibration(self, entity_id, offset):
    return offset


def fix_target_temperature_calibration(self, entity_id, temperature):
    _cur_trv_temp_s = self.real_trvs[entity_id]["current_temperature"]

    _calibration_mode = self.real_trvs[entity_id]["advanced"].get(
        "calibration_mode", CalibrationMode.DEFAULT
    )

    if _calibration_mode == CalibrationMode.AGGRESIVE_CALIBRATION:
        if self.attr_hvac_action == HVACAction.HEATING:
            temperature = _cur_trv_temp_s + 3.0

    if _calibration_mode == CalibrationMode.HEATING_POWER_CALIBRATION:
        if self.attr_hvac_action == HVACAction.HEATING:
            valve_position = heating_power_valve_position(self, entity_id)

            if valve_position <= 0.25:
                temp_diff = 1
            elif valve_position <= 0.5:
                temp_diff = 2
            elif valve_position <= 0.75:
                temp_diff = 3
            else:
                temp_diff = 4

            temperature = _cur_trv_temp_s + temp_diff

    if self.attr_hvac_action == HVACAction.IDLE:
        temperature = _cur_trv_temp_s - 3.0

    return temperature


async def override_set_hvac_mode(self, entity_id, hvac_mode):
    return False


async def override_set_temperature(self, entity_id, temperature):
    return False
