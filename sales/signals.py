from .models import Sale, Position
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Sale.positions.through)
def calculate_total_price(sender, instance, action, **kwargs):
    
    # print(action) to find out what actions are there.
    
    total_net_price = 0
    total_net_profit = 0

    if action == 'post_add' or action == 'post_remove':
        for item in instance.get_positions():
            total_net_price += item.net_price 
            # profit comes from "the income - the total cost of purchase"
            total_net_profit += item.net_profit
    
    instance.total_net_price = total_net_price # of sales
    instance.total_net_profit = total_net_profit # of sales
    total_sales_cost = instance.tax_cost + instance.vat_cost + instance.delivery_cost + instance.extra_cost
    instance.final_profit = total_net_profit - total_sales_cost
    instance.save()

    qs = instance.positions.all() # position_sold status update
    for position in qs:
        position.position_sold = True
        position.save()

