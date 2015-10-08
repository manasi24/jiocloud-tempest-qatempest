# Copyright 2015 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import copy
import httplib2

from oslo_serialization import jsonutils as json
from oslotest import mockpatch

from tempest.services.compute.json import quota_classes_client
from tempest.tests import base
from tempest.tests import fake_auth_provider


class TestQuotaClassesClient(base.TestCase):

    FAKE_QUOTA_CLASS_SET = {
        "injected_file_content_bytes": 10240,
        "metadata_items": 128,
        "server_group_members": 10,
        "server_groups": 10,
        "ram": 51200,
        "floating_ips": 10,
        "key_pairs": 100,
        "id": u'\u2740(*\xb4\u25e1`*)\u2740',
        "instances": 10,
        "security_group_rules": 20,
        "security_groups": 10,
        "injected_files": 5,
        "cores": 20,
        "fixed_ips": -1,
        "injected_file_path_bytes": 255,
        }

    def setUp(self):
        super(TestQuotaClassesClient, self).setUp()
        fake_auth = fake_auth_provider.FakeAuthProvider()
        self.client = quota_classes_client.QuotaClassesClient(
            fake_auth, 'compute', 'regionOne')

    def _test_show_quota_class_set(self, bytes_body=False):
        serialized_body = json.dumps({
            "quota_class_set": self.FAKE_QUOTA_CLASS_SET})
        if bytes_body:
            serialized_body = serialized_body.encode('utf-8')

        mocked_resp = (httplib2.Response({'status': 200}), serialized_body)
        self.useFixture(mockpatch.Patch(
            'tempest.common.service_client.ServiceClient.get',
            return_value=mocked_resp))
        resp = self.client.show_quota_class_set("test")
        self.assertEqual(self.FAKE_QUOTA_CLASS_SET, resp)

    def test_show_quota_class_set_with_str_body(self):
        self._test_show_quota_class_set()

    def test_show_quota_class_set_with_bytes_body(self):
        self._test_show_quota_class_set(bytes_body=True)

    def test_update_quota_class_set(self):
        fake_quota_class_set = copy.deepcopy(self.FAKE_QUOTA_CLASS_SET)
        fake_quota_class_set.pop("id")
        serialized_body = json.dumps({"quota_class_set": fake_quota_class_set})

        mocked_resp = (httplib2.Response({'status': 200}), serialized_body)
        self.useFixture(mockpatch.Patch(
            'tempest.common.service_client.ServiceClient.put',
            return_value=mocked_resp))
        resp = self.client.update_quota_class_set("test")
        self.assertEqual(fake_quota_class_set, resp)
