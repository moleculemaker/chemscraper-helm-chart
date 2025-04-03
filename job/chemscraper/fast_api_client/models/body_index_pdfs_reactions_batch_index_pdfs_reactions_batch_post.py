import json
from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import File

T = TypeVar("T", bound="BodyIndexPdfsReactionsBatchIndexPdfsReactionsBatchPost")


@_attrs_define
class BodyIndexPdfsReactionsBatchIndexPdfsReactionsBatchPost:
    """
    Attributes:
        pdf_files (list[File]):
        json_reaction_files (list[File]):
        mapping_file (File):
    """

    pdf_files: list[File]
    json_reaction_files: list[File]
    mapping_file: File
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pdf_files = []
        for pdf_files_item_data in self.pdf_files:
            pdf_files_item = pdf_files_item_data.to_tuple()

            pdf_files.append(pdf_files_item)

        json_reaction_files = []
        for json_reaction_files_item_data in self.json_reaction_files:
            json_reaction_files_item = json_reaction_files_item_data.to_tuple()

            json_reaction_files.append(json_reaction_files_item)

        mapping_file = self.mapping_file.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pdf_files": pdf_files,
                "json_reaction_files": json_reaction_files,
                "mapping_file": mapping_file,
            }
        )

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        _temp_pdf_files = []
        for pdf_files_item_data in self.pdf_files:
            pdf_files_item = pdf_files_item_data.to_tuple()

            _temp_pdf_files.append(pdf_files_item)
        pdf_files = (None, json.dumps(_temp_pdf_files).encode(), "application/json")

        _temp_json_reaction_files = []
        for json_reaction_files_item_data in self.json_reaction_files:
            json_reaction_files_item = json_reaction_files_item_data.to_tuple()

            _temp_json_reaction_files.append(json_reaction_files_item)
        json_reaction_files = (None, json.dumps(_temp_json_reaction_files).encode(), "application/json")

        mapping_file = self.mapping_file.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "pdf_files": pdf_files,
                "json_reaction_files": json_reaction_files,
                "mapping_file": mapping_file,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pdf_files = []
        _pdf_files = d.pop("pdf_files")
        for pdf_files_item_data in _pdf_files:
            pdf_files_item = File(payload=BytesIO(pdf_files_item_data))

            pdf_files.append(pdf_files_item)

        json_reaction_files = []
        _json_reaction_files = d.pop("json_reaction_files")
        for json_reaction_files_item_data in _json_reaction_files:
            json_reaction_files_item = File(payload=BytesIO(json_reaction_files_item_data))

            json_reaction_files.append(json_reaction_files_item)

        mapping_file = File(payload=BytesIO(d.pop("mapping_file")))

        body_index_pdfs_reactions_batch_index_pdfs_reactions_batch_post = cls(
            pdf_files=pdf_files,
            json_reaction_files=json_reaction_files,
            mapping_file=mapping_file,
        )

        body_index_pdfs_reactions_batch_index_pdfs_reactions_batch_post.additional_properties = d
        return body_index_pdfs_reactions_batch_index_pdfs_reactions_batch_post

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
