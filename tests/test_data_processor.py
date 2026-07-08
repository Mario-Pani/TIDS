import unittest

from data_processor import identify_unit_type, process_files


class DataProcessorTests(unittest.TestCase):
    def test_identify_reactor(self):
        content = "REACTOR_GEN=1\nGM$=M"
        self.assertEqual(identify_unit_type(content, "unit.ehv"), "Reactor")

    def test_identify_series_from_filename(self):
        content = "GM$=M"
        self.assertEqual(identify_unit_type(content, "my_series_unit.ehv"), "Series")

    def test_identify_series_from_gm_suffix(self):
        content = "GM$=XS"
        self.assertEqual(identify_unit_type(content, "unit.ehv"), "Series")

    def test_identify_main_unit_default(self):
        content = "GM$=M"
        self.assertEqual(identify_unit_type(content, "unit.ehv"), "Main Unit")

    def test_process_files_preserves_order_and_overrides(self):
        base = "A=1\nB=2\nA=9\n#comment\nBROKENLINE"
        extra = "B=20\nC=3"

        unit_type, merged = process_files(base, "unit.ehv", extra)

        self.assertEqual(unit_type, "Main Unit")
        lines = merged.splitlines()
        self.assertEqual(lines[0], "A                   =9")
        self.assertEqual(lines[1], "B                   =20")
        self.assertEqual(lines[2], "C                   =3")

    def test_main_unit_adjusts_core_and_hv_bot_elct(self):
        base = "GM$=M\nCORE_WINDOW_HT=12.9\nHV_BOT_ELCT_CLR=3.1"
        extra = ""

        unit_type, merged = process_files(base, "unit.ehv", extra)

        self.assertEqual(unit_type, "Main Unit")
        self.assertIn("CORE_WINDOW_HT      =12.59", merged)
        self.assertIn("HV_BOT_ELCT_CLR     =2.79", merged)

    def test_non_main_unit_does_not_adjust(self):
        base = "REACTOR_GEN=1\nCORE_WINDOW_HT=12.9\nHV_BOT_ELCT_CLR=3.1"
        extra = ""

        unit_type, merged = process_files(base, "unit.ehv", extra)

        self.assertEqual(unit_type, "Reactor")
        self.assertIn("CORE_WINDOW_HT      =12.9", merged)
        self.assertIn("HV_BOT_ELCT_CLR     =3.1", merged)

    def test_main_unit_adjusts_with_mixed_case_keys(self):
        base = "GM$=M\nCore_WINDOW_HT=12.9\nhv_bot_elct_clr=3.1"
        extra = ""

        unit_type, merged = process_files(base, "unit.ehv", extra)

        self.assertEqual(unit_type, "Main Unit")
        self.assertIn("Core_WINDOW_HT      =12.59", merged)
        self.assertIn("hv_bot_elct_clr     =2.79", merged)

    def test_can_disable_main_unit_adjustments(self):
        base = "GM$=M\nCORE_WINDOW_HT=12.9\nHV_BOT_ELCT_CLR=3.1"
        extra = ""

        unit_type, merged = process_files(base, "unit.ehv", extra, apply_main_adjustments=False)

        self.assertEqual(unit_type, "Main Unit")
        self.assertIn("CORE_WINDOW_HT      =12.9", merged)
        self.assertIn("HV_BOT_ELCT_CLR     =3.1", merged)


if __name__ == "__main__":
    unittest.main()
