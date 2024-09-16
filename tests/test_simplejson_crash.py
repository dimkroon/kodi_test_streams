

import unittest

import addon
from kodi_addon_checker.addons.Addon import Addon


class Tests(unittest.TestCase):
    def test_str_count(sefl):
        addon.test_str_count()

    def test_build_error_message(self):
        addon.test_build_msg()

    def test_create_smpl_xception_wo_requests(self):
        addon.test_simplejson_exc()

    def test_create_standard_json_exception(self):
        addon.test_stdjson_exc()

    def test_simplejson_loads_wo_requests(self):
        addon.test_simpjson_loads()

    def test_simplejson_loads_w_requests(self):
        addon.test_simpjson_loads_req()

    def test_standard_json_loads(self):
        addon.test_std_json_loads()

    def test_requests_response_jons(self):
        addon.test_resp_json()

    def test_unhandled_JSONDecodeError(self):
        addon.test_unhandled_json_error()