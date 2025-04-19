---
title: "Calendar Downloads"
---

This page provides downloadable `.ics` calendar files based on public data. Each file contains holidays for a specific region or context, as described below.

> ⚠️ Use at your own risk. No guarantee is given for accuracy, completeness, or fitness for any particular purpose.

## Available Calendar Files

{{< icalfilelist >}}

---

These files were generated using the following command:

```bash
python holidays_print.py --years-range -3 5 --region <REGION> --output <FILENAME> [--with-public|--with-unofficial]