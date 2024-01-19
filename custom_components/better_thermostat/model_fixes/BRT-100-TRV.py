from homeassistant.components.climate.const import HVACAction

def fix_local_calibration(self, entity_id, offset):
    if self.attr_hvac_action == HVACAction.IDLE:
        if offset < self.tolerance:
            offset = self.tolerance
    
    return offset


def fix_target_temperature_calibration(self, entity_id, temperature):
    _cur_trv_temp_s = self.real_trvs[entity_id]["current_temperature"]

    if self.attr_hvac_action == HVACAction.IDLE:
        if temperature - _cur_trv_temp_s > 0.0:
            temperature -= self.tolerance

    return temperature


async def override_set_hvac_mode(self, entity_id, hvac_mode):
    return False


async def override_set_temperature(self, entity_id, temperature):
    return False
