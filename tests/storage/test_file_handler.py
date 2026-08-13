from cipher.storage.file_handler import FileHandler
from cipher.models.text import Text, RotType, Status
from cipher.exceptions import FileHandlerError
import pytest

def test_save_file_happy_path(tmp_path):
    test_obj_1 = Text("test_name", RotType.ROT13, Status.ENCRYPTED)
    test_path =  tmp_path/"entries.json"
    handler = FileHandler()
    handler.save(str(test_path), [test_obj_1])
    file_read = handler.read(str(test_path))

    assert [test_obj_1] == file_read

def test_save_directory(tmp_path):
    test_obj_11 = Text("test_name", RotType.ROT13, Status.ENCRYPTED)
    test_path = tmp_path
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.save(str(test_path), [test_obj_11])

def test_save_invalid_json(tmp_path):
    test_path = tmp_path / "test_save.json"
    test_content = '[{"text": "blablabla", "rot_type": "rot13, "status": "encrypted"]'
    test_path.write_text(test_content, encoding="utf-8")
    test_obj_22 = Text("test_name", RotType.ROT13, Status.ENCRYPTED)
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.save(str(test_path), [test_obj_22])

def test_correct_json_not_list(tmp_path):
    test_path = tmp_path / "test_not_list.json"
    test_content = '{"text": "blablabla", "rot_type": "rot13", "status": "encrypted"}'
    test_path.write_text(test_content, encoding="utf-8")
    test_obj_22 = Text("test_object", RotType.ROT13, Status.ENCRYPTED)
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.save(str(test_path), [test_obj_22])

def test_read_returns_enum_types(tmp_path):
    test_obj_2 = Text("test_second", RotType.ROT13, Status.ENCRYPTED)
    test_path = tmp_path/"entries_second.json"
    handler = FileHandler()
    handler.save(str(test_path), [test_obj_2])
    file_read = handler.read(str(test_path))

    assert isinstance(file_read[0].rot_type, RotType)
    assert isinstance(file_read[0].status, Status)

def test_read_returns_cracked_rot_type(tmp_path):
    test_path = tmp_path/"test_third.json"
    test_content = '[{"text": "blablabla", "rot_type": "rot99", "status": "encrypted"}]'
    test_path.write_text(test_content, encoding="utf-8")
    handler = FileHandler()


    with pytest.raises(FileHandlerError):
        handler.read(str(test_path))

def test_append_to_file_and_check_the_order(tmp_path):
    test_obj_3 = Text("test_text", RotType.ROT47, Status.DECRYPTED)
    test_path = tmp_path/"test_fourth.json"
    handler = FileHandler()
    handler.save(str(test_path), [test_obj_3])
    test_obj_4 = Text("test_test", RotType.ROT13, Status.ENCRYPTED)
    handler.save(str(test_path), [test_obj_4])
    file_read = handler.read(str(test_path))

    assert file_read[0] == test_obj_3
    assert file_read[1] == test_obj_4
    assert len(file_read) == 2

def test_read_directory(tmp_path):
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.read(str(tmp_path))

def test_read_no_file(tmp_path):
    test_path = tmp_path/"fake_file.json"
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.read(str(test_path))

def test_read_missing_key(tmp_path):
    test_path = tmp_path / "test_five.json"
    test_content = '[{"text": "blablabla", "status": "encrypted"}]'
    test_path.write_text(test_content, encoding="utf-8")
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.read(str(test_path))

def test_invalid_json(tmp_path):
    test_path = tmp_path / "test_six.json"
    test_content = '[{"text": "blablabla", "rot_type": "rot13, "status": "encrypted"]'
    test_path.write_text(test_content, encoding="utf-8")
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.read(str(test_path))

def test_polish_char(tmp_path):
    test_path = tmp_path / "test_seven.json"
    test_obj_5 = Text("żźćńóąę", RotType.ROT47, Status.DECRYPTED)
    handler = FileHandler()
    handler.save(str(test_path), [test_obj_5])

    read_data = test_path.read_text(encoding="utf-8")

    assert "żźćńóąę" in read_data

def test_read_root_not_list(tmp_path):
    test_path = tmp_path / "test_not_list.json"
    test_content = '{"text": "blablabla", "rot_type": "rot13", "status": "encrypted"}'
    test_path.write_text(test_content, encoding="utf-8")
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.read(str(test_path))

def test_read_entry_not_dict(tmp_path):
    test_path = tmp_path / "test_entry_not_dict.json"
    test_content = '[1,2,3]'
    test_path.write_text(test_content, encoding="utf-8")
    handler = FileHandler()

    with pytest.raises(FileHandlerError):
        handler.read(str(test_path))