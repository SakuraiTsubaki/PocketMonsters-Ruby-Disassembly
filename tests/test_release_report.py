from __future__ import annotations
import csv, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ReleaseReportTests(unittest.TestCase):
    def test_release_evidence_is_synchronized(self):
        project=json.loads((ROOT/"project.json").read_text(encoding="utf-8")); report=json.loads((ROOT/"analysis"/"ruby-release-header-report.json").read_text(encoding="utf-8"))
        with (ROOT/"research"/"releases.csv").open(newline="",encoding="utf-8") as stream: rows=list(csv.DictReader(stream))
        p={x["id"]:x for x in project["releases"]}; r={x["id"]:x for x in report["releases"]}; c={x["id"]:x for x in rows}
        self.assertEqual(set(p),set(r)); self.assertEqual(set(p),set(c)); self.assertEqual(len(p),4)
        for release_id,item in p.items(): self.assertEqual(item["status"],"candidate"); self.assertEqual(item["sha256"],r[release_id]["sha256"]); self.assertEqual(item["sha256"],c[release_id]["sha256"]); self.assertTrue(all(r[release_id]["validation"].values()))
    def test_region_codes_revisions_and_observed_sizes(self):
        releases=json.loads((ROOT/"analysis"/"ruby-release-header-report.json").read_text(encoding="utf-8"))["releases"]
        jp=next(x for x in releases if x["id"]=="ruby-jp-rev0"); western=sorted((x for x in releases if x["id"].startswith("ruby-en-")),key=lambda x:x["header"]["software_version"])
        self.assertEqual((jp["header"]["game_code"],jp["size"]),("AXVJ",8388608)); self.assertEqual([x["header"]["software_version"] for x in western],[0,1,2]); self.assertTrue(all(x["header"]["game_code"]=="AXVE" and x["size"]==16777216 for x in western))
if __name__=="__main__": unittest.main()
