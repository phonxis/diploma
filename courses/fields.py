from django.db import models
from django.core.exceptions import ObjectDoesNotExist

'''
@for_fields - относительно какого элемента будет происходить сортировка
'''
class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # проверка того, было ли уже задано значение для этого экземпляра
        if getattr(model_instance, self.attname) is None:
            try:
                # получаем все объекты из модели
                queryset = self.model.objects.all()
                if self.for_fields:
                    # фильтрация объектов, по course или module
                    query = {field: getattr(model_instance, field)
                             for field in self.for_fields}
                    queryset = queryset.filter(**query)
                # получаем последний объект с найвысшим order
                last_item = queryset.latest(self.attname)
                # текущему объекту повышаем order
                value = last_item.order + 1
            except ObjectDoesNotExist:
                # если не возможно получить последний объект
                # то текущий элемент будет первым в сортировке
                value = 0
            # задание значения полю
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)
