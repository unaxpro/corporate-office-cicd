import unittest
from corporate_network import CorporateNetwork

class CorporateNetworkTests(unittest.TestCase):
    def setUp(self):
        self.net = CorporateNetwork()

    def test_dhcp_lease(self):
        result = self.net.dhcp_request("hr-pc")
        self.assertTrue(result["success"])
        self.assertEqual(result["lease"]["gateway"], "192.168.10.1")

    def test_dns_lookup(self):
        result = self.net.dns_lookup("intranet.corp.local")
        self.assertTrue(result["success"])
        self.assertEqual(result["answer"], "192.168.50.20")

    def test_dns_failure(self):
        self.net.toggle_failure("dns")
        self.assertFalse(self.net.dns_lookup("intranet.corp.local")["success"])

    def test_dhcp_failure(self):
        self.net.toggle_failure("dhcp")
        self.assertFalse(self.net.dhcp_request("hr-pc")["success"])

    def test_department_isolation_model(self):
        result = self.net.connect("hr-pc", "finance-pc")
        self.assertFalse(result["success"])

    def test_web_server_allowed(self):
        result = self.net.connect("hr-pc", "web-server")
        self.assertTrue(result["success"])

class PcManagementTests(unittest.TestCase):
    def setUp(self):
        self.net = CorporateNetwork()

    def test_add_multiple_pcs_get_unique_ips_and_names(self):
        result = self.net.add_pcs("HR", None, 3)
        self.assertTrue(result["success"])
        ips = {p["ip"] for p in result["added"]}
        labels = [p["label"] for p in result["added"]]
        self.assertEqual(len(ips), 3)
        self.assertEqual(labels, ["HR PC 2", "HR PC 3", "HR PC 4"])
        self.assertNotIn("192.168.10.100", ips)

    def test_custom_name_with_count_is_numbered(self):
        result = self.net.add_pcs("Sales", "Booth", 2)
        self.assertEqual([p["label"] for p in result["added"]], ["Booth 1", "Booth 2"])

    def test_rejects_bad_input(self):
        self.assertFalse(self.net.add_pcs("Legal", None, 1)["success"])
        self.assertFalse(self.net.add_pcs("HR", "bad/name", 1)["success"])
        self.assertFalse(self.net.add_pcs("HR", None, 0)["success"])
        self.assertFalse(self.net.add_pcs("HR", None, 11)["success"])
        self.assertFalse(self.net.add_pcs("HR", None, "abc")["success"])

    def test_duplicate_name_rejected_without_partial_add(self):
        self.net.add_pcs("HR", "Desk", 1)
        before = len(self.net.pcs)
        self.assertFalse(self.net.add_pcs("IT", "desk", 1)["success"])
        self.assertEqual(len(self.net.pcs), before)

    def test_department_capacity_limit(self):
        self.assertTrue(self.net.add_pcs("IT", None, 10)["success"])
        self.assertTrue(self.net.add_pcs("IT", None, 1)["success"])
        self.assertFalse(self.net.add_pcs("IT", None, 1)["success"])

    def test_remove_pc_releases_lease(self):
        pc = self.net.add_pcs("Finance", None, 1)["added"][0]["id"]
        self.net.dhcp_request(pc)
        self.assertIn(pc, self.net.leases)
        self.assertTrue(self.net.remove_pc(pc)["success"])
        self.assertNotIn(pc, self.net.leases)
        self.assertNotIn(pc, self.net.pcs)

    def test_cannot_remove_last_pc_or_unknown(self):
        self.assertFalse(self.net.remove_pc("hr-pc")["success"])
        self.assertFalse(self.net.remove_pc("nope")["success"])

    def test_freed_ip_is_reused(self):
        first = self.net.add_pcs("HR", None, 1)["added"][0]
        self.net.remove_pc(first["id"])
        again = self.net.add_pcs("HR", None, 1)["added"][0]
        self.assertEqual(first["ip"], again["ip"])

    def test_same_vlan_allowed_even_if_trunk_down(self):
        pc = self.net.add_pcs("HR", None, 1)["added"][0]["id"]
        self.net.toggle_failure("link")
        self.assertTrue(self.net.connect("hr-pc", pc)["success"])
        self.assertFalse(self.net.connect(pc, "finance-pc")["success"])

    def test_new_pc_can_use_dhcp_and_reach_services(self):
        pc = self.net.add_pcs("Sales", None, 1)["added"][0]["id"]
        lease = self.net.dhcp_request(pc)["lease"]
        self.assertEqual(lease["gateway"], "192.168.40.1")
        self.assertTrue(self.net.connect(pc, "web-server")["success"])

    def test_simulation_reset_keeps_pcs_but_reset_pcs_restores_defaults(self):
        self.net.add_pcs("HR", None, 2)
        self.net.reset()
        self.assertEqual(len(self.net.pcs), 6)
        self.net.reset_pcs()
        self.assertEqual(len(self.net.pcs), 4)

if __name__ == "__main__":
    unittest.main()
