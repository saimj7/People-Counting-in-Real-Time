import cv2, threading, queue

class ThreadingClass:
  # initiate threading class
  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
	# define an empty queue and thread
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read the frames as soon as they are available
  # this approach removes OpenCV's internal buffer and reduces the frame lag
  def _reader(self):
    while True:
      ret, frame = self.cap.read() # read the frames and ---
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()
        except queue.Empty:
          pass
      self.q.put(frame) # --- store them in a queue (instead of the buffer)

  def read(self):
    return self.q.get() # fetch frames from the queue one by one
