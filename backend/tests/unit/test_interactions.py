"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_excludes_interaction_with_different_learner_id():
    """Test that filtering by item_id excludes interactions with different learner_id"""
    from app.models.interaction import InteractionModel
    
    interactions = [
        InteractionModel(id=1, learner_id=1, item_id=1, kind="view", created_at="2025-01-01"),
        InteractionModel(id=2, learner_id=2, item_id=1, kind="view", created_at="2025-01-01"),
        InteractionModel(id=3, learner_id=1, item_id=2, kind="view", created_at="2025-01-01"),
    ]
    
    from app.routers.interactions import _filter_by_item_id
    filtered = _filter_by_item_id(interactions, 1)
    
    assert len(filtered) == 2
    assert all(i.item_id == 1 for i in filtered)
    
def test_filter_no_matches_returns_empty():
    """Test filtering by item_id that doesn't exist returns empty list"""
    from app.models.interaction import InteractionModel
    from app.routers.interactions import _filter_by_item_id
    
    interactions = [
        InteractionModel(id=1, learner_id=1, item_id=1, kind="view", created_at="2025-01-01"),
        InteractionModel(id=2, learner_id=2, item_id=2, kind="view", created_at="2025-01-01"),
    ]
    
    filtered = _filter_by_item_id(interactions, 999)
    assert len(filtered) == 0
    assert filtered == []


def test_filter_handles_zero_and_negative_item_ids():
    """Test filtering with zero and negative item_id values (boundary testing)"""
    from app.models.interaction import InteractionModel
    from app.routers.interactions import _filter_by_item_id
    
    interactions = [
        InteractionModel(id=1, learner_id=1, item_id=0, kind="view", created_at="2025-01-01"),
        InteractionModel(id=2, learner_id=2, item_id=-1, kind="view", created_at="2025-01-01"),
        InteractionModel(id=3, learner_id=3, item_id=0, kind="view", created_at="2025-01-01"),
        InteractionModel(id=4, learner_id=4, item_id=5, kind="view", created_at="2025-01-01"),
    ]
    
    filtered = _filter_by_item_id(interactions, 0)
    assert len(filtered) == 2
    assert all(i.item_id == 0 for i in filtered)
    assert {i.id for i in filtered} == {1, 3}
