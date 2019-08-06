from django.db import models
from django_fsm import FSMFieldMixin as BaseFSMFieldMixin, TransitionNotAllowed, transition
from django_fsm.signals import pre_transition, post_transition


class FSMFieldMixin(BaseFSMFieldMixin):
    def change_state(self, instance, method, *args, **kwargs):
        meta = method._django_fsm
        method_name = method.__name__
        current_state = self.get_state(instance)

        if not meta.has_transition(current_state):
            raise TransitionNotAllowed(
                "Can't switch from state '{0}' using method '{1}'".format(current_state, method_name),
                object=instance,
                method=method,
            )
        if not meta.conditions_met(instance, current_state):
            raise TransitionNotAllowed(
                "Transition conditions have not been met for method '{0}'".format(method_name),
                object=instance,
                method=method,
            )

        next_state = meta.next_state(current_state)

        signal_kwargs = {
            'sender': instance.__class__,
            'instance': instance,
            'name': method_name,
            'field': meta.field,
            'source': current_state,
            'target': next_state,
            'method_args': args,
            'method_kwargs': kwargs,
        }

        pre_transition.send(**signal_kwargs)

        # Add states to func kwargs
        kwargs['fsm_current_state'] = current_state
        kwargs['fsm_next_state'] = next_state

        try:
            result = method(instance, *args, **kwargs)
            if next_state is not None:
                if hasattr(next_state, 'get_state'):
                    next_state = next_state.get_state(instance, transition, result, args=args, kwargs=kwargs)
                    signal_kwargs['target'] = next_state
                self.set_proxy(instance, next_state)
                self.set_state(instance, next_state)
        except Exception as exc:
            exception_state = meta.exception_state(current_state)
            if exception_state:
                self.set_proxy(instance, exception_state)
                self.set_state(instance, exception_state)
                signal_kwargs['target'] = exception_state
                signal_kwargs['exception'] = exc
                post_transition.send(**signal_kwargs)
            raise
        else:
            post_transition.send(**signal_kwargs)

        return result


class FSMField(FSMFieldMixin, models.CharField):
    """
    State Machine support for Django model as CharField
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 50)
        super(FSMField, self).__init__(*args, **kwargs)
