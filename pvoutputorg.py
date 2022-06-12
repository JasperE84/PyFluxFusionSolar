import requests
from datetime import datetime

class PvOutputOrg:
    def __init__(self, conf, logger):
        self.conf = conf
        self.logger = logger
        self.logger.debug("PvOutputOrg class instantiated")

    def write_to_pvoutput(self, fusionsolar_json_data):
        if self.conf.pvoutput:
            pvoutput_header_obj = {
                "X-Pvoutput-Apikey": self.conf.pvoutputapikey,
                "X-Pvoutput-SystemId": self.conf.pvoutputsystemid,
            }

            pvoutput_data_obj = self.make_pvoutput_data_obj(fusionsolar_json_data)

            try:
                self.logger.info("Writing to PVOutput. Header: {} Data: {}".format(pvoutput_header_obj, pvoutput_data_obj))
                api_response = requests.post(self.conf.pvoutputurl, data=pvoutput_data_obj, headers=pvoutput_header_obj)
                self.logger.debug("PVOutput response {}".format(api_response.text))
            except Exception as e:
                raise Exception("Exception while posting data to PVOutput: '{}'".format(str(e)))

        else:
            self.logger.debug("PVOutput writing disabled")

    def make_pvoutput_data_obj(self, response_json_data):
        current_time = datetime.now()
        pvodate = current_time.strftime("%Y%m%d")
        pvotime = current_time.strftime("%H:%M")

        pvoutput_data_obj = {
            "d": pvodate,
            "t": pvotime,
            "v1": float(response_json_data["realKpi"]["cumulativeEnergy"]),
            "v2": float(response_json_data["realKpi"]["realTimePower"]),
            "c1": 2,
        }

        return pvoutput_data_obj
