from pydantic import ConfigDict

from top_journal_sdk._models import APIModel
from top_journal_sdk.v2.models._aliases import to_camel


class V2Model(APIModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
