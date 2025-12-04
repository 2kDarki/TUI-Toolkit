from tuikit.exceptions import TimeError, InputError
from datetime import datetime, timedelta, tzinfo
from tuikit.zonetools import Timezone
import unittest

class TestTimezone(unittest.TestCase):    
    def setUp(self):
        self.tz     = Timezone()
        self.dt_str = "2007-03-23T13:15:00"
        self.dt_obj = datetime(2007, 3, 23, 13, 15)

    def test_valid_abbreviation(self):
        self.assertEqual(self.tz.offset, 2)
        self.assertEqual(self.tz.name.upper(), "CAT")

    def test_valid_utc_offset_string(self):
        tz = Timezone("UTC+3")
        self.assertEqual(tz.offset, 3)
        self.assertTrue(tz.name.startswith("UTC+"))

    def test_valid_numeric_offset(self):
        tz = Timezone(2)
        self.assertEqual(tz.offset, 2)
        self.assertTrue(isinstance(tz.zone, tzinfo))

    def test_valid_iana_timezone(self):
        tz = Timezone("Africa/Harare")
        self.assertEqual(tz.offset, 2)
        self.assertEqual(tz.name, "Africa/Harare")

    def test_invalid_initializers(self):
        with self.assertRaises(TimeError):
            Timezone("Fake/Zone")
            Timezone(30)
            Timezone("UTC+25")

    def test_zoneinfo_format(self):
        tz = Timezone("UTC+5.5")
        name = tz.zone.tzname(None)
        self.assertEqual(name, "UTC+05:30")
    
    def test_list_zones_getter_timezones(self):
        zones = self.tz.list_zones(getter=True, 
                sort="Africa")
        self.assertIsInstance(zones, list)
        self.assertTrue(any("Africa/" in z for z in 
             zones))

    def test_list_zones_getter_aliases(self):
        aliases = self.tz.list_zones(aliased=True, 
                  getter=True, sort="C")
        self.assertIsInstance(aliases, list)
        self.assertIn("CAT", aliases)

    def test_list_zones_invalid_kwargs(self):
        with self.assertRaises(InputError):
             self.tz.list_zones(getter=True, 
             sort="XYZ")
             self.tz.list_zones(aliased=True, 
             getter=True, sort="??")
    
    def test_now_returns_datetime(self):
        self.assertIsInstance(self.tz.now, datetime)
        self.assertIsNotNone(self.tz.now.tzinfo)
    
    def test_localize_single_string(self):
        localized = self.tz.localize(self.dt_str)
        self.assertTrue(localized.tzinfo)

    def test_localize_single_datetime(self):
        localized = self.tz.localize(self.dt_obj)
        self.assertEqual(localized.tzinfo.utcoffset(
            localized), timedelta(hours=2))

    def test_localize_list_input(self):
        results = self.tz.localize([self.dt_str, 
                  self.dt_obj])
        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(r, datetime) 
             for r in results))

    def test_localize_multiple_args(self):
        results = self.tz.localize(self.dt_str, 
                  self.dt_obj)
        self.assertEqual(len(results), 2)
    
    def test_localize_invalid_args(self):
        with self.assertRaises(TimeError):
            self.tz.localize("invalid-date")
        with self.assertRaises(InputError):
            self.tz.localize()

    def test_convert_timezone(self):
        other = Timezone("UTC")
        dt = self.dt_obj.replace(tzinfo=self.tz.zone)
        converted = self.tz.convert(dt, "UTC")
        self.assertEqual(converted.tzinfo.utcoffset(
             converted), timedelta(0))

    def test_convert_invalid_input(self):
        with self.assertRaises(TimeError):
            self.tz.convert("not-a-datetime", "UTC")

    def test_iso_now_format(self):
        iso = self.tz.iso_now
        self.assertTrue(isinstance(iso, str))
        self.assertIn("T", iso)

    def test_diff_seconds(self):
        dt1  = "2007-03-23T10:00:00"
        dt2  = "2007-03-23T12:30:00"
        diff = self.tz.diff_seconds(dt1, dt2)
        self.assertEqual(diff, 9000.0)