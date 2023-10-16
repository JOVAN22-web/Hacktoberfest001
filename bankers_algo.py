class BankersAlgorithm:
    def __init__(self, max_resources, allocated_resources):
        self.max_resources = max_resources  # Maximum available resources
        self.allocated_resources = allocated_resources  # Currently allocated resources
        self.available_resources = [max_res - allocated_res for max_res, allocated_res in zip(max_resources, allocated_resources)]  # Available resources
        self.num_processes = len(max_resources)
        self.num_resources = len(max_resources[0])
        self.need = [[max_res - allocated_res for max_res, allocated_res in zip(max_row, allocated_row)] for max_row, allocated_row in zip(max_resources, allocated_resources)]

    def is_safe_state(self, sequence):
        work = self.available_resources[:]
        finish = [False] * self.num_processes

        for i in sequence:
            if finish[i] is False and all(need <= work for need, work in zip(self.need[i], work)):
                work = [work + allocated for work, allocated in zip(work, self.allocated_resources[i])]
                finish[i] = True

        return all(finish)

    def request_resources(self, process, request):
        if all(request <= self.need[process]) and all(request <= self.available_resources):
            # Temporarily allocate resources to the process
            self.allocated_resources[process] = [allocated + req for allocated, req in zip(self.allocated_resources[process], request)]
            self.available_resources = [avail - req for avail, req in zip(self.available_resources, request)]
            self.need[process] = [need - req for need, req in zip(self.need[process], request)]

            # Check if the new state is safe
            if self.is_safe_state(range(self.num_processes)):
                return True
            else:
                # Roll back the allocation if it results in an unsafe state
                self.allocated_resources[process] = [allocated - req for allocated, req in zip(self.allocated_resources[process], request)]
                self.available_resources = [avail + req for avail, req in zip(self.available_resources, request)]
                self.need[process] = [need + req for need, req in zip(self.need[process], request)]
                return False
        else:
            return False

# Example usage
max_resources = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]

allocated_resources = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

banker = BankersAlgorithm(max_resources, allocated_resources)

request = [1, 0, 2]  # Example request for process 1

if banker.request_resources(1, request):
    print("Request granted. System is in safe state.")
else:
    print("Request denied. System would be in an unsafe state.")


if banker.request_resources(1, request):
    print("Request granted. System is in safe state.")
else:
    print("Request denied. System would be in an unsafe state.")
