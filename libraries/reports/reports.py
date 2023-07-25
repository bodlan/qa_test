from dataclasses import dataclass, fields, asdict
from pandas import DataFrame


@dataclass
class ReportItem:
    test_name: str = ""
    status: str = ""
    comments: str = ""


class Report:
    def __init__(self):
        self.rows = []

    def add_row(self, report_object: ReportItem):
        self.rows.append(report_object)

    def generate_xlsx(self, filepath):
        try:
            fieldnames = [field.name for field in fields(ReportItem)]
            data = [asdict(item) for item in self.rows]
            df = DataFrame(data, columns=fieldnames)
            if not df.empty:
                df.to_excel(filepath, index=False, sheet_name="Report")

        except Exception as ex:
            raise ex
