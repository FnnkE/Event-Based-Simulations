import matplotlib.pyplot as plt

# ----- Import Data From Files -----
normal_data = []
file = open("d_normal-timings.txt", 'r')
for line in file:
    normal_data.append(float(line.strip()))
file.close()

improved_event_edge_data = []
file = open("d_improved-filter-edge-timings.txt", 'r')
for line in file:
    improved_event_edge_data.append(float(line.strip()))
file.close()

event_edge_data = []
file = open("d_filter-edge-timings.txt", 'r')
for line in file:
    event_edge_data.append(float(line.strip()))
file.close()

frame_edge_data = []
file = open("d_edge-timings.txt", 'r')
for line in file:
    frame_edge_data.append(float(line.strip()))

improved_event_th_data = []
file = open("d_improved-filter-th-timings.txt", 'r')
for line in file:
    improved_event_th_data.append(float(line.strip()))
file.close()

event_th_data = []
file = open("d_filter-th-timings.txt", 'r')
for line in file:
    event_th_data.append(float(line.strip()))
file.close()

frame_th_data = []
file = open("d_th-timings.txt", 'r')
for line in file:
    frame_th_data.append(float(line.strip()))
file.close()

# ----- Calculate Averages -----
normal_avg = [sum(normal_data)/len(normal_data)] * len(normal_data)
improved_event_edge_avg = [sum(improved_event_edge_data)/len(improved_event_edge_data)] * len(improved_event_edge_data)
event_edge_avg = [sum(event_edge_data)/len(event_edge_data)] * len(event_edge_data)
frame_edge_average = [sum(frame_edge_data)/len(frame_edge_data)] * len(frame_edge_data)
improved_event_th_avg = [sum(improved_event_th_data)/len(improved_event_th_data)] * len(improved_event_th_data)
event_th_avg = [sum(event_th_data)/len(event_th_data)] * len(event_th_data)
frame_th_avg = [sum(frame_th_data)/len(frame_th_data)] * len(frame_th_data)


# ----- Plot Initial Timings -----
plt.figure(1)
plt.plot(normal_data, color='black', label="Normal Performance")
plt.plot(event_edge_data, 'b', label="Event-Like Edge Filter")
plt.plot(frame_edge_data, 'g', label="Frame-Based Edge Filter")
plt.plot(event_th_data, 'r', label="Event-Like Threshold Filter")
plt.plot(frame_th_data, color='orange', label="Frame-Based Threshold Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (s)")
plt.xlim(0, 100)
plt.title("Raw Timings")
plt.savefig("g_RawTimings.png")
plt.show()

# ----- Plot Inital Timing Averages -----
plt.figure(2)
plt.plot(normal_avg, color='black', label="Normal Performance")
plt.plot(event_edge_avg, color='b', label="Event-Like Edge Filter")
plt.plot(frame_edge_average, color='g', label="Frame-Based Edge Filter")
plt.plot(event_th_avg, color='r', label="Event-Like Threshold Filter")
plt.plot(frame_th_avg, color='orange', label="Frame-Based Threshold Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (s)")
plt.xlim(0, 100)
plt.title("Average Timings")
plt.savefig("g_AvgTimings.png")
plt.show()

# ----- Plot Imporved Edge Timings -----
plt.figure(3)
plt.plot(normal_data, color='black', label="Normal Performance")
plt.plot(event_edge_data, color='b', label="Event-Like Edge Filter")
plt.plot(frame_edge_data, color='g', label="Frame-Based Edge Filter")
plt.plot(improved_event_edge_data, color='r', label="Improved Event-Like Edge Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (s)")
plt.xlim(0, 100)
plt.title("Raw Timings")
plt.savefig("g_ImprovedTimings.png")
plt.show()

# ----- Plot Improved Edge Timing Averages -----
plt.figure(4)
plt.plot(normal_avg, color='black', label="Normal Performance")
plt.plot(event_edge_avg, color='b', label="Event-Like Edge Filter")
plt.plot(frame_edge_average, color='g', label="Frame-Based Edge Filter")
plt.plot(improved_event_edge_avg, color='r', label="Improved Event-Like Edge Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (s)")
plt.xlim(0, 100)
plt.title("Raw Timings")
plt.savefig("g_ImprovedAvgTimings.png")
plt.show()

# ----- Plot Improved Threshold Timings -----
plt.figure(5)
plt.plot(normal_data, color='black', label="Normal Performance")
plt.plot(event_th_data, 'b', label="Event-Like Threshold Filter")
plt.plot(frame_th_data, color='g', label="Frame-Based Threshold Filter")
plt.plot(improved_event_th_data, color='r', label="Improved Event-Like Threshold Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (s)")
plt.xlim(0, 100)
plt.title("Raw Timings")
plt.savefig("g_ImprovedTHTimings.png")
plt.show()

# ----- Plot Imporved Threshold Timing Averages -----
plt.figure(6)
plt.plot(normal_avg, color='black', label="Normal Performance")
plt.plot(event_th_avg, color='b', label="Event-Like Threshold Filter")
plt.plot(frame_th_avg, color='g', label="Frame-Based Threshold Filter")
plt.plot(improved_event_th_avg, color='r', label="Improved Event-Like Threshold Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (s)")
plt.xlim(0, 100)
plt.title("Average Timings")
plt.savefig("g_ImprovedAvgTHTimings.png")
plt.show()

# ----- Plot Improved Timings -----
plt.figure(7)
plt.plot(normal_data, color='r', label="Normal Performance")
plt.plot(improved_event_edge_data, color='g', label="Improved Event-Like Edge Filter")
plt.plot(improved_event_th_data, color='b', label="Improved Event-Like Threshold Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (s)")
plt.xlim(0, 100)
plt.title("Average Timings")
plt.savefig("g_ImprovedTimings.png")
plt.show()

# ----- Plot Imporved Timing Averages -----
plt.figure(8)
plt.plot(normal_avg, color='r', label="Normal Performance")
plt.plot(improved_event_edge_avg, color='g', label="Improved Event-Like Edge Filter")
plt.plot(improved_event_th_avg, color='b', label="Improved Event-Like Threshold Filter")

plt.legend()
plt.xlabel("Frames")
plt.ylabel("Time (s)")
plt.xlim(0, 100)
plt.title("Average Timings")
plt.savefig("g_ImprovedAvgTimings.png")
plt.show()