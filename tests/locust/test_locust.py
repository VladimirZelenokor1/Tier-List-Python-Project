from locust import HttpUser, task, between


class AppUser(HttpUser):
    wait_time = between(2, 5)

    @task
    def app(self):
        self.client.get("/")

    @task
    def auth(self):
        self.client.get("/auth")

    @task
    def templates(self):
        self.client.get("/template-tiers")  # Will redirect to auth

    # @task
    # def auth(self):
    #     self.client.get("/auth")
