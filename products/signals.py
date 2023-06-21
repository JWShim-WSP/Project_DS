from .models import Purchase
from sales.models import Position
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# The 'signal' is a communication between 'sender' and 'receiver' applications. 
# The sender will signal to the receiver to create its own automatically.
# In this case, User creation will be the sender to Profile to create the profile of the user automatically.

# The receiver decorator (first argument is the signal)
@receiver(post_save, sender=Purchase)
def post_save_update_product_info_from_Purchase(sender, instance, **kwargs):
    # 'sender' is the class of django.contrib.auto.models.User (e.g., the model)
    # 'instance' is the user (object) created or updated to have a profile matched automatically
    # 'created', it signals to this to create a profile. Therefore, 'created' must be checked to create the profile only once.
    if instance.status == "Stocked": # Finally the product is moved in the inventory
        product_inventory = 0
        total_quantity = 0
        total_net_price_KRW = 0
        total_added_price_KRW = 0
        total_ex_rate_to_KRW = 0
        total_unit_price = 0

        qs = Purchase.objects.filter(product=instance.product)
        loop_count = 0

        for purchase in qs:
            if purchase.status == "Stocked":
                loop_count += 1
                product_inventory += purchase.quantity
                total_quantity += purchase.quantity
                total_net_price_KRW += purchase.net_price_KRW
                total_added_price_KRW += purchase.added_price_KRW
                total_ex_rate_to_KRW += purchase.ex_rate_to_KRW
                total_unit_price += purchase.unit_price

        if loop_count: # do not divide by 0 in any case
            average_ex_rate_to_KRW = total_ex_rate_to_KRW / loop_count
        else:
            average_ex_rate_to_KRW = instance.ex_rate_to_KRW

        instance.product.total_quantity = total_quantity
        instance.product.total_net_price_KRW = total_net_price_KRW
        instance.product.total_added_price_KRW = total_added_price_KRW
        instance.product.average_ex_rate_to_KRW = average_ex_rate_to_KRW

        if total_quantity: # do not divide by 0 in any case
            instance.product.average_unit_price_KRW = total_added_price_KRW / total_quantity
        else:
            instance.product.average_unit_price_KRW = total_added_price_KRW

        # let's adjust the 'inventory' with 'Sales Positions' too.
        qs = Position.objects.filter(product=instance.product)
        for position in qs:
            if position.inventory_status == 'Yes': # this will be saled soon.
                if product_inventory >= position.quantity:
                    product_inventory -= position.quantity
                else:
                    pass # system error!!!!
            else: # sales position was blocked due to the lack of inventory. This should be updated if it is filled by the Purchase.
                if product_inventory >= position.quantity:
                    product_inventory -= position.quantity
                    position.inventory_status = "Yes" # now it is OK to go
                    position.save()
        # Finally, we have the updated 'product' information including 'inventory'
        instance.product.inventory = product_inventory
        instance.product.save()

# secondly, go to 'apps.py' to configure the Profile app to receive the signal
# finally, go to '__init__.py' to initialize the configuration of the signal communication

# When Sales_Positioning happened, the inventory should be updated accordingly.
@receiver(post_save, sender=Position)
def post_save_update_product_info_from_Position(sender, instance, **kwargs):
    if instance.inventory_status == "Yes": # We have inventory update from Sales positioning

        product_inventory = 0

        qs = Purchase.objects.filter(product=instance.product)
        for purchase in qs:
            if purchase.status == "Stocked":            
                product_inventory += purchase.quantity

        # let's adjust the 'inventory' with 'Sales Positions' too.
        qs = Position.objects.filter(product=instance.product)
        for position in qs:
            if position.inventory_status == 'Yes': # this will be saled soon.
                if product_inventory >= position.quantity:
                    product_inventory -= position.quantity
                else:
                    pass # system error!!!
        
        instance.product.inventory = product_inventory
        # Finally, we have the updated 'product' information including 'inventory'
        instance.product.save()
