from django.contrib import admin
from django.core.management import call_command
from .models import Product, Comment, Profile, Vote, Fetched_Product
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile



@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','id','slug']

    actions = ['get_remote_image']

    def get_remote_image(self, request, queryset):
        for product in queryset:
            if product.image_url and not product.image1:
             try:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(product.image_url).read())
                img_temp.flush()
                for x in range (1, 6):                                       
                    getattr(product, f"image{x}").save(f"{product.pk}_image{x}.jpg", File(img_temp))
                product.save()
                print(f'Successfully downloaded and assigned JPG image for Product {product.slug}')
                self.message_user(request, f'Successfully downloaded and assigned JPG image for Product {product.slug}')
             except Exception as e:
                self.message_user(request, f'Error downloading or assigning image for Product {product.slug}: {e}', level='error')
                print(f'Error downloading or assigning image for Product {product.slug}: {e}')
            if product.thumbnail_url and not product.thumbnail:
             try:
                img_temp2 = NamedTemporaryFile(delete=True)
                img_temp2.write(urlopen(product.thumbnail_url).read())
                img_temp2.flush()                                                   
                product.thumbnail.save(f"{product.pk}_thumbnail.jpg", File(img_temp2))
                product.save()
                print(f'Successfully downloaded and assigned JPG thumbnail for Product {product.slug}')
                self.message_user(request, f'Successfully downloaded and assigned JPG thumbnail for Product {product.slug}')
             except Exception as e:
                self.message_user(request, f'Error downloading or assigning thumbnail for Product {product.slug}: {e}', level='error')
                print(f'Error downloading or assigning thumbnail for Product {product.slug}: {e}')

    get_remote_image.short_description = 'download image for product'

@admin.register(Fetched_Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','id','slug']
    
    actions = ['custom_action']

    def custom_action(self, request, queryset):
        # Call your custom command using call_command
        call_command('populatecommand')

    custom_action.short_description = 'Populate PRODUCTS table command'

@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['product','body','created_on','owner']

@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    
@admin.register(Vote)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['product','value','owner']
