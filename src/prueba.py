#
# Ref: http://linuxtv.org/downloads/v4l-dvb-apis/
#      http://jayrambhia.com/blog/capture-v4l2/
#

import v4l2
import fcntl


class WebCam(object):
    def __init__(self, *args, **kwargs):
        self._camara = '/dev/video0'
        self._fd = None
        self._controles = []

    def _abrir(self):
        self._fd = open(self._camara, 'rw')

    def _cerrar(self):
        if isinstance(self._fd, file):
            self._fd.close()

    def camaras(self):
        pass

    def controles(self):
        queryctrl = v4l2.v4l2_queryctrl(v4l2.V4L2_CID_BASE)

        while queryctrl.id < v4l2.V4L2_CID_LASTP1:
            try:
                ioctl(self._fd, v4l2.VIDIOC_QUERYCTRL, queryctrl)
            except IOError, e:
                assert e.errno == errno.EINVAL
                queryctrl.id += 1
                continue

            print queryctrl.name
            yield queryctrl
            queryctrl = v4l2.v4l2_queryctrl(queryctrl.id + 1)

        print '---'

        queryctrl.id = v4l2.V4L2_CID_PRIVATE_BASE
        while True:
            try:
                ioctl(self._fd, v4l2.VIDIOC_QUERYCTRL, queryctrl)
            except IOError, e:
                assert e.errno == errno.EINVAL
                break
            print queryctrl.name
            yield queryctrl
            queryctrl = v4l2.v4l2_queryctrl(queryctrl.id + 1)


#
#vd = open('/dev/video0', 'rw')
#
#cp = v4l2.v4l2_capability()
#fcntl.ioctl(vd, v4l2.VIDIOC_QUERYCAP, cp)
#
#print cp.driver
#print cp.card
#print cp.bus_info
#print cp.version
#print cp.capabilities
#print cp.reserved
#
#fmt = v4l2.v4l2_format()
#fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
#fmt.fmt.pix.width = 1024
#fmt.fmt.pix.height = 768
#fmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_MJPEG
#fmt.fmt.pix.field = v4l2.V4L2_FIELD_NONE
#
#fcntl.ioctl(vd, v4l2.VIDIOC_TRY_FMT, fmt)
#
#print fmt.fmt.pix.width
#print fmt.fmt.pix.height
#
