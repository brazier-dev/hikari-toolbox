import hikari
import pytest

import toolbox


def test_validate_embed_valid():
    toolbox.validate_embed(
        hikari.Embed(
            title="a" * 256,
            description="a" * 1024,
        )
        .add_field(name="a" * 256, value="a" * 1024)
        .set_footer(text="a" * 2048)
        .set_author(name="a" * 256)
    )


def test_validate_embed_total_length():
    with pytest.raises(toolbox.EmbedValidationError):
        toolbox.validate_embed(
            hikari.Embed(
                title="a" * 256,
                description="a" * 4096,
            )
            .add_field(name="a" * 256, value="a" * 1024)
            .set_footer(text="a" * 2048)
            .set_author(name="a" * 256)
        )


def test_validate_embed_fields():
    with pytest.raises(toolbox.EmbedValidationError):
        embed = hikari.Embed()
        for _ in range(100):
            embed.add_field(name="a" * 256, value="a" * 1024)
        toolbox.validate_embed(embed)

    with pytest.raises(toolbox.EmbedValidationError):
        embed = hikari.Embed()
        for _ in range(3):
            embed.add_field(name="a" * 300, value="a" * 1200)
        toolbox.validate_embed(embed)


def test_validate_embed_title():
    with pytest.raises(toolbox.EmbedValidationError):
        toolbox.validate_embed(hikari.Embed(title="a" * 300))


def test_validate_embed_description():
    with pytest.raises(toolbox.EmbedValidationError):
        toolbox.validate_embed(hikari.Embed(description="a" * 5000))


def test_validate_embed_footer():
    with pytest.raises(toolbox.EmbedValidationError):
        toolbox.validate_embed(hikari.Embed().set_footer(text="a" * 3000))


def test_validate_embed_author():
    with pytest.raises(toolbox.EmbedValidationError):
        toolbox.validate_embed(hikari.Embed().set_author(name="a" * 300))
