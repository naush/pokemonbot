from pokemonbot.commands import whois
import pytest

def test_whois():
    assert whois.respond('John', 'hello') == 'Do you want to know what kind of pokemon is John? Ask me *who is* John.'
