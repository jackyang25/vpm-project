from datetime import time


def find_available_time_blocks(time_blocks):
    if not time_blocks:
        return []

    merged_blocks = []
    time_blocks.sort(key=lambda x: x[0])  # Sort by start time

    start, end = time_blocks[0]
    print(start,end)
    for block in time_blocks[1:]:
        if block[0] <= end:  # Overlapping or adjacent blocks
            end = max(end, block[1])
        else:  # Non-overlapping block
            merged_blocks.append([start, end])
            start, end = block

    merged_blocks.append([start, end])  # Add the last merged block

    return merged_blocks

def main():
    time_blocks =  [[time(6, 10), time(7, 0)], [time(18, 0), time(20, 0)], [time(16, 0), time(22, 0)]]
   
    print(find_available_time_blocks(time_blocks))

if __name__ =="__main__":
    main()

