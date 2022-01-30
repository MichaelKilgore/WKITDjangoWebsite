from django.contrib.admin import AdminSite
class MyAdminSite(AdminSite):
	pass


# Then register your models with the new admin site
site = MyAdminSite()

# Register your models here.
#site.register(Shop,ShopAdmin)
#site.register(Product,ProductAdmin)
