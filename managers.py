#导入库，包，函数等
import cv2
import numpy
import time

class CaptureManager(object):

    def __init__(self,capture,previewWindowManager=None,shouldMirrorPreview=False):

        self.previewWindowManager=previewWindowManager
        self.shouldMirrorPreview=shouldMirrorPreview

        self._capture=capture
        self._channel=0
        self._enteredFrame=False
        self._frame=None
        self._imageFilename=None
        self._videoFilename=None
        self._videoEncoding=None
        self._videoWriter=None

        self._startTime=None
        self._framesElapsed=int (0)
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
        if self._enteredFrame and self._frame is None:
            _,self._frame=self._capture.retrieve()
            return self._frame

    @property
    def isWritingImage(self):
        
        return self._imageFilename is not None

    @property
    def isWritingVideo(self):
        return self._videoFilename is not None

    #同步获取一帧
    def enterFrame(self):
        """Capture the next frame,if any."""

        #首先检查Pevious frame是否以及退出
        assert not self._enteredFrame,'previous enterFrame() had no matching exitFrame()'

        if self._capture is not None:
            self._enteredFrame=self._capture.grab()

    #从当前通道获取图像、估计帧速率、通过窗口管理器显示图像，执行暂停的请求，面向文件中写入图像
    def exitFrame(self):
        """Draw to the window.Write to files.Release the frame."""
        #check whether any grabbed frame is retrievable.
        #the getter may retrieve and cache the frame.
        if self.frame is None:
            self._enteredFrame=False
            return

        #update the FPS estimate and related variables.
        if self._framesElapsed==0:
            self._startTime=time.time()
        else:
            timeElapsed=time.time()-self._starTime
        self._framesElapsed+=1

        #draw to the window,if any.
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame=numpy.fliplr(self._frame).copy
                self.previewWindowManager.show(self._frame)

            else:
                self.previewWindowManager.show(self._frame)

        #write to the image file,if any.
        if self.isWritingImage:
            cv2.imwrite(self._imageFilename,self._frame)
            self._imageFilename=None

        #write to the video file,if any
        self._writeVideoFrame()

        #release the frame
        self._frame=None
        self._enteredFrame=False

    #其他文件写入的方法
   # '''
    def writeImage(self,filename):
        """Write the next exited frame to an image file."""
        self._imageFilename=filename

    def startWritingVideo(self,filename,encoding=cv2.VideoWriter_fourcc('I','4','2','0')):
        """start writing exited frames to a video file."""
        self._videoFilename=filename
        self._videoEncoding=encoding

    def stopWritingVideo(self):
        """stop Writing exited frames to a video file."""
        self._videoFilename=None
        self._videoEncoding=None
        self._videoWriter=None

    def _writeVideoFrame(self):

        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps=self._capture.get(cv2.CAP_PROP_FPS)
            if fps==0.0:
                if self._framesElapsed<20:
                    #the capture's FPS is unknown so use an estimate
                    #estimate is more stable.
                    return
                else:
                    fps=self._fpsEstimate
            size=(int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self._videoWriter.write(self._frame)
#'''

class WindowManager(object):

    def __init__(self,windowName,keypressCallback=None):
        self.keypressCallback=keypressCallback

        self._windowName=windowName
        self._isWindowCreated=False

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated=True

    def show (self,frame):
        cv2.imshow(self._windowName,frame)

    def destroyWindow(self):
        cv2.destroywindow(self._windowName)
        self._isWindowCreated=False

    def processEvents(self):
        keycode=cv2.waitKey(1)
        if self.keypressCallback is not None and keycode!=-1:
            #discard any non_ascii info encoded by GTK.
            keycode &= 0xFF
            self.keypressCallback(keycode)
        

        
