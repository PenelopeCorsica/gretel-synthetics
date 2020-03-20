import os
import pytest
from unittest.mock import patch, Mock

from gretel_synthetics.train import train_rnn, train_tokenizer


def test_create_vocab(global_local_config):
    check = create_vocab(global_local_config)
    assert len(check) == 34
    global_local_config.max_chars = 8
    check = create_vocab(global_local_config)
    assert len(check) == 8


@patch('gretel_synthetics.train.build_sequential_model')
@patch('pickle.dump')
@patch('gretel_synthetics.train.read_training_data')
@patch('gretel_synthetics.train.open')
def test_train_rnn(_open, trng, pickle, model, smol_data, global_local_config):
    mock_model = Mock()
    model.return_value = mock_model
    trng.return_value = smol_data
    train_rnn(global_local_config)

    model.assert_called_with(
        vocab_size=34,
        batch_size=global_local_config.batch_size,
        store=global_local_config
    )

    mock_model.fit.assert_called

    # let's rerun with a much smaller max_chars value
    mock_model = Mock()
    model.return_value = mock_model
    trng.return_value = smol_data
    global_local_config.max_chars = 3
    train_rnn(global_local_config)

    model.assert_called_with(
        vocab_size=3,
        batch_size=global_local_config.batch_size,
        store=global_local_config
    )

    mock_model.fit.assert_called
    