import time
from locust import HttpUser, task, between

class UserClient(HttpUser):
    wait_time = between(10, 30)
    host = "https://tsy-iabs.online"

    default_headers = {
        "Accept": "application/json, text/plain, */*",
        "Host": "tsy-iabs.online",
        "Origin": "https://the-strength-yard.vercel.app",
        "Referer": "https://the-strength-yard.vercel.app/",
    }

    def on_start(self):
        with self.client.post(
            "/login", 
            json={"EmailAddress":"admin@tsy.com", "Password":"12345678"},
            catch_response=True
        ) as resp:
            if resp.status_code == 200:
                response_json = resp.json()
                UserClient.default_headers["Authorization"] = "Bearer " + response_json[1]["token"]
                resp.success()
            else:
                resp.failure("Login failed")
            
        time.sleep(5)

    
    @task
    def check_protected(self):
        with self.client.get(
            "/protected",
            headers=UserClient.default_headers,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure("Failed to get protected route")

    @task
    def get_public_membership(self):
        with self.client.get(
            "/memberships/public",
            headers=UserClient.default_headers,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure("Failed to get public memberships list")
            
    @task
    def view_class_slots(self):
        with self.client.get(
            "/classSlot",
            headers=UserClient.default_headers,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure("Failed to get class slots")

    @task
    def view_membership_log(self):
        with self.client.get(
            "/membershiplog/2",
            headers=UserClient.default_headers,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure("Failed to get membership log")

    @task
    def view_membership_record(self):
        with self.client.get(
            "/membershiprecord/1",
            headers=UserClient.default_headers,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure("Failed to get membership record")

    @task
    def view_points_history(self):
        with self.client.get(
            "/pointsHistory/2",
            headers=UserClient.default_headers,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure("Failed to get membership record")
    
    @task
    def view_payments_history(self):
        with self.client.get(
            "/payments/history/membershiprecord/2",
            headers=UserClient.default_headers,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure("Failed to get points history")


