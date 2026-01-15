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


# class AsyncWithSyncUser(HttpUser):
#     host = "http://localhost:8000"
#     @task
#     def hello_sync_time_sleep(self):
#         request_id = str(uuid.uuid4().hex[:8])
#         self.client.get("/hello_async_time_sleep", headers={
#             "X-Request-ID": request_id
#         })
#         self.stop()
#         # if self.environment.runner.state != STATE_STOPPING:
#         #     self.environment.runner.quit()
