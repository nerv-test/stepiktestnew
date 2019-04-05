from django.dispatch import Signal

review_added = Signal(providing_args=['work'])

image_added = Signal(providing_args=['work'])
