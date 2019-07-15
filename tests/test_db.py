import pytest
import sqlite3

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from instabot.db import DB


@pytest.fixture
def real_connection():
    return sqlite3.connect('instabot.test.sqlite')


@pytest.fixture
def reset_db(real_connection):
    real_connection.execute('DROP TABLE IF EXISTS follows')
    real_connection.commit()


@pytest.fixture
def mock_sqlite(mocker, mock_connection):
    mock_sqlite = mocker.patch('instabot.db.sqlite3')
    mock_sqlite.connect = Mock(return_value=mock_connection)
    return mock_sqlite


@pytest.fixture
def mock_connection():
    return Mock()


@pytest.fixture
def mocked_db(reset_db, mock_sqlite, mock_connection):
    database = DB('instabot.test.sqlite')
    mock_sqlite.connect.reset_mock()
    mock_connection.reset_mock()
    return database


def test_integration(reset_db, real_connection):
    # Start out with an empty database
    database = DB('instabot.test.sqlite')
    assert real_connection.execute('SELECT COUNT(*) FROM follows').fetchone()[0] == 0

    # Record one follow
    database.record_follow('12345678', 'username123')
    user_id, followed_at, unfollowed_at = real_connection.execute(
        "SELECT user_id, followed_at, unfollowed_at FROM follows").fetchone()
    assert user_id == '12345678'
    assert followed_at is not None
    assert unfollowed_at is None

    # Fetch list of follows older than 60 seconds
    real_connection.execute(
        "UPDATE follows SET followed_at = DATETIME('now', '-60 minutes') WHERE user_id = '12345678'")
    real_connection.commit()
    user_ids = database.get_followed_before(60)
    assert user_ids == ['12345678']

    # Record an unfollow
    database.record_unfollow('12345678')
    user_id, unfollowed_at = real_connection.execute(
        "SELECT user_id, unfollowed_at FROM follows WHERE user_id = '12345678'").fetchone()
    assert user_id == '12345678'
    assert unfollowed_at is not None

    # Exactly one row should have been inserted
    assert real_connection.execute('SELECT COUNT(*) FROM follows').fetchone()[0] == 1


def test_config(mock_sqlite, mock_connection):
    DB('test_filename')

    mock_sqlite.connect.assert_called_once_with('test_filename')
    mock_connection.execute.assert_called_once_with("CREATE TABLE IF NOT EXISTS 'follows' ("
                                                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                    "user_id TEXT NOT NULL, "
                                                    "username TEXT, "
                                                    "followed_at DATETIME NOT NULL, "
                                                    "unfollowed_at DATETIME)")
    mock_connection.commit.assert_called_once_with()


def test_record_follow(mocked_db, mock_connection):
    mocked_db.record_follow('user_id1234', 'test_username')
    mock_connection.execute.assert_called_once_with(
        "INSERT INTO follows(user_id, username, followed_at) VALUES (?, ?, DATETIME('now'))",
        ['user_id1234', 'test_username']
    )
    mock_connection.commit.assert_called_once_with()


def test_record_unfollow(mocked_db, mock_connection):
    mocked_db.record_unfollow('user_12345678')
    mock_connection.execute.assert_called_once_with(
        "UPDATE follows SET unfollowed_at = DATETIME('now') WHERE user_id = ?",
        ['user_12345678']
    )
    mock_connection.commit.assert_called_once_with()


def test_get_followed_before(mocked_db, mock_connection):
    mock_cursor = Mock()
    mock_cursor.fetchall = Mock(return_value=[('test_id1',), ('test_id2',)])
    mock_connection.execute.return_value = mock_cursor

    results = mocked_db.get_followed_before(120)

    assert results == ['test_id1', 'test_id2']
    expected_query = ("SELECT user_id FROM follows "
                      "WHERE unfollowed_at IS NULL "
                      "AND followed_at < DATETIME('now', '-120 seconds')")
    mock_connection.execute.assert_called_once_with(expected_query)
