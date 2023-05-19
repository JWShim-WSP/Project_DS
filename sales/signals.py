from .models import Sale
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=Sale.positions.through)
def calculate_total_price(sender, instance, action, **kwargs):
    
    # print(action) to find out what actions are there.
    
    total_net_price = 0
    total_added_price = 0
    total_net_price_KRW = 0
    total_added_price_KRW = 0

    if action == 'post_add' or action == 'post_remove':
        for item in instance.get_positions():
            total_net_price += item.net_price
            total_added_price += item.added_price
            total_net_price_KRW += item.net_price_KRW
            total_added_price_KRW += item.added_price_KRW
    
    instance.total_net_price = total_net_price
    instance.total_added_price = total_added_price
    instance.total_net_price_KRW = total_net_price_KRW
    instance.total_added_price_KRW = total_added_price_KRW
    instance.save()


