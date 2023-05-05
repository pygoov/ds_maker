import csv


class XWriter:
    result: str

    def __init__(self) -> None:
        self.result = ""

    def write(self, s: str) -> None:
        self.result += s


def write_to_csv(data: list) -> str:
    writer = XWriter()
    scw_writer = csv.writer(
        writer,
        delimiter=',',
        quotechar='"',
        lineterminator="\n",
        quoting=csv.QUOTE_ALL
    )
    for line in data:
        scw_writer.writerow([line])
    return writer.result
