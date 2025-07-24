from typing import Any, Dict, List, cast
from src.gdocs.service import get_service
from src.gdocs.utils import LANGUAGE_COLORS, find_backtick_lines, get_index_of_line_start


class GoogleDocsEngine:
    def __init__(self, service_account_file: str, document_id: str) -> None:
        self.service = cast(Any, get_service(service_account_file))
        self.document_id = document_id

    def insert_text(self, text: str) -> None:
        insert_request = {
            "insertText": {
                "location": {"index": 1},
                "text": text
            }
        }
        style_request = {
            "updateTextStyle": {
                "range": {
                    "startIndex": 1,
                    "endIndex": 1 + len(text)
                },
                "textStyle": {
                    "weightedFontFamily": {
                        "fontFamily": "Montserrat"
                    }
                },
                "fields": "weightedFontFamily"
            }
        }

        self.service.documents().batchUpdate(
            documentId=self.document_id,
            body={"requests": [insert_request, style_request]}
        ).execute()

        doc = self.service.documents().get(documentId=self.document_id).execute()

        backticks = find_backtick_lines(text)
        print(backticks)
        # e.g. backticks == [(1, '```go'), (3, '```end'), …]

        style_requests: List[Dict] = []
        open_line = None
        current_lang = None

        for line_num, content in backticks:
            # compute character index where this line begins
            start_index = get_index_of_line_start(doc, line_number=line_num)
            if content.startswith("```") and content != "```end":
                # e.g. content=="```go"
                current_lang = content[3:].strip()  # "go"
                open_line = start_index # line_num
            else:  # assume content=="```end"
                if open_line is None or current_lang is None:
                    continue  # mismatched end - end without beginning
                # compute end index: end of this line plus its newline
                end_index = get_index_of_line_start(doc, line_number=line_num + 1)
                # look up color
                rgb = LANGUAGE_COLORS.get(current_lang, {"red":0,"green":0,"blue":0})
                style_requests.append({
                    "updateTextStyle": {
                        "range": {"startIndex": open_line, "endIndex": end_index},
                        "textStyle": {
                            "foregroundColor": {"color": {"rgbColor": rgb}},
                            "weightedFontFamily": {
                                "fontFamily": "Montserrat"
                            },
                        },
                        "fields": "foregroundColor, weightedFontFamily"
                    }
                })
                # reset for next block
                open_line = None
                current_lang = None

        # 4) Batch everything
        requests = style_requests
        result = self.service.documents().batchUpdate(
            documentId=self.document_id,
            body={"requests": requests}
        ).execute()
        print(f"Updated doc. Total changes: {len(result.get('replies', []))}")
