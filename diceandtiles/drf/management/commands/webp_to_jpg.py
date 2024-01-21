# myscript.py

import os
from django.core.management.base import BaseCommand
from diceandtiles.drf.models import Product
from PIL import Image

class Command(BaseCommand):
    help = 'Change file extensions from .jpg to .webp for images in Product model'

    def handle(self, *args, **options):
        products = Product.objects.all()

        for product in products:
            # Change the file extension for each image field
            product.image1 = self.change_file_extension(product.image1)
            product.image2 = self.change_file_extension(product.image2)
            product.image3 = self.change_file_extension(product.image3)
            product.image4 = self.change_file_extension(product.image4)
            product.image5 = self.change_file_extension(product.image5)
            product.thumbnail = self.change_file_extension(product.thumbnail)

            # Save the updated product instance
            product.save()

    def change_file_extension(self, file_field):
        if file_field and file_field.name.endswith('.webp'):
            # Get the current file path
            current_path = str(file_field.path)

            # Change the file extension to .webp
            new_path = current_path.replace('.webp', '.jpg')

            file_field.name = new_path

            return new_path
        else:
            return file_field
