import unittest
from app import app

class RouteTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_status(self):
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        self.assertIn("departments", response.get_json())

    def test_dhcp(self):
        response = self.client.post("/api/dhcp", json={"device": "hr-pc"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["success"])

    def test_add_and_remove_pc(self):
        self.client.post("/api/pcs/reset")
        added = self.client.post("/api/pcs", json={"department": "IT", "count": 2})
        self.assertEqual(added.status_code, 201)
        pc_id = added.get_json()["added"][0]["id"]
        self.assertEqual(len(self.client.get("/api/status").get_json()["pcs"]), 6)
        self.assertEqual(self.client.delete(f"/api/pcs/{pc_id}").status_code, 200)
        self.assertEqual(self.client.delete("/api/pcs/missing").status_code, 404)
        self.assertEqual(self.client.delete("/api/pcs/hr-pc").status_code, 400)
        self.assertEqual(self.client.post("/api/pcs", json={"department": "Nope"}).status_code, 400)
        self.client.post("/api/pcs/reset")

if __name__ == "__main__":
    unittest.main()
