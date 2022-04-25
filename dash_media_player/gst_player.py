# Import PyGObject (GStreamer's Python binding library)
import gi

""" Tell PyGObject the minimum version 
of GStreamer that our program requires, 
which the library shortens to "Gst """
gi.require_version("Gst", "1.0")

"""  Tell PyGObject the minimum version 
of GLib that our program requires """ 
gi.require_version("GLib", "2.0")

# Import the "Gst" module, as well as the "GLib" module
from gi.repository import Gst, GLib

# Import the function Thread from threading module
from threading import Thread

class GstPlayer:
    # Initialize GStreamer
    Gst.init()
    
    def __init__(self):
        # Define the pipeline
        self.pipeline = Gst.parse_launch(
            "appsrc name=source is-live=true max-bytes=0 ! "
            "qtdemux ! "
            "h264parse ! "
            "avdec_h264 ! "
            "timeoverlay halignment=center valignment=top \
            text='Stream time:' shaded-background=true \
            font-desc='Sans, 24'!" 
            "videoscale ! "
            "xvimagesink"
        )
        
        # Reference for appsrc element with name 'source'
        self.appsrc = self.pipeline.get_by_name("source")

        """ The main loop is in charge of handling events 
        and doing some other background tasks """
        self.main_loop = GLib.MainLoop()

        # Start it in a new thread
        self.thread = Thread(target=self.main_loop.run)
        self.thread.start()

    # Push a buffer into the source.
    def push(self, data):
        buffer = Gst.Buffer.new_wrapped(data)
        gst_flow_return = self.appsrc.emit('push-buffer', buffer)
        del buffer

        if gst_flow_return != Gst.FlowReturn.OK:
            print('We got some error, stop sending data')

    # Get the number of currently queued bytes inside appsrc.
    def get_queued_bytes(self):
        return self.appsrc.get_property("current-level-bytes")

    # Returns the current state flag of the pipeline.
    def _get_state(self):
        """ gst's get_state function returns a 3-tuple; 
        we just want the status flag in position 1. """
        return self.pipeline.get_state(Gst.CLOCK_TIME_NONE)[1]
    
    # Immediately begin playing the segments received.
    def play_segment(self):
        self.pipeline.set_state(Gst.State.NULL)
        # Start the pipeline up
        self.pipeline.set_state(Gst.State.PLAYING) 
        self.playing = True

    # If paused, resume playback.
    def play(self):
        if self._get_state() == Gst.State.PAUSED:
            self.pipeline.set_state(Gst.State.PLAYING)
            self.playing = True

    # Pause playback.
    def pause(self):
        self.pipeline.set_state(Gst.State.PAUSED)
        self.playing = False
    
    # Stop playback and clean up by setting it to the NULL state
    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.pipeline = False
    
    # Stop the main loop
    def quit_main_loop(self):
        self.main_loop.quit()