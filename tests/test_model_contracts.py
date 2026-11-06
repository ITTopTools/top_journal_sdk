"""Fixed synthetic contracts for every public DTO, independent of model annotations."""

import importlib
import inspect
import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest
from pydantic import BaseModel, JsonValue, TypeAdapter, ValidationError

from top_journal_sdk._models import APIModel, UnconfirmedResponse

_SAMPLES = TypeAdapter(dict[str, dict[str, JsonValue]]).validate_json(
    (Path(__file__).parent / "fixtures" / "model_samples.json").read_text()
)


def _model(name: str) -> type[BaseModel]:
    version, module, cls = name.split(".")
    return cast(
        type[BaseModel],
        getattr(importlib.import_module(f"top_journal_sdk.{version}.models.{module}"), cls),
    )


def test_every_model_has_a_reviewed_sample() -> None:
    discovered: set[str] = set()
    root = Path(__file__).parent.parent / "top_journal_sdk"
    for version in ("v1", "v2"):
        for path in (root / version / "models").glob("*.py"):
            if path.name.startswith("_"):
                continue
            module = importlib.import_module(f"top_journal_sdk.{version}.models.{path.stem}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module.__name__ and issubclass(obj, BaseModel):
                    discovered.add(f"{version}.{path.stem}.{name}")
    assert discovered == set(_SAMPLES)


@pytest.mark.parametrize("name", sorted(_SAMPLES))
def test_model_json_contract(name: str) -> None:
    """Known fields, aliases and nonempty nested payloads must survive a JSON round trip."""
    model = _model(name)
    payload = _SAMPLES[name]
    instance = model.model_validate_json(json.dumps(payload))
    # Contract fields must bind to declared attributes, not merely survive as extras.
    expected_extra: set[str] = {"newField"} if "newField" in payload else set()
    assert set(instance.model_extra or {}) == expected_extra
    result = instance.model_dump(mode="json", by_alias=True, exclude_unset=True)
    assert result == payload
    assert (
        model.model_validate_json(instance.model_dump_json()).model_dump() == instance.model_dump()
    )


@pytest.mark.parametrize(
    "name", [name for name in sorted(_SAMPLES) if issubclass(_model(name), APIModel)]
)
def test_responses_preserve_new_json_fields(name: str) -> None:
    payload = deepcopy(_SAMPLES[name])
    payload["unannouncedServerField"] = {"nested": [None, True, 3, 1.5, "text", {"x": []}]}
    instance = _model(name).model_validate(payload)
    assert (
        instance.model_dump(mode="json")["unannouncedServerField"]
        == payload["unannouncedServerField"]
    )


@pytest.mark.parametrize(
    "name", [name for name in sorted(_SAMPLES) if issubclass(_model(name), UnconfirmedResponse)]
)
def test_unconfirmed_schemas_preserve_entire_payload(name: str) -> None:
    payload = {"id": 123, "nested": {"values": [1, False, None]}, "text": "new schema"}
    assert _model(name).model_validate(payload).model_dump(exclude_unset=True) == payload


@pytest.mark.parametrize(
    "name,field,bad_value",
    [
        ("v1.attendance.AttendanceResponse", "date", "not-a-date"),
        ("v1.auth.LoginResponse", "access_token", []),
        ("v1.evaluation.EvaluationResponse", "teach_photo", "invalid-url"),
        ("v1.homework.HomeworkCounterResponse", "counter_type", 999),
        ("v1.schedule.LessonResponse", "started_at", "25:99:00"),
        ("v1.user.UserResponse", "age", {}),
        ("v2.auth.LoginResponse", "userType", {}),
        ("v2.home.AttendanceItem", "date", "2026-02-30"),
        ("v2.home.ProgressItem", "date", "tomorrow"),
        ("v2.home.ActivityItem", "date", "not-a-datetime"),
        ("v2.profile.Profile", "birthDate", "2026-02-30"),
        ("v2.profile.Payment", "nextPaymentDate", "tomorrow"),
        ("v2.profile.DocumentField", "files", ["invalid"]),
        ("v2.schedule.ScheduleItem", "startTime", "27:00"),
        ("v2.schedule.ScheduleItem", "date", "invalid"),
        ("v2.evaluation.ResponseMeta", "requestedAt", "invalid"),
        ("v2.evaluation.LessonEvaluationsResponse", "items", [1]),
        ("v2.stats.PageCountersResponse", "materialsNew", {}),
        ("v2.user.UserInfoResponse", "user", []),
        ("v2.stories.StoriesResponse", "items", [None]),
    ],
)
def test_models_reject_invalid_contract_fields(
    name: str, field: str, bad_value: JsonValue
) -> None:
    payload = deepcopy(_SAMPLES[name])
    payload[field] = bad_value
    with pytest.raises(ValidationError):
        _model(name).model_validate(payload)


def test_unknown_fields_reject_non_json_objects() -> None:
    with pytest.raises(ValidationError):
        UnconfirmedResponse.model_validate({"data": object()})


@pytest.mark.parametrize(
    "name,field",
    [
        ("v1.auth.LoginRequest", "password"),
        ("v1.evaluation.EvaluationRequest", "key"),
        ("v1.user.UserResponse", "student_id"),
        ("v2.auth.LoginRequest", "password"),
        ("v2.auth.LoginResponse", "userRole"),
        ("v2.evaluation.LessonEvaluationsResponse", "items"),
        ("v2.profile.DocumentField", "files"),
        ("v2.profile.DocumentFieldsResponse", "fields"),
        ("v2.schedule.ScheduleItem", "startTime"),
        ("v2.stats.HomeworkStatsResponse", "homeworkTotal"),
        ("v2.user.UserInfoResponse", "user"),
    ],
)
def test_required_contract_fields_cannot_be_omitted(name: str, field: str) -> None:
    payload = deepcopy(_SAMPLES[name])
    del payload[field]
    with pytest.raises(ValidationError) as exc:
        _model(name).model_validate(payload)
    assert any(error["type"] == "missing" for error in exc.value.errors())


def test_schedule_lookup_and_missing_lesson() -> None:
    from top_journal_sdk.v1.exceptions import LessonNotFoundError
    from top_journal_sdk.v1.models.schedule import ScheduleResponse

    schedule = ScheduleResponse.model_validate(_SAMPLES["v1.schedule.ScheduleResponse"])
    assert schedule.lesson(1).subject_name == "Math"
    with pytest.raises(LessonNotFoundError):
        schedule.lesson(99)


def test_mutable_defaults_are_isolated_between_profiles() -> None:
    from top_journal_sdk.v1.models.profile import ProfilePhoneResponse, ProfileSettingsResponse

    first = ProfileSettingsResponse()
    second = ProfileSettingsResponse()
    first.phones.append(ProfilePhoneResponse(phone_number="70000000000"))
    assert second.phones == []


def test_startup_prompts_accept_legacy_and_camel_case_keys() -> None:
    from top_journal_sdk.v2.models.startup import (
        EmailConfirmationResponse,
        OpenedInterviewResponse,
    )

    email = EmailConfirmationResponse.model_validate(
        {
            "emailConfirmation": {
                "delay_count": 1,
                "max_delay_count": 3,
                "unknownFlag": True,
            }
        }
    )
    assert email.email_confirmation is not None
    assert email.email_confirmation.delay_count == 1
    assert email.email_confirmation.model_dump()["unknownFlag"] is True
    interview = OpenedInterviewResponse.model_validate(
        {
            "openedInterview": {
                "id": 7,
                "delayCount": 1,
                "maxDelayCount": 3,
                "message_type": 2,
            }
        }
    )
    assert interview.opened_interview is not None
    assert interview.opened_interview.id == 7
    assert interview.opened_interview.message_type == 2


def test_profile_accepts_nonempty_moderation_objects() -> None:
    from top_journal_sdk.v2.models.profile import DeclineComment, DocumentField, Profile

    profile = deepcopy(_SAMPLES["v2.profile.Profile"])
    profile["declineComment"] = {"message": "Please upload again", "reasonCode": 2}
    value = Profile.model_validate(profile)
    assert isinstance(value.decline_comment, DeclineComment)
    assert value.decline_comment.message == "Please upload again"
    document = DocumentField.model_validate(_SAMPLES["v2.profile.DocumentField"])
    assert document.moderation is not None
    assert document.moderation.status is False
    with pytest.raises(ValidationError):
        DocumentField.model_validate(
            {**_SAMPLES["v2.profile.DocumentField"], "moderation": {"status": []}}
        )
