# myapp/management/commands/migrate_products.py

import os
from django.core.management.base import BaseCommand
from PIL import Image
from diceandtiles.drf.models import Product, Productweb

class Command(BaseCommand):
    help = 'Migrate data from Product to Productweb'

    def handle(self, *args, **options):
        products = Product.objects.all()

        for product in products:
            # Create a new Productweb instance
            product_web = Productweb(
                bggid=product.bggid,
                name=product.name,
                description=product.description,
                is_active=product.is_active,
                slug=product.slug,
                min_players=product.min_players,
                max_players=product.max_players,
                image_url=product.image_url,
                thumbnail_url=product.thumbnail_url,
                # Change the file extensions in the new instance
                image1=self.change_file_extension(product.image1),
                image2=self.change_file_extension(product.image2),
                image3=self.change_file_extension(product.image3),
                image4=self.change_file_extension(product.image4),
                image5=self.change_file_extension(product.image5),
                thumbnail=self.change_file_extension(product.thumbnail),
            )

            # Save the new Productweb instance
            product_web.save()

    def change_file_extension(self, file_field):
        if file_field:
            # Get the current file path
            current_path = str(file_field.path)

            # Change the file extension to .webp
            new_path = current_path.replace('.jpg', '.webp')

            # Update the file field with the new path
            file_field.name = new_path

        return file_field