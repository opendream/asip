from sorl.thumbnail.engines.pil_engine import Engine

try:
    from PIL import Image
except ImportError:
    import Image

class CommonEngine(Engine):
    def _padding(self, image, geometry, options):

        x_image, y_image = self.get_image_size(image)
        left = int((geometry[0] - x_image) / 2)
        top = int((geometry[1] - y_image) / 2)
        color = options.get('padding_color')

        padding = options.get('padding')

        if type(padding) is int:
            geometry = list(geometry)
            geometry[0] += padding*2
            geometry[1] += padding*2

            left += padding
            top += padding

        im = Image.new(image.mode, geometry, color)
        im.paste(image, (left, top))
        return im