"""Lossless response models for evolving journal APIs."""

from pydantic import BaseModel, ConfigDict, Field, JsonValue


class APIModel(BaseModel):
    """Validate known fields and preserve additional JSON fields from the server."""

    model_config = ConfigDict(extra="allow")
    # Pydantic uses this narrower annotation to validate extra fields as JSON.
    __pydantic_extra__: dict[str, JsonValue] = Field(  # pyright: ignore[reportIncompatibleVariableOverride]
        init=False
    )


class UnconfirmedResponse(APIModel):
    """JSON object whose domain schema has not yet been observed.

    This deliberately promises only JSON validation and lossless serialization.
    It must not be treated as a confirmed description of the endpoint's fields.
    """
