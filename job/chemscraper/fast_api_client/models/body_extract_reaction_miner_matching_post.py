from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="BodyExtractReactionMinerMatchingPost")


@_attrs_define
class BodyExtractReactionMinerMatchingPost:
    """
    Attributes:
        reaction_miner_json_file (File):
        pdf (Union[Unset, File]):
    """

    reaction_miner_json_file: File
    pdf: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reaction_miner_json_file = self.reaction_miner_json_file.to_tuple()

        pdf: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.pdf, Unset):
            pdf = self.pdf.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reaction_miner_json_file": reaction_miner_json_file,
            }
        )
        if pdf is not UNSET:
            field_dict["pdf"] = pdf

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        reaction_miner_json_file = self.reaction_miner_json_file.to_tuple()

        pdf: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.pdf, Unset):
            pdf = self.pdf.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "reaction_miner_json_file": reaction_miner_json_file,
            }
        )
        if pdf is not UNSET:
            field_dict["pdf"] = pdf

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reaction_miner_json_file = File(payload=BytesIO(d.pop("reaction_miner_json_file")))

        _pdf = d.pop("pdf", UNSET)
        pdf: Union[Unset, File]
        if isinstance(_pdf, Unset):
            pdf = UNSET
        else:
            pdf = File(payload=BytesIO(_pdf))

        body_extract_reaction_miner_matching_post = cls(
            reaction_miner_json_file=reaction_miner_json_file,
            pdf=pdf,
        )

        body_extract_reaction_miner_matching_post.additional_properties = d
        return body_extract_reaction_miner_matching_post

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
