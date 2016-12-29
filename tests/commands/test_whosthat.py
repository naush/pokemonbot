import pytest
from unittest import mock

from pokemonbot.commands import whosthat

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_new_game(mocked_save, mocked_load):
    mocked_load.side_effect = [{'pokemons':[{'name':'pikachu'}]}, {}]
    assert whosthat.respond('U21EYJH0T', "who's that pokemon") == 'Who is :pokemon-pikachu:?'

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_save_choice(mocked_save, mocked_load):
    mocked_load.side_effect = [{'pokemons':[{'name':'pikachu'}]}, {}]
    whosthat.respond('U21EYJH0T', whosthat.COMMAND)
    mocked_save.assert_called_with({'U21EYJH0T':{'command':whosthat.COMMAND, 'context':{'pokemon':'pikachu'}}})

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_guess_wrong(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu'}}}
    ]
    assert whosthat.respond('U21EYJH0T', "raichu") == 'Nope.'

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_guess_right(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu'}}}
    ]
    assert whosthat.respond('U21EYJH0T', "pikachu") == 'You got it!'

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_clears_user_data(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu'}}}
    ]
    whosthat.respond('U21EYJH0T', "pikachu")
    mocked_save.assert_called_with({'U21EYJH0T':{}})
