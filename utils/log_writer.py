import csv
from base.timer import Timer
from base.whiteboard import Whiteboard
from base.configuration_parser import ConfigurationParser


CSV_FILE_DIRECTORY = "./utils/"

class LogWriter:
    def __init__(self):
        self.whiteboard = Whiteboard.get_instance()
        config_parser = ConfigurationParser.get_instance()
        self.url_mpd = config_parser.get_parameter('url_mpd')

        self.timer = Timer.get_instance()

        self.time_qi = 0.0
        self.qi = 0
        self.segment = 0
        
        self.time_buffer = 0.0
        self.buffer_size = 0

        self.index_buffer = 0
        self.index_qi = 0

        self.previous_data_plot1 = ()
        self.previous_data_plot2 = ()
        
        self.fieldnames1 = ["qi", 'segment', "time_played"]
        self.fieldnames2 = ["buffer_size", "time"] 

        with open(CSV_FILE_DIRECTORY + 'qi_log.csv', 'w') as csv_file1:
            csv_writer = csv.DictWriter(csv_file1, fieldnames=self.fieldnames1)
            csv_writer.writeheader()

        with open(CSV_FILE_DIRECTORY + 'buffer_log.csv', 'w') as csv_file2:
            csv_writer = csv.DictWriter(csv_file2, fieldnames=self.fieldnames2)
            csv_writer.writeheader()

    def run(self):
        if 'BigBuckBunny' in self.url_mpd:
            segment_duration = self.url_mpd.split('/')[6]
            segment_duration = segment_duration.split('_')[1]
            segment_duration = int(segment_duration.split('s')[0])
        else:
            segment_duration = self.url_mpd.split('/')[7]
            segment_duration = segment_duration.split('_')[1]
            segment_duration = int(segment_duration.split('s')[0])

        all_seg_played = self.whiteboard.get_all_segments_played()

        while not all_seg_played:

            with open(CSV_FILE_DIRECTORY + 'qi_log.csv', 'a') as csv_file1:
                csv_writer = csv.DictWriter(csv_file1, fieldnames=self.fieldnames1)
                
                data_plot1 = self.whiteboard.get_playback_qi()
                

                if len(data_plot1) > 0 and len(data_plot1) == 1 + self.index_qi and data_plot1 != self.previous_data_plot1:
                    # print(data_plot1)
                    self.time_qi = data_plot1[self.index_qi][0]
                    self.qi = int(data_plot1[self.index_qi][1])
                    self.segment += 1 

                    info = {
                        "qi": self.qi,
                        "segment": self.segment,
                        "time_played": self.time_qi
                    }

                    csv_writer.writerow(info)

                    self.previous_data_plot1 = data_plot1
                    self.index_qi += segment_duration

            with open(CSV_FILE_DIRECTORY + 'buffer_log.csv', 'a') as csv_file2:
                csv_writer = csv.DictWriter(csv_file2, fieldnames=self.fieldnames2)

                data_plot2 = self.whiteboard.get_playback_buffer_size()

                if len(data_plot2) > 0 and data_plot2 != self.previous_data_plot2:
                    self.time_buffer = data_plot2[self.index_buffer][0]
                    self.buffer_size = int(data_plot2[self.index_buffer][1])

                    # self.time = self.timer.get_current_time()
                    # self.buffer_size = self.whiteboard.get_amount_video_to_play()

                    info = {
                        "buffer_size": self.buffer_size,
                        "time": self.time_buffer
                    }

                    csv_writer.writerow(info)

                    self.previous_data_plot2 = data_plot2
                    self.index_buffer += 1

            all_seg_played = self.whiteboard.get_all_segments_played()