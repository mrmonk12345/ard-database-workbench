from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt


def create_libraries_table(samples, amplicons):
    table = QTableWidget(len(samples), len(amplicons) + 1)

    # headers
    headers = ["Sample"] + [str(a["amplicon_type_id"]) for a in amplicons]
    table.setHorizontalHeaderLabels(headers)

    for row, sample in enumerate(samples):
        # sample label column
        item = QTableWidgetItem(sample["sample_label"])
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row, 0, item)

        for col, amp in enumerate(amplicons, start=1):
            checkbox = QTableWidgetItem()
            checkbox.setFlags(
                Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
            )
            checkbox.setCheckState(Qt.CheckState.Unchecked)

            table.setItem(row, col, checkbox)

    table.resizeColumnsToContents()

    return table


def extract_sample_amplicons(table, samples, amplicons):
    result = []

    for row, sample in enumerate(samples):
        selected = []

        for col, amp in enumerate(amplicons, start=1):
            item = table.item(row, col)

            if item and item.checkState() == Qt.CheckState.Checked:
                selected.append(amp["amplicon_type_id"])

        if selected:
            result.append({
                "sample_id": sample["sample_id"],
                "amplicon_type_ids": selected
            })

    return result