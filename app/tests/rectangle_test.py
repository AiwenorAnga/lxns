import pytest
from app.rectangle import Rectangle


def test_are_rectangles_same():
    rectangle1 = Rectangle(
        x=100,
        y=200,
        width=50,
        height=50,
        color=(255.0, 0.0, 0.0),
        frame=1,
        video_height=1080,
    )
    rectangle2 = Rectangle(
        x=105,
        y=205,
        width=55,
        height=55,
        color=(255.0, 255.0, 255.0),
        frame=2,
        video_height=1080,
    )

    assert rectangle1.are_rectangles_same(rectangle1) is not False

    assert (
        rectangle1.are_rectangles_same(rectangle2, size_diff_threshold=0) is False
    ), "Too big size difference"
    assert (
        rectangle1.are_rectangles_same(rectangle2, size_diff_threshold=10) is not False
    )

    assert (
        rectangle1.are_rectangles_same(
            rectangle2, size_diff_threshold=10, distance_threshold=0
        )
        is False
    ), "Too big distance difference"
    assert (
        rectangle1.are_rectangles_same(
            rectangle2, size_diff_threshold=10, distance_threshold=10
        )
        is not False
    )


def test_same_rectangle_matching():
    # Initialize rectangles
    rect1 = Rectangle(
        x=10,
        y=20,
        width=100,
        height=100,
        color=tuple([255.0, 0.0, 0.0]),
        frame=1,
        video_height=1080,
    )
    rect2 = Rectangle(
        x=15,
        y=25,
        width=100,
        height=100,
        color=tuple([255.0, 0.0, 0.0]),
        frame=2,
        video_height=1080,
    )

    match = rect1.same_rectangle(rect2, video_height=1080)
    assert match is True
    assert rect1.x == 15
    assert rect1.y == 25
    assert rect1.width == 100
    assert rect1.height == 100
    assert rect1.frame == 2


def test_same_rectangle_not_matching():
    rect1 = Rectangle(
        x=10,
        y=20,
        width=100,
        height=50,
        color=tuple([255.0, 0.0, 0.0]),
        frame=1,
        video_height=1080,
    )
    rect2 = Rectangle(
        x=15,
        y=25,
        width=100,
        height=50,
        color=tuple([0.0, 255.0, 0.0]),
        frame=2,
        video_height=1080,
    )

    match = rect1.same_rectangle(rect2, video_height=1080)
    assert match is False
    assert rect1.x == 10
    assert rect1.y == 20
    assert rect1.width == 100
    assert rect1.height == 50
    assert rect1.frame == 1


if __name__ == "__main__":
    pytest.main()
