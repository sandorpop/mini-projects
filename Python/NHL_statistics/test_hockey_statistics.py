import json
import pytest
from hockey_statistics import FileHandler, Player, Stats, StatsApplication


# ------------------------
# Fixtures
# ------------------------

@pytest.fixture
def sample_players():
    return [
        {
            "name": "Sidney Crosby",
            "nationality": "CAN",
            "assists": 50,
            "goals": 40,
            "penalties": 10,
            "team": "PIT",
            "games": 82
        },
        {
            "name": "Connor McDavid",
            "nationality": "CAN",
            "assists": 70,
            "goals": 60,
            "penalties": 8,
            "team": "EDM",
            "games": 80
        },
        {
            "name": "Auston Matthews",
            "nationality": "USA",
            "assists": 40,
            "goals": 55,
            "penalties": 6,
            "team": "TOR",
            "games": 78
        }
    ]


@pytest.fixture
def stats(sample_players):
    s = Stats()
    for p in sample_players:
        s.add_player(**p)
    return s


# ------------------------
# FileHandler Tests
# ------------------------

def test_filehandler_reads_valid_file(tmp_path):
    file = tmp_path / "players.json"
    data = [{"name": "Test"}]
    file.write_text(json.dumps(data))

    handler = FileHandler(file)
    result = handler.read()

    assert result == data


def test_filehandler_invalid_filename():
    handler = FileHandler("non_existent_file.json")
    with pytest.raises(ValueError):
        handler.read()


def test_filehandler_invalid_json(tmp_path):
    file = tmp_path / "invalid.json"
    file.write_text("not json")

    handler = FileHandler(file)
    with pytest.raises(json.JSONDecodeError):
        handler.read()


# ------------------------
# Player Tests
# ------------------------

def test_player_string_format():
    player = Player("Test Player", "USA", 10, 20, 5, "ABC", 50)
    result = str(player)

    assert "Test Player" in result
    assert "ABC" in result
    assert "20 + 10 =  30" in result


# ------------------------
# Stats Tests
# ------------------------

def test_add_player(stats):
    assert len(stats.all_entries()) == 3


def test_search_case_insensitive(stats):
    result = stats.search("sidney crosby")
    assert len(result) == 1
    assert result[0].name == "Sidney Crosby"


def test_players_by_team(stats):
    result = stats.players_by_team("edm")
    assert len(result) == 1
    assert result[0].team == "EDM"


def test_players_by_country(stats):
    result = stats.players_by_country("can")
    assert len(result) == 2


def test_all_entries_returns_copy(stats):
    entries = stats.all_entries()
    entries.clear()
    assert len(stats.all_entries()) == 3


# ------------------------
# StatsApplication Logic Tests
# ------------------------

def test_sort_by_points(stats):
    app = StatsApplication()
    app._StatsApplication__stats = stats  # inject test stats

    sorted_players = app.sort_by_points(stats.all_entries())

    # Connor: 130 points
    assert sorted_players[0].name == "Connor McDavid"
    # Sidney: 90 points
    assert sorted_players[1].name == "Sidney Crosby"


def test_most_goals_sorting(stats):
    app = StatsApplication()
    app._StatsApplication__stats = stats

    players = sorted(
        stats.all_entries(),
        key=lambda p: (-p.goals, p.games)
    )

    assert players[0].name == "Connor McDavid"