from cipher.core.buffer import Buffer
from cipher.models.text import Text, RotType, Status


def test_add_preserves_order():
    buffer = Buffer()
    first = Text("first_text", RotType.ROT13, Status.ENCRYPTED)
    second = Text("second_text", RotType.ROT47, Status.ENCRYPTED)
    buffer.add(first)
    buffer.add(second)

    assert buffer.entries == [first, second]


def test_new_buffer_is_empty():
    buffer = Buffer()

    assert buffer.entries == []


def test_clearing_entries_does_not_clear_buffer():
    buffer = Buffer()
    obj = Text("new_text", RotType.ROT13, Status.DECRYPTED)
    buffer.add(obj)
    entries_list = buffer.entries
    entries_list.clear()

    assert len(buffer.entries) == 1
    assert obj in buffer.entries

