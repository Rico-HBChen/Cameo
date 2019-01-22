import cv2
import numpy
import utils

def strokeEdges(src,dst,blurKaize=7,edgeKsize=5):
    if blurKsize >=3:
        #中值滤波mediaBlur(src,blurksize)，将图像src用长宽为blurksize的像素区域中间的值代替周围值
        blurredSrc=cv2.medianBlur(src,blurKsize)

        #颜色转换将BGR转换为GRAY
        graySrc=cv2.cvtColor (blurredSrc,cv2.COLOR_BGR2GRAY)
    else:
        graySrc=cv2.cvtColor(src,cv2.COLOR_BGR2GAY)
    cv2.Laplacian(graySrc,cv2.CV_8U,graySrc,ksize=edgeKsize)
    normalizedInverseAlpha=(1.0/255)*(255-graySrc)
    channels=cv2.split(src)
    for channel in channels:
        channel[:]=channel*normalizedInverseAlpha
    cv2.merge(channels,dst)

#卷积滤波器
class VConvolutionFilter(object):
    """A filter that applies a convolution to V (or all of BGR)."""
    def __init__ (self,kernel):
        self._kernel=kernel

    def apply(self,src,dst):
        """apply the filter with a bgr or gray source/destination."""
        cv2.filter2D(src,-1,self._kernel,dst)

#锐化滤波器
class SharpenFilter(VConvolutionFilter):
    """a sharpen filter with a 1-pixel radius."""

    def __init__(self):
        kernel=numpy.array([[-1,-1,-1],
                                         [-1,9,-1],
                                         [-1,-1,-1]])
        VConvolutionFilter.__init__(self,kernel)

#边缘检测
class FindEdgesFilter(VConvolutionFilter):
    """an edge_finding filter with a 1-pixel radius."""

    def __init__(self):
        kernel=numpy.array([[-1,-1,-1],
                                         [-1,8,-1],
                                         [-1,-1,-1]])
        VConvolutionFilter.__init__(self,kernel)

#模糊滤波器
class BlurFilter(VConvolutionFilter):

    def __init__(self):
        kernel=numpy.array([[0.04,0.04,0.04,0.04,0.04],
                                     [0.04,0.04,0.04,0.04,0.04],
                                     [0.04,0.04,0.04,0.04,0.04],
                                     [0.04,0.04,0.04,0.04,0.04],
                                     [0.04,0.04,0.04,0.04,0.04]])
        VConvolutionFilter.__init__(self.kernel)

#非对称核特殊效果
class EmbossFilter(VConvolutionFilter):
    """an emboss filter with a 1-pixel radius."""

    def __init__(self):
        kernel=numpy.array([[-2,-1,0],
                                         [-1,1-1],
                                         [0,1,2]])
        VConvolutionFilter.__init__(self,kernel)
