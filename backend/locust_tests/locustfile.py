from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 5) 
    host = "http://localhost:8000"

    @task
    def get_endpoint(self):
        self.client.get("/shop/")  

