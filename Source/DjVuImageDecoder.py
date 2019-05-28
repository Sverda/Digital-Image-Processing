from __future__ import print_function
import os

import djvu.dllpath
djvu.dllpath.set_dll_search_path()
import djvu.decode
import numpy

class DjVuImageDecoder(djvu.decode.Context):
    def __init__(self, djvuImagePath):
        document = self.new_document(djvu.decode.FileURI(djvuImagePath))
        document.decoding_job.wait()
        page = document.pages[0]
        pageJob = page.decode(wait=True)
        self._pageInfo = pageJob
        self.width = pageJob.width
        self.height = pageJob.height
        self.setGrayscale()

    def setGrayscale(self):
        self._djvuPixelFormat = djvu.decode.PixelFormatGrey()
        self._djvuPixelFormat.rows_top_to_bottom = 1
        self._djvuPixelFormat.y_top_to_bottom = 0
        self._arrayType = numpy.uint8

    def getSize(self):
        return self._pageInfo.size

    def getPixels(self):
        width, height = self.width, self.height
        rect = (0, 0, width, height)
        imageBuffer = numpy.zeros((height, width), self._arrayType)
        self._pageInfo.render(djvu.decode.RENDER_BACKGROUND, rect, rect, self._djvuPixelFormat, buffer=imageBuffer)
        return imageBuffer

    def handle_message(self, message):
        if isinstance(message, djvu.decode.ErrorMessage):
            print(message, file=sys.stderr)
            os._exit(1)