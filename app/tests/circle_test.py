import pytest
from app.circle import Circle


def test_filter_nan():
    color = (255.0, float("nan"), 0.0)
    filtered_color = Circle.filter_nan(color)
    assert filtered_color is None
    color = (255.0, 255.0, 0.0)


def test_is_valid_color():
    valid_color = (255.0, 0.0, 0.0)
    invalid_color = (256.0, 0.0, 0.0)
    invalid_color_2 = (256.0, "aa", 0.0)
    assert Circle.is_valid_color(valid_color) is True
    assert Circle.is_valid_color(invalid_color) is False
    assert Circle.is_valid_color(invalid_color_2) is False


def test_are_colors_similar():
    color1 = (255.0, 0.0, 0.0)
    color2 = (250.0, 5.0, 5.0)
    similar_color = (255.0, 0.0, 10.0)
    not_similar_color = (255.0, 0.0, 20.0)
    assert bool(Circle.are_colors_similar(color1, color2, tolerance=10)) is True
    assert bool(Circle.are_colors_similar(color1, similar_color, tolerance=10)) is True
    assert bool(Circle.are_colors_similar(color1, similar_color, tolerance=0)) is False
    assert (
        bool(Circle.are_colors_similar(color1, not_similar_color, tolerance=10))
        is False
    )


def test_are_circles_same():
    circle1 = Circle(
        x=100, y=200, radius=50, color=(255.0, 0.0, 0.0), frame=1, video_height=1080
    )
    circle2 = Circle(
        x=100, y=200, radius=100, color=(255.0, 0.0, 0.0), frame=2, video_height=1080
    )
    circle3 = Circle(
        x=150, y=250, radius=50, color=(255.0, 0.0, 0.0), frame=2, video_height=1080
    )

    assert circle1.are_circles_same(circle1) == 0

    assert circle1.are_circles_same(circle2, radius_threshold=50) is not False
    assert (
        circle1.are_circles_same(circle2, radius_threshold=49) is False
    ), "Too big radius difference"

    assert (
        circle1.are_circles_same(circle3, distance_threshold=70) is False
    ), "Too big distance difference"
    assert circle1.are_circles_same(circle3, distance_threshold=71) is not False


def test_same_circle():
    circle1 = Circle(
        x=100, y=200, radius=50, color=(255.0, 0.0, 0.0), frame=1, video_height=1080
    )
    circle2 = Circle(
        x=105, y=205, radius=50, color=(255.0, 0.0, 0.0), frame=2, video_height=1080
    )
    circle3 = Circle(
        x=110, y=210, radius=50, color=(255.0, 0.0, 0.0), frame=3, video_height=1080
    )
    circle4 = Circle(
        x=110, y=210, radius=50, color=(255.0, 0.0, 0.0), frame=53, video_height=1080
    )
    assert circle1.same_circle(circle2, video_height=1080) is True
    assert (
        circle3.same_circle(circle2, video_height=1080) is False
    ), "the same object can only be in the next frame"
    assert (
        circle3.same_circle(circle4, video_height=1080) is False
    ), "too big gap between frames"


if __name__ == "__main__":
    pytest.main()
