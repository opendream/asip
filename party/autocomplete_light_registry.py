import autocomplete_light
from party.functions import portfolio_render_reference
from party.models import Portfolio


class PortfolioAutocomplete(autocomplete_light.AutocompleteModelBase):

    choices = Portfolio.objects.filter().order_by('-ordering')
    search_fields = ['title']

    display_edit_link = True
    field_name = 'portfolios'

    def choice_label(self, choice):

        return portfolio_render_reference(choice, self.display_edit_link, self.field_name)

    def choice_html(self, choice):

        return self.choice_html_format % (
            self.choice_value(choice),
            self.choice_label(choice))

autocomplete_light.register(Portfolio, PortfolioAutocomplete)

