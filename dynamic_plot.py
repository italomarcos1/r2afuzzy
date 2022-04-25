import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

CSV_FILE_DIRECTORY = "./utils/"

plt.style.use('seaborn')

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

def animate(i):
    qi_data = pd.read_csv(CSV_FILE_DIRECTORY + 'qi_log.csv')
    qi = qi_data['qi']
    segment = qi_data['segment']

    buffer_data = pd.read_csv(CSV_FILE_DIRECTORY + 'buffer_log.csv')
    buffer_size = buffer_data['buffer_size']
    time_buffer = buffer_data['time']

    ax1.cla()
    ax2.cla()

    ax1.plot(segment, qi, label='Quality Index')

    ax1.legend(loc='upper right')
    ax1.set_title('Quality index x Segment (during playback)')
    ax1.set_xlabel('Segment')
    ax1.set_ylabel('Quality index (0-19)')
    plt.tight_layout()

    ax2.plot(time_buffer, buffer_size, label='Buffer ocupation', color='#444444', linestyle='--')

    ax2.legend(loc='upper right')
    ax2.set_title('Buffer size x Time')
    ax2.set_xlabel('Execution time (seconds)')
    ax2.set_ylabel('Buffer size (seconds)')
    plt.tight_layout()

ani = FuncAnimation(fig, animate, interval=1)

plt.tight_layout()
plt.show()