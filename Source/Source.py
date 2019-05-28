from __future__ import print_function

import argparse
import os
import sys

import djvu.dllpath
djvu.dllpath.set_dll_search_path()
import djvu.decode
import numpy
from PIL import Image

djvu_pixel_format = djvu.decode.PixelFormatGrey()
djvu_pixel_format.rows_top_to_bottom = 1
djvu_pixel_format.y_top_to_bottom = 0

class Context(djvu.decode.Context):

    def handle_message(self, message):
        if isinstance(message, djvu.decode.ErrorMessage):
            print(message, file=sys.stderr)
            os._exit(1)

    def process(self, first_djvu_path, second_djvu_path):
        first_document = self.new_document(djvu.decode.FileURI(first_djvu_path))
        first_document.decoding_job.wait()
        first_page = first_document.pages[0]
        first_page_job = first_page.decode(wait=True)
        
        second_document = self.new_document(djvu.decode.FileURI(second_djvu_path))
        second_document.decoding_job.wait()
        second_page = second_document.pages[0]
        second_page_job = second_page.decode(wait=True)

        max_width = max([first_page_job.width, second_page_job.width])
        max_height = max([first_page_job.height, second_page_job.height])
        print(str(max_width) + 'x' + str(max_height))
        
        documents = [first_document, second_document]
        image_number = 0
        for document in documents:
            page = document.pages[0]
            page_job = page.decode(wait=True)
            width, height = page_job.size
            if width < max_width or height < max_height:
                rect = (0, 0, width, height)
                document_image_buffer = numpy.zeros((height, width), dtype=numpy.uint8)
                page_job.render(djvu.decode.RENDER_BACKGROUND, rect, rect, djvu_pixel_format, buffer=document_image_buffer)
                # Create black background
                black_image = numpy.zeros((max_height, max_width), numpy.uint8)
                # Copy smaller image to bigger
                start_width_index = int(round((max_width - width) / 2))
                start_height_index = int(round((max_height - height) / 2))
                for h in range (0, height):
                    for w in range (0, width):
                        black_image[h + start_height_index, w + start_width_index] = document_image_buffer[h, w]
                img = Image.fromarray(black_image, mode='L')
                img.save('Resources/output_' + str(image_number) + '.png')
            image_number += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('first_djvu_path')
    parser.add_argument('second_djvu_path')
    options = parser.parse_args()
    context = Context()
    context.process(options.first_djvu_path, options.second_djvu_path)

if __name__ == '__main__':
    main()