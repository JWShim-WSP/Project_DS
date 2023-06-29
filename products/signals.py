from .models import Purchase
from sales.models import Position
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# The 'signal' is a communication between 'sender' and 'receiver' applications. 
# The sender will signal to the receiver to create its own automatically.
# In this case, User creation will be the sender to Profile to create the profile of the user automatically.
# secondly, go to 'apps.py' to configure the Profile app to receive the signal
# finally, go to '__init__.py' to initialize the configuration of the signal communication

# The receiver decorator (first argument is the signal)
@receiver(post_save, sender=Purchase)
def post_save_update_product_info_from_Purchase(sender, instance, **kwargs):
    # 'sender' is the class of django.contrib.auto.models.User (e.g., the model)
    # 'instance' is the user (object) created or updated to have a profile matched automatically
    # 'created', it signals to this to create a profile. Therefore, 'created' must be checked to create the profile only once.
    product_inventory = 0
    total_quantity = 0
    total_net_price_KRW = 0
    total_added_price_KRW = 0
    total_ex_rate_to_KRW = 0
    total_unit_price = 0

    purchase_qs = Purchase.objects.filter(product=instance.product)
    loop_count = 0

    for purchase in purchase_qs:
        loop_count += 1

        if purchase.status == "Stocked":
            product_inventory += purchase.quantity
            total_quantity += purchase.quantity

        total_net_price_KRW += purchase.net_price_KRW
        total_added_price_KRW += purchase.added_price_KRW
        total_ex_rate_to_KRW += purchase.ex_rate_to_KRW
        total_unit_price += purchase.unit_price

    if loop_count: # do not divide by 0 in any case
        average_ex_rate_to_KRW = total_ex_rate_to_KRW / loop_count
        instance.product.average_unit_price = total_unit_price / loop_count
        instance.product.average_unit_price_KRW = (total_unit_price / loop_count) * average_ex_rate_to_KRW
    else:
        instance.error # this should not happen

    instance.product.total_quantity = total_quantity
    instance.product.total_net_price_KRW = total_net_price_KRW
    instance.product.total_added_price_KRW = total_added_price_KRW
    instance.product.average_ex_rate_to_KRW = average_ex_rate_to_KRW

    # let's adjust the 'inventory' with 'Sales Positions' too.
    position_qs = Position.objects.filter(product=instance.product, inventory_status=True)
    if position_qs: # if we have any sales position for the product, then inventory should be calculated more to subtract.
        for position in position_qs:
            if product_inventory >= position.quantity:
                product_inventory -= position.quantity
            else: # system error
                position.error = "Should not happen!!!"

    # Finally, we update the product's inventory here
    instance.product.inventory = product_inventory
    instance.product.save()

    # let's see if there is any sales position pending
    position_qs = Position.objects.filter(product=instance.product, inventory_status=False, position_sold=False)
    if position_qs: # yes, we have pending sales position.
        for position in position_qs:
            if product_inventory >= position.quantity:
                product_inventory -= position.quantity
                # the postion.save() below will signal to update the product inventory!!! Therefore, don't try to save the product.inventory here!                   
                position.inventory_status = True
                position.save(update_fields=['inventory_status'])
            else: # system error
                position.error = "Should not happen!!!"

# When Sales_Positioning happened, the inventory should be updated accordingly.
@receiver(post_save, sender=Position)
def post_save_update_product_info_from_Position(sender, instance, **kwargs):
    if (instance.inventory_status == True) and (instance.position_sold == False): # We have inventory update from Sales positioning
        product_inventory = instance.product.inventory
        # let's adjust the 'inventory' with the instance of 'Sales Position'.
        if product_inventory >= instance.quantity:
            product_inventory -= instance.quantity
        else:
            product_inventory.messages = "error" # system error
        
        instance.product.inventory = product_inventory
        # Finally, we have the updated 'product' information including 'inventory'
        instance.product.save(update_fields=['inventory'])
