from django.dispatch import Signal
add_factory = Signal()
add_kwargs =  Signal()
add_data_factory = Signal()
create_permission_allowed = Signal()
delete_permission_allowed = Signal()
update_permission_allowed = Signal()
retrieve_permission_allowed = Signal()
get_retrieve_id_obj = Signal()
get_specfics_module = Signal()

get_parent_obj = Signal()