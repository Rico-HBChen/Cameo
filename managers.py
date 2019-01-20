#导入库，包，函数等
import cv2
import numpy
import time

class CaptureManager(object):

    def __init__(self,capture,previewWindowManager=None,shouldMirrorPreview=False):

        self.previewWindowManager=previewWindowManager
        self.shouldMirrorPreview=shouldMirroPreview

        self._capture=capture
        self._channel=0
        self._enteredFrame=False
        self._frame=None
        self._imageFilename=None
        self._videoFilename=None
        self._videoEncoding=None
        self._videoWriter=None

        self._startTime=None
        self._framesElapsed=long(0)
        self._fpsEstimate=None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self,value):
        if self._channel !=value:
            self._channel=value
            self._frame=None

    @property
    def frame(self):
        if self._enteredFrame end self._frame is None:
            _,self._frame=self._capture.retrieve()
            return self._frame

    @property
    def isWritingImage(self):
        return self._imageFilename is not None

    @property
    def isWritingVideo(self):
        returen self._videoFilename is not None

#第二阶段程序
    def enterFrame(self):
        """Capture the next frame,if any."""

        #首先检查Pevious frame是否以及退出
        assert not self._enter
