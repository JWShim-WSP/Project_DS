from .models import Sale, Position
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Sale.positions.through)
def calculate_total_price(sender, instance, action, **kwargs):
    
    # print(action) to find out what actions are there.
    
    total_net_price = 0
    total_net_profit = 0
    delivery_completed = True

    if action == 'post_add' or action == 'post_remove':
        for item in instance.get_positions():
            total_net_price += item.net_price 
            # profit comes from "the income - the total cost of purchase"
            total_net_profit += item.net_profit
            if item.inventory_status == False:
                delivery_completed = False
    
    instance.total_net_price = total_net_price # of sales
    instance.total_net_profit = total_net_profit # of sales
    total_sales_cost = instance.delivery_cost + instance.extra_cost
    instance.final_profit = total_net_profit - total_sales_cost
    instance.delivery_completed = delivery_completed
    instance.save()

    qs = instance.positions.all() # position_sold status update
    for position in qs:
        if position.position_sold == False:
            position.position_sold = True # regardless of inventory_status, all positions will be marked as 'sold_out'
            position.save(update_fields=['position_sold'])
            # this will signal to Product of Position Change (post_save)

