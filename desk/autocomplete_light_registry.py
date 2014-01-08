import autocomplete_light
from guestlist.models import GuestlistEntry

autocomplete_light.register(
    GuestlistEntry,
    autocomplete_light.AutocompleteModelTemplate,
    choice_template='desk/guest_choice.html',
    search_fields=('username', 'name'),
    name="GuestSigninAutocomplete")
