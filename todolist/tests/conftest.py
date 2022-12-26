from pytest_factoryboy import register


from .factories import (
    GoalFactory,
    GoalCategoryFactory,
    GoalCommentFactory,
    BoardFactory,
)

pytest_plugins = 'tests.fixtures'


register(GoalFactory)
register(GoalCategoryFactory)
register(GoalCommentFactory)
register(BoardFactory)
