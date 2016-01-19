# built-in
import sys
import os
import xml.etree.ElementTree as ET

# external
sys.path.append('Y:/Workspace/SCRIPTS/python')
from PyQt4 import QtGui, QtCore, uic
from timecode import Timecode

TC_BASE = '59.94'
DEBUG = False

class EdlList(QtGui.QListWidget):
    def __init__(self, type, parent=None):
        super(EdlList, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

    def iterate(self):
        for i in range(self.count()):
            yield self.item(i).text()


class LogWidget(QtGui.QWidget):

    def __init__(self):
        super(LogWidget, self).__init__()

        self.setWindowTitle('Edit Log Generator')

        self.list_view = EdlList(self)
        self.exec_btn = QtGui.QPushButton('C O N V E R T')
        self.exec_btn.setEnabled(0)

        self.connect(self.list_view, QtCore.SIGNAL("dropped"), self.dropEDL)
        self.initUI()

    def initUI(self):
        layout = QtGui.QVBoxLayout()

        layout.addWidget(self.list_view)
        layout.addWidget(self.exec_btn)

        self.setLayout(layout)

        self.exec_btn.clicked.connect(self.execute)

        self.show()

    def dropEDL(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)
                self.exec_btn.setEnabled(1)
                item = QtGui.QListWidgetItem(url, self.list_view)
                item.setStatusTip(url)

    def execute(self, state):
        for edl in self.list_view.iterate():
            edl = str(edl)
            if (".edl" in edl) or (".EDL" in edl):
                edlToLog(edl)
            elif (".xml" in edl) or (".XML" in edl):
                xmlToLog(edl)


def run():
    app = QtGui.QApplication(sys.argv)
    wid = LogWidget()
    sys.exit(app.exec_())


def frameToTC(frame, base=TC_BASE):
    tc = Timecode(base, '00:00:00:00')
    tc.frames = frame

    return tc


def sequence(in_, out_, base=TC_BASE, debug=DEBUG):
    if isinstance(in_, int):
        in_ = frameToTC(in_)

    if isinstance(out_, int):
        out_ = frameToTC(out_)

    elif isinstance(in_, Timecode):
        pass

    elif isinstance(out_, Timecode):
        pass

    return (in_, out_)


def xmlToLog(XML, out_path=None):
    # LOAD XML TREE
    tree = ET.parse(XML)
    root = tree.getroot()
    
    # CREATE OUTPUT STRING
    out_string = ''
    
    # SET OUT POINT TO 0
    xout = 0

    # Find the Video element
    video = root.find('sequence/media/video')

    # Iterate over all tracks in the video element
    for track in video.iter('track'):

        # Iterate over all clips in the track
        for clipitem in track.findall('clipitem'):

            # Get clip name, timeline in & out points
            name = clipitem.find('name').text
            in_  = clipitem.find('start').text
            out_ = clipitem.find('end').text

            # Add an extra linebreak if the clips do not butt together
            # (Detecting this is why we store the out frame on each iteration)
            if (in_ != xout):
                out_string += ',,\n'

            # Write the line (note inline conversion from str to int to timecode)
            out_string += '{},{},{}\n'.format(name, frameToTC(int(in_)), frameToTC(int(out_)))

            # Store the out frame for next iteration
            xout = out_

    # Write the CSV
    if not (out_path):
        out_path = os.path.dirname(XML)

    out_csv = os.path.join(out_path, XML + '.csv')

    with open(out_csv, 'w') as out_stream:
        out_stream.write(out_string)


def edlToLog(EDL, out_path=None):
    out_stream = ''

    with open(EDL, 'r') as edl:
    
        for line in edl:

            line = line.split()
            
            clip_name  = line[1]
            try:
                clip_start = line[6]
                clip_end   = line[7]
            except:
                continue

            '''
            if ('SLATE' in clip_name) or \
               ('BLK' in clip_name) or \
               ('BLACK' in clip_name):
                continue

            else:
            '''
            out_stream += "{},{},{}\n".format(clip_name, clip_start, clip_end)


    # Write the CSV
    if not (out_path):
        out_path = os.path.dirname(EDL)

    out_csv = os.path.join(out_path, EDL + '.csv')

    with open(out_csv, 'w') as csv:
        csv.write(out_stream)

    return True


if __name__ == '__main__':
    run()