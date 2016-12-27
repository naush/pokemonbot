import pytest
from unittest import mock

from pokemonbot.commands import whois

def test_whois_standard_response():
    assert whois.respond('John', 'hello') == 'Do you want to know what kind of pokemon is John? Ask me *who is* John.'

@mock.patch('random.choice')
def test_whois_random_pokemon(mocked_random_choice):
    mocked_random_choice.return_value = 'pikachu'
    assert whois.respond('John', 'who is John') == 'John is a :pokemon-pikachu:!'

@mock.patch('random.choice')
def test_whois_strips_non_alphanumerical_character_from_user_name(mocked_random_choice):
    mocked_random_choice.return_value = 'pikachu'
    assert whois.respond('John', 'who is Mary?') == 'Mary is a :pokemon-pikachu:!'
