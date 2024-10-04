import numpy as np

def find_safe_sequence(processes, avail, maxm, allot):
    need = maxm - allot
    finish = [False] * len(processes)
    work = avail #buoc 1: khoi tao work = available
    safe_sequence = []
    while len(safe_sequence) < len(processes):
        found = False
        for i in range(len(processes)):
            if not finish[i] and np.all(need[i] <= work):
                work += allot[i]
                finish[i] = True
                safe_sequence.append(processes[i])
                found = True
                break
        if not found:
            return None  # Không tìm thấy chuỗi an toàn
        print("Work after allocating resources for", processes[i], ":", work)
    return safe_sequence
def request_resources(processes, avail, maxm, allot, request, process_id):
    process_index = processes.index(process_id)
    if np.all(request <= avail) and np.all(request <= (maxm[process_index] - allot[process_index])):
        avail -= request
        allot[process_index] += request
        safe_sequence = find_safe_sequence(processes, avail, maxm, allot)
        if safe_sequence is not None:
            return safe_sequence
        else:
            # Không an toàn, hoàn trả tài nguyên và thử lại từ đầu
            allot[process_index] -= request
            avail += request
            return None
    else:
        return None


if __name__ == "__main__":
    num_processes = int(input("Enter the number of processes: "))
    num_resources = int(input("Enter the number of resource types: "))

    processes = [f'P{i}' for i in range(num_processes)]
    avail = np.array(list(map(int, input("Enter the available resources (format: A B C ...): ").split())))
    max_matrix = np.zeros((num_processes, num_resources), dtype=int)

    print("Enter the maximum resource matrix for each process:")
    for i in range(num_processes):
        max_matrix[i] = np.array(
            list(map(int, input(f"Enter the maximum resource for {processes[i]} (format: A B C ...): ").split())))

    allot = np.zeros((num_processes, num_resources), dtype=int)

    print("Enter the allocated resource matrix for each process:")
    for i in range(num_processes):
        allot[i] = np.array(
            list(map(int, input(f"Enter the initial allocation for {processes[i]} (format: A B C ...): ").split())))

    while True:
        print("\nAvailable Resources:")
        for j in range(num_resources):
            print(chr(65 + j), end="\t")

        for j in range(num_resources):
            print(avail[j], end="\t")
        print("\n")

        print("Max Matrix:")
        for i in range(num_processes):
            print(f"Process {i}: ", end="")
            for j in range(num_resources):
                print(max_matrix[i][j], end="\t")
            print()

        print("Allocated Matrix:")
        for i in range(num_processes):
            print(f"Process {i}: ", end="")
            for j in range(num_resources):
                print(allot[i][j], end="\t")
            print()

        print("\nMenu:")

        print("0. Khong Request")
        print("1. Request Resources")
        print("2. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            request = np.array(
                list(map(int, input("Enter the resource request for a process (format: A B C ...): ").split())))
            process_id = input("Enter the process ID to request resources (e.g., P0, P1, ...): ")

            safe_sequence = request_resources(processes, avail, max_matrix, allot, request, process_id)
            if safe_sequence is not None:
                print("Safe Sequence:", safe_sequence)

            else:
                print(f"The request of {process_id} is invalid or may lead to a deadlock.")
            break


        elif choice == 0:
            safe_sequence = find_safe_sequence(processes, avail, max_matrix, allot)
            if safe_sequence is not None:
                print("Chuỗi an toàn (Safe Sequence):", safe_sequence)
            else:
                print("Không tìm thấy chuỗi an toàn.")
            break

        elif choice == 2:
            break
        else:
            print("Invalid choice. Please try again.")




