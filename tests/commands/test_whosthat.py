import pytest
from unittest import mock

from pokemonbot.commands import whosthat

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_new_game(mocked_save, mocked_load):
    mocked_load.side_effect = [{'pokemons':[{'name':'pikachu'}]}, {}]
    assert whosthat.respond('U21EYJH0T', "who's that pokemon") == 'Who is that pokemon? :pokemon-pikachu:'

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_save_choice(mocked_save, mocked_load):
    mocked_load.side_effect = [{'pokemons':[{'name':'pikachu'}]}, {}]
    whosthat.respond('U21EYJH0T', whosthat.COMMAND)
    mocked_save.assert_called_with({'U21EYJH0T':{'command':whosthat.COMMAND, 'context':{'pokemon':'pikachu','attempt':0}}})

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_guess_wrong(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu','attempt':0}}}
    ]
    assert whosthat.respond('U21EYJH0T', "raichu") == 'Nope.'

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_guess_wrong_again(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu','attempt':2}}},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu','attempt':3}}},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu','attempt':4}}},
    ]
    assert whosthat.respond('U21EYJH0T', "raichu") == 'Are you even a Pokémon fan?'
    assert whosthat.respond('U21EYJH0T', "pidgey") == 'Last chance.'
    assert whosthat.respond('U21EYJH0T', "rattata") == 'It’s a pikachu. Go read a Pokédex.'

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_guess_wrong_again(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu','attempt':3}}}
    ]
    assert whosthat.respond('U21EYJH0T', "raichu") == 'Last chance.'

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_guess_right(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu','attempt':0}}}
    ]
    assert whosthat.respond('U21EYJH0T', "pikachu") == 'You got it!'

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_clears_user_data(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'context':{'pokemon':'pikachu','attempt':0}}}
    ]
    whosthat.respond('U21EYJH0T', "pikachu")
    mocked_save.assert_called_with({'U21EYJH0T':{}})

@mock.patch('pokemonbot.commands.whosthat.load')
@mock.patch('pokemonbot.commands.whosthat.save')
def test_whosthat_counts_number_of_attemps(mocked_save, mocked_load):
    mocked_load.side_effect = [
        {'pokemons':[{'name':'pikachu'}]},
        {'U21EYJH0T':{'command':whosthat.COMMAND, 'context':{'pokemon':'pikachu','attempt':0}}}
    ]
    whosthat.respond('U21EYJH0T', "pidgey")
    mocked_save.assert_called_with({'U21EYJH0T':{'command':whosthat.COMMAND, 'context':{'pokemon':'pikachu','attempt':1}}})
