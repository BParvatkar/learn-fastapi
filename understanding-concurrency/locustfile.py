from locust import HttpUser, task


class SyncUser(HttpUser):
    @task
    def sync_request_test(self):
        self.client.get("/sync-request")


class AsyncUser(HttpUser):
    @task
    def async_request_test(self):
        self.client.get("/async-request")


class AsyncWithBlockUser(HttpUser):
    @task
    def async_request_test(self):
        self.client.get("/async-with-block-request")
