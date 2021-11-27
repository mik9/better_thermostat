import time
from homeassistant.helpers.json import JSONEncoder


class cleanState:
  def __init__(self, current_temperature, local_temperature,local_temperature_calibration,system_mode,has_real_mode = True, calibration = 0):
    self.current_temperature = current_temperature
    self.local_temperature = local_temperature
    self.local_temperature_calibration = local_temperature_calibration
    self.system_mode = system_mode
    self.has_real_mode = has_real_mode
    self.calibration = calibration


def default_calibration(self):
  state = self.hass.states.get(self.heater_entity_id).attributes
  new_calibration = float(round(float(self._cur_temp) - (float(state.get('local_temperature')) - float(state.get('local_temperature_calibration'))),1))
  return new_calibration

def temperature_calibration(self):
  state = self.hass.states.get(self.heater_entity_id).attributes
  mqtt = self.hass.components.mqtt
  new_calibration = abs(float(round(float(self._target_temp) - (float(self._cur_temp) + float(state.get('local_temperature'))),1)))
  if new_calibration < float(self._min_temp):
      new_calibration = float(self._min_temp)
  if new_calibration > float(self._max_temp):
      new_calibration = float(self._max_temp)

  if state.get('system_mode') is not None and self._target_temp is not None and self._cur_temp is not None:
      check_overswing = (float(self._target_temp) - 0.5) < float(self._cur_temp)
      if check_overswing:
        mqtt.async_publish('zigbee2mqtt/'+state.get('friendly_name')+'/set/current_heating_setpoint', float(5), 0, False)
        time.sleep(30)
        mqtt.async_publish('zigbee2mqtt/'+state.get('friendly_name')+'/set/current_heating_setpoint', float(new_calibration), 0, False)
  return new_calibration