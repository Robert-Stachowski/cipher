import pytest
from dataclasses import FrozenInstanceError
from cipher.models.text import Text, RotType, Status


def test_text_are_created():
    obj = Text('text', RotType.ROT13, Status.ENCRYPTED)

    assert obj.text == 'text'
    assert obj.rot_type is RotType.ROT13
    assert obj.status is Status.ENCRYPTED


def test_text_are_immutable():
    obj = Text('text', RotType.ROT13, Status.ENCRYPTED)

    with pytest.raises(FrozenInstanceError):
        obj.text = 'new_text'

