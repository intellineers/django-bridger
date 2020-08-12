from django.db import models
from bridger.utils.colors import WBColor
from bridger.utils.enum import ChoiceEnum
def get_and_update_or_create(model, filter_params, defaults):
    """ get or create with default values applied to existing instances

    {model}.objects.get_or_create(*{filter_params}, defaults={defaults})
    
    Arguments:
        model {django.db.models.Model} -- The model the queryset gets applied to
        filter_params {dict} -- The parameters that the queryset gets filter against
        defaults {dict} -- The default values that will be applied to the instance (create, update)
    
    Returns:
        django.db.models.Model -- The created/updated instance of the model
    """

    instance, created = model.objects.get_or_create(**filter_params, defaults=defaults)
    if not created:
        for attr, value in defaults.items():
            setattr(instance, attr, value)
        instance.save()
    return instance


class NoGroupBySubquery(models.Subquery):
    """ Same as the default django subquery, however does not perform a group by """

    def get_group_by_cols(self):
        return []


class NoGroupByExpressionWrapper(models.ExpressionWrapper):
    def get_group_by_cols(self):
        return []


class ComplexToStringMixin(models.Model):
    """ Mixin that allows to store a complex to string method in the database
    """

    class Meta:
        abstract = True

    computed_str = models.CharField(max_length=512, null=True, blank=True)

    def compute_str(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        self.computed_str = self.compute_str()
        super().save(*args, **kwargs)


class LabelKeyMixin:
    @classmethod
    def get_label_key(cls):
        if hasattr(cls, "LABEL_KEY"):
            return cls.LABEL_KEY
        raise AssertionError(
            f"You need to implement the get_label_key method in the class {cls} or remove the LabelKeyMixin from {cls}."
        )

class Status(ChoiceEnum):
    PENDING = 'Pending'
    DENIED = 'Denied'
    APPROVED = 'Approved'
    @classmethod
    def get_color_map(cls):
        colors = [
            WBColor.YELLOW_LIGHT.value,
            WBColor.RED_LIGHT.value,
            WBColor.GREEN_LIGHT.value
        ]
        return [choice for choice in zip(cls, colors)]