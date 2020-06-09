import random
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 10)

    @task
    def index_page(self):
        i = random.randint(1, 16)
        self.client.get("/search?services=" + 'c' + str(i))
