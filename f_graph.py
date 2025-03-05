import matplotlib.pyplot as plt

normal_data = []
file = open("MidtermProject/d_normal-timings.txt", 'r')
for line in file:
    normal_data.append(float(line.strip()))  # Remove newline characters
file.close()

event_edge_data = []
file = open("MidtermProject/d_filter-edge-timings.txt", 'r')
for line in file:
    event_edge_data.append(float(line.strip()))  # Remove newline characters
file.close()

frame_edge_data = []
file = open("MidtermProject/d_edge-timings.txt", 'r')
for line in file:
    frame_edge_data.append(float(line.strip()))  # Remove newline characters

event_th_data = []
file = open("MidtermProject/d_filter-th-timings.txt", 'r')
for line in file:
    event_th_data.append(float(line.strip()))  # Remove newline characters
file.close()

frame_th_data = []
file = open("MidtermProject/d_th-timings.txt", 'r')
for line in file:
    frame_th_data.append(float(line.strip()))  # Remove newline characters
file.close()

normal_avg = [sum(normal_data)/len(normal_data)] * len(normal_data)
event_edge_avg = [sum(event_edge_data)/len(event_edge_data)] * len(event_edge_data)
frame_edge_average = [sum(frame_edge_data)/len(frame_edge_data)] * len(frame_edge_data)
event_th_avg = [sum(event_th_data)/len(event_th_data)] * len(event_th_data)
frame_th_avg = [sum(frame_th_data)/len(frame_th_data)] * len(frame_th_data)


plt.figure(1)
plt.plot(normal_data, color='black', label="Normal Performance")
plt.plot(event_edge_data, 'b', label="Event-Like Edge Filter")
plt.plot(frame_edge_data, 'g', label="Frame-Based Edge Filter")
plt.plot(event_th_data, 'r', label="Event-Like Threshold Filter")
plt.plot(frame_th_data, 'r', label="Frame-Based Threshold Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (ms)")
plt.xlim(0, 100)
plt.title("Raw Timings")
plt.savefig("g_RawTimings.png")
plt.show()



plt.figure(2)
plt.plot(normal_avg, color='black', label="Normal Performance")
plt.plot(event_edge_avg, color='purple', label="Event-Like Edge Filter")
plt.plot(frame_edge_average, color='teal', label="Frame-Based Edge Filter")
plt.plot(event_th_avg, color='orange', label="Event-Like Threshold Filter")
plt.plot(frame_th_avg, 'r', label="Frame-Based Threshold Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (ms)")
plt.xlim(0, 100)
plt.title("Average Timings")
plt.savefig("g_AvgTimings.png")
plt.show()

