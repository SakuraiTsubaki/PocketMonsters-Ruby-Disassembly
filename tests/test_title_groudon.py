import hashlib,json,struct,unittest
from pathlib import Path

ROOT=Path(__file__).parents[1]

class Tests(unittest.TestCase):
 def test_manifest_and_report_agree(self):
  manifest=json.loads((ROOT/'manifests/title-groudon.json').read_text())
  report=json.loads((ROOT/'analysis/ruby-jp-rev0-title-groudon.json').read_text())
  self.assertEqual(manifest['source']['offset'],f"0x{report['source_offset']:X}")
  self.assertEqual(manifest['decoded']['sha256'],report['decompressed_sha256'])
  self.assertEqual(manifest['decoded']['tile_count'],report['tile_count'])
  self.assertFalse(manifest['raw_rom_bytes_included'])
 def test_public_outputs_are_hash_locked(self):
  manifest=json.loads((ROOT/'manifests/title-groudon.json').read_text())
  for output in manifest['outputs'][:2]:
   data=(ROOT/output['path']).read_bytes()
   self.assertEqual(hashlib.sha256(data).hexdigest(),output['sha256'])
 def test_png_dimensions_and_color_type(self):
  png=(ROOT/'graphics/title/groudon-dark.png').read_bytes()
  self.assertEqual(png[:8],b'\x89PNG\r\n\x1a\n')
  self.assertEqual(struct.unpack('>II',png[16:24]),(256,256))
  self.assertEqual(png[25],2)

if __name__=='__main__': unittest.main()
