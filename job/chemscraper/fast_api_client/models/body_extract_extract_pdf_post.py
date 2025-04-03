from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="BodyExtractExtractPdfPost")


@_attrs_define
class BodyExtractExtractPdfPost:
    """
    Attributes:
        pdf (Union[Unset, File]):
    """

    pdf: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pdf: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.pdf, Unset):
            pdf = self.pdf.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pdf is not UNSET:
            field_dict["pdf"] = pdf

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        pdf: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.pdf, Unset):
            pdf = self.pdf.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if pdf is not UNSET:
            field_dict["pdf"] = pdf

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _pdf = d.pop("pdf", UNSET)
        pdf: Union[Unset, File]
        if isinstance(_pdf, Unset):
            pdf = UNSET
        else:
            pdf = File(payload=BytesIO(_pdf))

        body_extract_extract_pdf_post = cls(
            pdf=pdf,
        )

        body_extract_extract_pdf_post.additional_properties = d
        return body_extract_extract_pdf_post

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
