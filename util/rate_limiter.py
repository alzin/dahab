import time


class RateLimiter:
    """Rate limiter to limit the number of requests per minute."""
    REQUESTS_PER_MINUTE = 5
    SECONDS_IN_A_MINUTE = 60

    def __init__(self):
        # Initialize last_request_time with the current time
        self.last_request_time = time.time() - (self.SECONDS_IN_A_MINUTE /
                                                self.REQUESTS_PER_MINUTE)

    def wait(self):
        current_time = time.time()
        print("RateLimiter: Current Time:", current_time)
        print("RateLimiter: Last Request Time:", self.last_request_time)
        print("RateLimiter: Difference:", current_time - self.last_request_time)

        if self.last_request_time and current_time - self.last_request_time < (self.SECONDS_IN_A_MINUTE / self.REQUESTS_PER_MINUTE):
            time_to_wait = (self.SECONDS_IN_A_MINUTE / self.REQUESTS_PER_MINUTE) - \
                (current_time - self.last_request_time)
            print("RateLimiter: Waiting for", time_to_wait, "seconds.")
            time.sleep(time_to_wait)

        self.last_request_time = current_time
