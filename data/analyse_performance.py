import csv


def compute_performance():
    with open('dataOp2.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        count = 0
        wait_time = dict()
        for line in reader:
            count += 1
            time = line[1]
            clearance_time = int(line[2])
            safe = line[3]
            # print(f'flow {flow}, time {time}, clearance time {clearance_time} and safe {safe}')
            if safe == 0 or safe == '0':
                if wait_time.get(time, None) is None:
                    wait_time[time] = clearance_time
                else:
                    wait_time[time] += clearance_time

        avg_wait_time = 0
        for key, values in wait_time.items():
            # print(f'key {key} and values {values}')
            avg_wait_time += values
        print("result for observations: ", count)
        print("Average wait time : ", avg_wait_time // count)


if __name__ == '__main__':
    compute_performance()
