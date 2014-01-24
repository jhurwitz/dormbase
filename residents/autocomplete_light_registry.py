import autocomplete_light

from residents.models import Resident

autocomplete_light.register(
    Resident,
    autocomplete_light.AutocompleteModelTemplate,
    choice_template='residents/resident_choice.html',
    search_fields=('user__username', 'user__first_name', 'user__last_name'),
    name="ResidentAutocomplete")
